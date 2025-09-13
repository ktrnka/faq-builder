"""YouTube-related CLI commands."""

import json
import os
import time
from datetime import datetime

import click
import tiktoken
from dotenv import load_dotenv
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

from ..llm.client import get_openai_client
from ..llm.prompts.transcript_cleaning import TranscriptCleaningPrompt

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


def download_video_transcript(video_id: str, languages: list[str], output_dir: str, youtube_client=None) -> str:
    """Download transcript for a video and save to file."""
    metadata = None
    publish_date = "unknown"

    # Check in the raw subdirectory for existing files
    youtube_raw_dir = os.path.join(output_dir, "youtube", "raw")
    if os.path.exists(youtube_raw_dir):
        for file in os.listdir(youtube_raw_dir):
            if video_id in file:
                path = os.path.join(youtube_raw_dir, file)
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
    
    youtube_raw_dir = os.path.join(output_dir, "youtube", "raw")
    filename = f"{publish_date}_{video_id}.json"
    output_file = os.path.join(youtube_raw_dir, filename)

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
    os.makedirs(youtube_raw_dir, exist_ok=True)

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
def youtube():
    """YouTube video processing commands."""
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

    Saves transcripts with timestamps to data/youtube/raw/{date}_{video_id}.json
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

        click.echo(f"📹 [{i}/{len(video_ids)}] Processing video ID: {video_id}")
        
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
    
    Example: faq-builder youtube show-transcript data/youtube/raw/2025-09-06__-tRDk3P7bg.json | less
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


@youtube.command("clean-transcript")
@click.argument("transcript_file", type=click.Path(exists=True, readable=True))
@click.option("--max-lines", type=int, help="Maximum number of lines to process (for testing)")
@click.option("--output-dir", default="data", help="Base output directory (default: data)")
def clean_transcript(transcript_file, max_lines, output_dir):
    """Clean and segment a YouTube transcript using LLM.
    
    Takes a JSON transcript file and produces a cleaned, segmented version
    with chapters, speaker identification, and improved formatting.
    
    Automatically determines output path: raw/filename.json -> cleaned/filename.json
    
    TRANSCRIPT_FILE: Input JSON transcript (e.g., data/youtube/raw/2025-09-06__-tRDk3P7bg.json)
    """
    try:
        click.echo(f"🔍 Processing transcript: {transcript_file}")
        
        # Determine output file path - same filename in cleaned directory
        input_path = os.path.abspath(transcript_file)
        filename = os.path.basename(input_path)
        output_file = os.path.join(output_dir, "youtube", "cleaned", filename)
        
        click.echo(f"� Output will be saved to: {output_file}")
        
        # Get the formatted text (same as show-transcript)
        formatted_text = format_transcript_readable(transcript_file)
        
        # Optionally truncate for testing
        if max_lines:
            lines = formatted_text.split('\n')
            if len(lines) > max_lines:
                formatted_text = '\n'.join(lines[:max_lines])
                click.echo(f"📏 Truncated to {max_lines} lines for testing")
        
        # Count tokens for cost estimation
        encoding = tiktoken.encoding_for_model("gpt-4")
        token_count = len(encoding.encode(formatted_text))
        click.echo(f"🔢 Processing {token_count:,} tokens")
        
        # Initialize LLM prompt
        client = get_openai_client()
        prompt = TranscriptCleaningPrompt(client)
        
        click.echo("🤖 Sending to LLM for cleaning and segmentation...")
        
        # Execute the prompt
        cleaned_result = prompt.execute(transcript_text=formatted_text)
        
        # Create output directory if needed
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Save the result as JSON
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(cleaned_result.model_dump(), f, indent=2, ensure_ascii=False)
        
        click.echo(f"✅ Cleaned transcript saved to: {output_file}")
        
        # Show summary stats
        click.echo()
        click.echo("📊 Summary:")
        click.echo(f"   📖 Title: {cleaned_result.title}")
        click.echo(f"   📅 Date: {cleaned_result.date}")
        click.echo(f"   ⏱️  Duration: {int(cleaned_result.total_duration_seconds // 60):02d}:{int(cleaned_result.total_duration_seconds % 60):02d}")
        click.echo(f"   📝 Chapters: {len(cleaned_result.chapters)}")
        
        # Show chapter breakdown
        if cleaned_result.chapters:
            click.echo()
            click.echo("📚 Chapters:")
            for i, chapter in enumerate(cleaned_result.chapters, 1):
                duration_mins = int(chapter.start_time // 60)
                duration_secs = int(chapter.start_time % 60)
                click.echo(f"   {i}. [{duration_mins:02d}:{duration_secs:02d}] {chapter.title} ({chapter.chapter_type})")
        
        # Show processing notes if any
        if cleaned_result.processing_notes:
            click.echo()
            click.echo("📋 Processing notes:")
            for note in cleaned_result.processing_notes:
                click.echo(f"   • {note}")
                
    except Exception as e:
        click.echo(f"❌ Error cleaning transcript: {e}", err=True)
        raise  # Let it crash during development as requested


@youtube.command("show-cleaned-transcript")
@click.argument("cleaned_file", type=click.Path(exists=True, readable=True))
def show_cleaned_transcript(cleaned_file):
    """Display a cleaned transcript in human-readable format.
    
    Takes a cleaned JSON transcript file and formats it for easy review.
    Output can be piped to 'less' for paging through long transcripts.
    
    Example: faq-builder youtube show-cleaned-transcript data/cleaned/transcript_cleaned.json | less
    """
    try:
        with open(cleaned_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Build the formatted output
        lines = []
        lines.append(f"Title: {data['title']}")
        lines.append(f"Date: {data['date']}")
        lines.append(f"Duration: {int(data['total_duration_seconds'] // 60):02d}:{int(data['total_duration_seconds'] % 60):02d}")
        lines.append("")  # Empty line
        
        # Add chapters
        for chapter in data['chapters']:
            # Chapter header
            start_mins = int(chapter['start_time'] // 60)
            start_secs = int(chapter['start_time'] % 60)
            lines.append(f"## [{start_mins:02d}:{start_secs:02d}] {chapter['title']} ({chapter['chapter_type']})")
            lines.append("")
            
            # Chapter segments
            for segment in chapter['segments']:
                speaker_prefix = f"**{segment['speaker']}**: " if segment['speaker'] != "Host" else ""
                lines.append(f"{speaker_prefix}{segment['text']}")
                lines.append("")  # Empty line after each segment
            
            lines.append("---")  # Separator between chapters
            lines.append("")
        
        # Add processing notes if any
        if data.get('processing_notes'):
            lines.append("## Processing Notes")
            lines.append("")
            for note in data['processing_notes']:
                lines.append(f"• {note}")
            lines.append("")
        
        # Output the formatted text
        formatted_text = "\n".join(lines)
        click.echo(formatted_text)
        
    except Exception as e:
        click.echo(f"❌ Error formatting cleaned transcript: {e}", err=True)
