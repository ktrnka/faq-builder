import json
import os
import time
from datetime import datetime
from typing import List, Optional, Tuple

import click
import praw
import tiktoken
from dotenv import load_dotenv
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables
load_dotenv()

# Hard-coded playlist ID for TechJoy Academy Replays
TECHJOYLIVE_PLAYLIST_ID = "PLuePfAWKCLvUbnk7vAcQIXtPlMDtz6Ses"


def get_youtube_api_key() -> str:
    """Get YouTube API key from environment variables."""
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise click.ClickException("YOUTUBE_API_KEY not found in environment variables. Please add your YouTube API key to the .env file.")
    return api_key


def get_reddit_client() -> praw.Reddit:
    """Get Reddit client using credentials from environment variables."""
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        raise click.ClickException("REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET not found in environment variables. Please add your Reddit API credentials to the .env file.")
    
    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent="faq-builder/0.1.0 by /u/trnka"
    )


def download_user_comments(username: str, subreddit_names: list[str], limit: int, output_dir: str) -> tuple[str, int, dict[str, int]]:
    """Download comments from a specific user across multiple subreddits."""
    reddit_dir = os.path.join(output_dir, "reddit")
    os.makedirs(reddit_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    subreddits_str = ",".join(subreddit_names)
    filename = f"{username}_{subreddits_str}_comments_{timestamp}.json"
    output_file = os.path.join(reddit_dir, filename)
    
    reddit = get_reddit_client()
    
    try:
        user = reddit.redditor(username)
    except Exception as e:
        raise click.ClickException(f"Failed to access Reddit user: {e}")
    
    target_subreddits = [name.lower() for name in subreddit_names]
    
    comments_data = []
    comments_found = 0
    subreddit_counts = {name: 0 for name in subreddit_names}
    
    try:
        for comment in user.comments.new(limit=None):
            comment_subreddit = comment.subreddit.display_name.lower()
            
            if comment_subreddit in target_subreddits:
                original_subreddit_name = comment.subreddit.display_name
                
                comments_data.append({
                    "id": comment.id,
                    "text": comment.body,
                    "timestamp": datetime.fromtimestamp(comment.created_utc).isoformat(),
                    "permalink": f"https://www.reddit.com{comment.permalink}",
                    "score": comment.score,
                    "subreddit": original_subreddit_name,
                    "post_title": comment.submission.title if comment.submission else None,
                    "post_url": comment.submission.url if comment.submission else None,
                    "post_id": comment.submission.id if comment.submission else None
                })
                
                # Update counts
                comments_found += 1
                # Find matching subreddit name for counting (case-insensitive)
                for original_name in subreddit_names:
                    if original_name.lower() == comment_subreddit:
                        subreddit_counts[original_name] += 1
                        break
                
                if comments_found >= limit:
                    break
    except Exception as e:
        raise click.ClickException(f"Failed to fetch comments: {e}")
    
    if not comments_data:
        subreddits_list = ", ".join(subreddit_names)
        raise click.ClickException(f"No comments found for user '{username}' in subreddits: {subreddits_list}")
    
    # Save to JSON file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(comments_data, f, indent=2, ensure_ascii=False)
    
    return output_file, comments_found, subreddit_counts


def download_video_transcript(video_id: str, languages: list[str], output_dir: str, youtube_client=None) -> str:
    """Download transcript for a video and save to file."""
    metadata = None
    publish_date = "unknown"

    for file in os.listdir(output_dir):
        if video_id in file:
            path = os.path.join(output_dir, file)
            click.echo(f"📄 Transcript already exists for video: {video_id} in {path}, skipping")
            return path

    if youtube_client:
        try:
            video_request = youtube_client.videos().list(
                part="snippet,statistics,contentDetails",
                id=video_id
            )
            video_response = video_request.execute()
            
            if video_response["items"]:
                metadata = video_response["items"][0]
                published_at = metadata["snippet"]["publishedAt"]
                publish_date = published_at.split("T")[0]
        except Exception:
            pass
    
    youtube_dir = os.path.join(output_dir, "youtube")
    filename = f"{publish_date}_{video_id}.json"
    output_file = os.path.join(youtube_dir, filename)

    ytt_api = YouTubeTranscriptApi()
    fetched_transcript = ytt_api.fetch(video_id)

    if not fetched_transcript or len(fetched_transcript) == 0:
        raise click.ClickException("No transcript found for this video.")

    # Convert transcript to serializable format
    transcript_data = []
    for snippet in fetched_transcript:
        transcript_data.append({
            "text": snippet.text,
            "start": snippet.start,
            "duration": snippet.duration
        })

    # Prepare the JSON data structure
    json_data = {
        "metadata": metadata,
        "transcript": {
            "video_id": fetched_transcript.video_id,
            "language": fetched_transcript.language,
            "language_code": fetched_transcript.language_code,
            "is_generated": fetched_transcript.is_generated,
            "snippets": transcript_data
        }
    }

    # Create output directory and save file
    os.makedirs(youtube_dir, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

    return output_file


def format_transcript_readable(transcript_file: str) -> str:
    """Format a transcript JSON file into human-readable text."""
    with open(transcript_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Extract metadata
    metadata = data.get("metadata", {})
    title = metadata.get("snippet", {}).get("title", "Unknown Title")
    published_at = metadata.get("snippet", {}).get("publishedAt", "Unknown Date")
    
    # Format date nicely
    try:
        if published_at != "Unknown Date":
            date_obj = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
            formatted_date = date_obj.strftime("%Y-%m-%d")
        else:
            formatted_date = published_at
    except Exception:
        formatted_date = published_at
    
    # Build the formatted transcript
    lines = []
    lines.append(f"Title: {title}")
    lines.append(f"Date: {formatted_date}")
    lines.append("")  # Empty line
    
    # Add transcript segments
    transcript = data.get("transcript", {})
    snippets = transcript.get("snippets", [])
    
    for snippet in snippets:
        start_time = snippet.get("start", 0)
        text = snippet.get("text", "")
        
        # Convert start time to minutes:seconds format
        minutes = int(start_time // 60)
        seconds = int(start_time % 60)
        timestamp = f"[{minutes:02d}:{seconds:02d}]"
        
        lines.append(f"{timestamp} {text}")
    
    return "\n".join(lines)


@click.group()
def cli():
    """FAQ Builder - Build FAQs from various sources."""
    pass


@cli.group()
def youtube():
    """YouTube video processing commands."""
    pass


@cli.group()
def reddit():
    """Reddit comment processing commands."""
    pass


@youtube.command("list-videos")
@click.option("--search-term", default="Keith", help="Search term to filter video titles (default: Keith)")
@click.option("--playlist-id", default=TECHJOYLIVE_PLAYLIST_ID, help="YouTube playlist ID to scan")
@click.option("--max-pages", default=10, help="Maximum number of pages to fetch (default: 10)")
def list_videos(search_term, playlist_id, max_pages):
    """List videos from a YouTube playlist that contain the search term in the title."""

    # Get YouTube API key from environment
    api_key = get_youtube_api_key()

    # Build YouTube API client
    youtube = build("youtube", "v3", developerKey=api_key)

    click.echo(f"🔍 Searching for videos containing '{search_term}' in playlist...")
    click.echo(f"📄 Will fetch up to {max_pages} pages of results...")
    click.echo()

    # Get all playlist items with pagination
    matching_videos = []
    page_token = None
    total_videos_processed = 0
    request_params = {
        "part": "snippet,contentDetails",
        "playlistId": playlist_id,
        "maxResults": 50
    }
    
    for page_num in range(max_pages):
        if page_num > 0:
            time.sleep(1)
        request = youtube.playlistItems().list(**request_params)
        response = request.execute()
        
        # Process videos from this page
        page_videos = 0
        for item in response["items"]:
            total_videos_processed += 1
            title = item["snippet"]["title"]
            video_id = item["contentDetails"]["videoId"]
            
            # Check if search term is in the title (case-insensitive)
            if search_term.lower() in title.lower():
                matching_videos.append({
                    "title": title,
                    "video_id": video_id,
                    "url": f"https://www.youtube.com/watch?v={video_id}"
                })
            page_videos += 1
        
        click.echo(f"📄 Processed page {page_num + 1} with {page_videos} videos (total: {total_videos_processed})")
        
        # Check if there are more pages
        page_token = response.get("nextPageToken")
        request_params["pageToken"] = page_token
        if not page_token:
            click.echo(f"🏁 Reached end of playlist at page {page_num + 1}")
            break
    
    click.echo()

    # Display results
    if matching_videos:
        click.echo(f"✅ Found {len(matching_videos)} video(s) containing '{search_term}' out of {total_videos_processed} total videos:")
        click.echo()

        for i, video in enumerate(matching_videos, 1):
            click.echo(f"{i}. {video['title']}")
            click.echo(f"   🔗 {video['url']}")
            click.echo()
    else:
        click.echo(f"❌ No videos found containing '{search_term}' in the title out of {total_videos_processed} total videos.")


@youtube.command("download-transcript")
@click.argument("video_ids", nargs=-1, required=True)
@click.option("--languages", default="en", help="Comma-separated list of language codes (default: en)")
@click.option("--output-dir", default="data", help="Directory to save transcript files (default: data)")
def download_transcript(video_ids, languages, output_dir):
    """Download and save transcripts for one or more YouTube videos.

    VIDEO_IDS can be one or more YouTube video IDs (e.g., 'dQw4w9WgXcQ')
    or full YouTube URLs (e.g., 'https://www.youtube.com/watch?v=dQw4w9WgXcQ').

    Saves transcripts with timestamps to data/youtube/{date}_{video_id}.txt
    """
    
    # Get YouTube API key and build client for metadata
    api_key = get_youtube_api_key()
    youtube = build("youtube", "v3", developerKey=api_key)

    # Parse language codes
    language_codes = [lang.strip() for lang in languages.split(",")]

    click.echo(f"🔍 Downloading transcripts for {len(video_ids)} video(s)")
    click.echo(f"📝 Languages: {', '.join(language_codes)}")
    click.echo()

    successful_downloads = []
    failed_downloads = []

    for i, video_id in enumerate(video_ids, 1):
        # Extract video ID from URL if needed
        if "youtube.com/watch?v=" in video_id or "youtu.be/" in video_id:
            if "youtube.com/watch?v=" in video_id:
                video_id = video_id.split("watch?v=")[1].split("&")[0]
            elif "youtu.be/" in video_id:
                video_id = video_id.split("youtu.be/")[1].split("?")[0]

        click.echo(f"� [{i}/{len(video_ids)}] Processing video ID: {video_id}")
        
        try:
            # Download transcript to file
            output_file = download_video_transcript(video_id, language_codes, output_dir, youtube)
            
            click.echo(f"✅ Transcript saved to: {output_file}")
            successful_downloads.append(video_id)
            
            # Read back the JSON file to get summary info
            with open(output_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Extract info from JSON structure
            transcript = data["transcript"]
            snippet_count = len(transcript["snippets"])
            
            # Calculate total duration
            total_duration = 0
            if transcript["snippets"]:
                last_snippet = transcript["snippets"][-1]
                total_duration = int(last_snippet["start"] + last_snippet["duration"])
            
            total_minutes = total_duration // 60
            total_seconds = total_duration % 60

            click.echo(f"📊 Total segments: {snippet_count}")
            click.echo(f"⏱️  Total duration: {total_minutes:02d}:{total_seconds:02d}")
            click.echo(f"📝 Language: {transcript['language']} ({transcript['language_code']})")
            click.echo(f"🤖 Generated: {'Yes' if transcript['is_generated'] else 'No'}")
                
        except click.ClickException as e:
            click.echo(f"❌ Failed: {e}")
            failed_downloads.append((video_id, str(e)))
        except Exception as e:
            error_msg = f"Unexpected error: {e}"
            click.echo(f"❌ Failed: {error_msg}")
            failed_downloads.append((video_id, error_msg))
        
        # Sleep between downloads (except after the last one)
        if i < len(video_ids):
            click.echo("😴 Sleeping 10 seconds between downloads...")
            time.sleep(10)
            click.echo()

    # Summary
    click.echo()
    click.echo("=" * 60)
    click.echo(f"📊 Summary: {len(successful_downloads)} successful, {len(failed_downloads)} failed")
    
    if successful_downloads:
        click.echo(f"✅ Successfully downloaded: {', '.join(successful_downloads)}")
    
    if failed_downloads:
        click.echo("❌ Failed downloads:")
        for video_id, error in failed_downloads:
            click.echo(f"   - {video_id}: {error}")


@youtube.command("show-transcript")
@click.argument("transcript_file", type=click.Path(exists=True, readable=True))
def show_transcript(transcript_file):
    """Display a YouTube transcript in human-readable format.
    
    Takes a JSON transcript file and formats it with timestamps and metadata.
    Output can be piped to 'less' for paging through long transcripts.
    
    Example: faq-builder youtube show-transcript data/youtube/2025-09-06__-tRDk3P7bg.json | less
    """
    try:
        formatted_text = format_transcript_readable(transcript_file)
        click.echo(formatted_text)
    except Exception as e:
        click.echo(f"❌ Error formatting transcript: {e}", err=True)


@youtube.command("count-tokens")
@click.argument("transcript_file", type=click.Path(exists=True, readable=True))
def count_tokens(transcript_file):
    """Count tokens in a YouTube transcript using GPT-4 tokenizer.
    
    Displays token count for the human-readable formatted transcript,
    which is useful for determining if content fits within LLM context limits.
    """
    try:
        # Get the formatted text (same as show-transcript)
        formatted_text = format_transcript_readable(transcript_file)
        
        # Count tokens using tiktoken for GPT-4
        encoding = tiktoken.encoding_for_model("gpt-4")
        token_count = len(encoding.encode(formatted_text))
        
        # Calculate character count for reference
        char_count = len(formatted_text)
        
        # Show results
        click.echo(f"📄 File: {transcript_file}")
        click.echo(f"🔢 Tokens: {token_count:,}")
        click.echo(f"📝 Characters: {char_count:,}")
        click.echo(f"📏 Ratio: {char_count/token_count:.2f} chars/token" if token_count > 0 else "📏 Ratio: N/A")
        
        # Show context window status for common models
        click.echo()
        click.echo("🤖 Model compatibility:")
        
        # GitHub models have 2k input + 1k output = 3k total budget
        # But we need to reserve space for prompt, so let's say 1.5k for transcript
        github_limit = 1500
        if token_count <= github_limit:
            click.echo(f"   ✅ GitHub models (2k input): {token_count}/{github_limit} tokens")
        else:
            click.echo(f"   ❌ GitHub models (2k input): {token_count}/{github_limit} tokens (too large)")
        
        # GPT-4 turbo has much larger context
        gpt4_limit = 128000
        if token_count <= gpt4_limit:
            click.echo(f"   ✅ GPT-4 Turbo: {token_count}/{gpt4_limit:,} tokens")
        else:
            click.echo(f"   ❌ GPT-4 Turbo: {token_count}/{gpt4_limit:,} tokens (too large)")
            
    except Exception as e:
        click.echo(f"❌ Error counting tokens: {e}", err=True)


@reddit.command("download-user-comments")
@click.option("--username", default="trnka", help="Reddit username to fetch comments from (default: trnka)")
@click.option("--subreddits", default="mlquestions,machinelearning,gamedev,learnmachinelearning,mlops,aws,LanguageTechnology", help="Comma-separated list of subreddits to filter comments by (default: mlquestions,machinelearning,gamedev,learnmachinelearning,mlops,aws,LanguageTechnology)")
@click.option("--limit", default=50, help="Maximum total number of comments to fetch across all subreddits (default: 50)")
@click.option("--output-dir", default="data", help="Directory to save comment files (default: data)")
def download_user_comments_cmd(username, subreddits, limit, output_dir):
    """Download comments from a Reddit user across multiple subreddits.
    
    Downloads comments from the specified user that were posted in any of the specified subreddits
    and saves them to a JSON file in data/reddit/ with timestamp.
    """
    # Parse subreddit list
    subreddit_list = [s.strip() for s in subreddits.split(",") if s.strip()]
    
    click.echo(f"🔍 Downloading up to {limit} comments from u/{username}")
    click.echo(f"📍 Searching in subreddits: {', '.join([f'r/{s}' for s in subreddit_list])}")
    click.echo()
    
    try:
        output_file, comment_count, subreddit_counts = download_user_comments(username, subreddit_list, limit, output_dir)
        
        click.echo(f"✅ Successfully downloaded {comment_count} comments")
        click.echo(f"💾 Saved to: {output_file}")
        
        # Show breakdown by subreddit
        click.echo()
        click.echo("📊 Comments by subreddit:")
        for subreddit, count in subreddit_counts.items():
            if count > 0:
                click.echo(f"   r/{subreddit}: {count} comments")
        
        # Show a sample of the first comment if available
        with open(output_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        if data:
            first_comment = data[0]
            click.echo()
            click.echo("📝 Sample comment (first one):")
            click.echo(f"   Subreddit: r/{first_comment['subreddit']}")
            click.echo(f"   Timestamp: {first_comment['timestamp']}")
            click.echo(f"   Score: {first_comment['score']}")
            click.echo(f"   Text preview: {first_comment['text'][:100]}{'...' if len(first_comment['text']) > 100 else ''}")
            click.echo(f"   Permalink: {first_comment['permalink']}")
            
    except click.ClickException as e:
        click.echo(f"❌ Failed: {e}")
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    cli()
