"""YouTube-related CLI commands."""

import json
import logging
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Iterator, Dict, Any

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

logger = logging.getLogger(__name__)


def is_youtube_blocking_error(error_msg: str) -> bool:
    """Check if error message indicates YouTube is blocking requests."""
    blocking_indicators = [
        "YouTube is blocking requests from your IP",
        "too many requests",
        "IP has been blocked by YouTube",
        "cloud provider",
        "requests from an IP belonging to a cloud provider",
        "Could not retrieve a transcript for the video",
        "This is most likely caused by:"
    ]
    return any(indicator.lower() in error_msg.lower() for indicator in blocking_indicators)


def get_youtube_api_key() -> str:
    """Get YouTube API key from environment variables."""
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise click.ClickException("YOUTUBE_API_KEY not found in environment variables. Please add your YouTube API key to the .env file.")
    return api_key


def fetch_playlist_items(youtube_client, playlist_id: str, max_pages: int) -> Iterator[Dict[str, Any]]:
    """Generator that fetches playlist items with pagination.
    
    Args:
        youtube_client: YouTube API client
        playlist_id: YouTube playlist ID to fetch from
        max_pages: Maximum number of pages to fetch
        
    Yields:
        Dict: Individual playlist item from API response
    """
    page_token = None
    request_params = {
        "part": "snippet,contentDetails",
        "playlistId": playlist_id,
        "maxResults": 50
    }
    
    for page_num in range(max_pages):
        if page_num > 0:
            time.sleep(1)  # Rate limiting
            
        if page_token:
            request_params["pageToken"] = page_token
        elif "pageToken" in request_params:
            del request_params["pageToken"]
            
        request = youtube_client.playlistItems().list(**request_params)
        response = request.execute()
        
        logger.debug(f"Processed page {page_num + 1} with {len(response['items'])} videos")
        
        # Yield each item from this page
        for item in response["items"]:
            yield item
        
        # Check if there are more pages
        page_token = response.get("nextPageToken")
        if not page_token:
            logger.info(f"Reached end of playlist at page {page_num + 1}")
            break


def download_video_transcript(video_id: str, languages: list[str], output_dir: str, youtube_client=None) -> tuple[str, bool]:
    """Download transcript for a video and save to file.
    
    Returns:
        tuple: (file_path, was_downloaded) where was_downloaded is False if file already existed
    """
    metadata = None
    publish_date = "unknown"

    # Check in the raw subdirectory for existing files
    youtube_raw_dir = os.path.join(output_dir, "youtube", "raw")
    if os.path.exists(youtube_raw_dir):
        for file in os.listdir(youtube_raw_dir):
            if video_id in file:
                path = os.path.join(youtube_raw_dir, file)
                logger.debug(f"Transcript already exists for video: {video_id} in {path}, skipping")
                return path, False

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

    return output_file, True


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


def find_cleaned_transcript_file(video_id: str, cleaned_dir: str) -> str:
    """Find a cleaned transcript file by video ID.
    
    Looks for files matching the pattern *_{video_id}.json in the cleaned directory.
    
    Args:
        video_id: YouTube video ID to search for
        cleaned_dir: Directory containing cleaned transcript files
        
    Returns:
        Path to the matching file
        
    Raises:
        click.ClickException: If directory doesn't exist, no files found, or multiple matches
    """
    cleaned_dir_path = Path(cleaned_dir)
    if not cleaned_dir_path.exists():
        raise click.ClickException(f"Cleaned directory not found: {cleaned_dir}")
    
    # Find files that match the pattern *_{video_id}.json
    matching_files = list(cleaned_dir_path.glob(f"*_{video_id}.json"))
    
    if not matching_files:
        raise click.ClickException(f"No cleaned transcript found for video ID: {video_id} in {cleaned_dir}")
    elif len(matching_files) > 1:
        # Show available options if multiple matches
        click.echo(f"Multiple files found for video ID '{video_id}':")
        for f in matching_files:
            click.echo(f"  - {f}")
        raise click.ClickException("Please specify the full filename to disambiguate")
    else:
        return str(matching_files[0])


@click.group()
def youtube():
    """YouTube video processing commands."""
    pass


@youtube.command("list-videos")
@click.option("--search-term", default="Keith", help="Search term to filter video titles (default: Keith)")
@click.option("--playlist-id", default=TECHJOYLIVE_PLAYLIST_ID, help="YouTube playlist ID to scan")
@click.option("--max-pages", default=10, help="Maximum number of pages to fetch (default: 10)")
@click.option("--output-file", type=str, help="File to save video IDs to (one per line for xargs)")
def list_videos(search_term: str, playlist_id: str, max_pages: int, output_file: str) -> None:
    """List videos from a YouTube playlist that contain the search term in the title.
    
    Args:
        search_term: Term to search for in video titles
        playlist_id: YouTube playlist ID to scan
        max_pages: Maximum number of pages to fetch
        output_file: Optional file to save video IDs to
    """
    # Get YouTube API key from environment
    api_key = get_youtube_api_key()

    # Build YouTube API client
    youtube = build("youtube", "v3", developerKey=api_key)

    logger.debug(f"Searching for videos containing '{search_term}' in playlist...")
    logger.debug(f"Will fetch up to {max_pages} pages of results...")

    # Get all playlist items with pagination using generator
    matching_videos = []
    total_videos_processed = 0
    
    for item in fetch_playlist_items(youtube, playlist_id, max_pages):
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

    # Handle output
    if output_file:
        # Save video IDs to file
        with open(output_file, 'w') as f:
            for video in matching_videos:
                f.write(f"{video['video_id']}\n")
        click.echo(f"✅ Saved {len(matching_videos)} video IDs to {output_file}")
    else:
        # Display results to console
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
@click.option("--block-retry-delay", default=300, help="Seconds to wait when YouTube blocks us (default: 300 = 5 minutes)")
@click.option("--max-retries", default=3, help="Maximum number of retries for blocked requests (default: 3)")
def download_transcript(video_ids, languages, output_dir, block_retry_delay, max_retries):
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

    logger.debug(f"Downloading transcripts for {len(video_ids)} video(s)")
    logger.debug(f"Languages: {', '.join(language_codes)}")

    successful_downloads = []
    failed_downloads = []

    for i, video_id in enumerate(video_ids, 1):
        # Extract video ID from URL if needed
        if "youtube.com/watch?v=" in video_id or "youtu.be/" in video_id:
            if "youtube.com/watch?v=" in video_id:
                video_id = video_id.split("watch?v=")[1].split("&")[0]
            elif "youtu.be/" in video_id:
                video_id = video_id.split("youtu.be/")[1].split("?")[0]

        logger.debug(f"[{i}/{len(video_ids)}] Processing video ID: {video_id}")
        
        # Retry logic for YouTube blocking
        attempt = 0
        while attempt < max_retries:
            try:
                # Download transcript to file
                output_file, was_downloaded = download_video_transcript(video_id, language_codes, output_dir, youtube)
                
                if was_downloaded:
                    click.echo(f"✅ Transcript downloaded to: {output_file}")
                else:
                    click.echo(f"⏭️  Transcript already exists: {output_file}")
                successful_downloads.append(video_id)
                
                # Basic validation - just check we got some content
                with open(output_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                transcript = data["transcript"]
                snippet_count = len(transcript["snippets"])
                
                if snippet_count == 0:
                    click.echo(f"⚠️  Warning: No transcript segments found")
                else:
                    logger.debug(f"Retrieved {snippet_count} transcript segments")
                break  # Success, exit retry loop
                    
            except Exception as e:
                error_msg = str(e)
                
                # Check for YouTube blocking
                if is_youtube_blocking_error(error_msg):
                    attempt += 1
                    if attempt < max_retries:
                        click.echo(f"🚫 YouTube blocking detected (attempt {attempt}/{max_retries})")
                        click.echo(f"😴 Waiting {block_retry_delay} seconds ({block_retry_delay//60} minutes) before retry...")
                        time.sleep(block_retry_delay)
                        continue
                    else:
                        final_error = f"YouTube blocking after {max_retries} attempts: {error_msg}"
                        click.echo(f"❌ Failed: {final_error}")
                        failed_downloads.append((video_id, final_error))
                        break
                else:
                    # Non-blocking error, don't retry
                    if isinstance(e, click.ClickException):
                        click.echo(f"❌ Failed: {e}")
                        failed_downloads.append((video_id, str(e)))
                    else:
                        error_msg = f"Unexpected error: {e}"
                        click.echo(f"❌ Failed: {error_msg}")
                        failed_downloads.append((video_id, error_msg))
                    break
        
        # Sleep between downloads (except after the last one)
        if i < len(video_ids):
            logger.debug("Sleeping 10 seconds between downloads...")
            time.sleep(10)

    # Summary
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
@click.argument("transcript_files", nargs=-1, required=True, type=click.Path(exists=True, readable=True))
@click.option("--max-lines", type=int, help="Maximum number of lines to process (for testing)")
@click.option("--output-dir", default="data", help="Base output directory (default: data)")
@click.option("--force", is_flag=True, help="Force rebuild even if cleaned file already exists")
def clean_transcript(transcript_files, max_lines, output_dir, force):
    """Clean and segment YouTube transcripts using LLM.
    
    Takes one or more JSON transcript files and produces cleaned, segmented versions
    with chapters, speaker identification, and improved formatting.
    
    Automatically determines output path: raw/filename.json -> cleaned/filename.json
    Skips files that already have cleaned versions unless --force is used.
    
    Examples:
        # Clean a single file
        faq-builder youtube clean-transcript data/youtube/raw/video.json
        
        # Clean multiple files
        faq-builder youtube clean-transcript data/youtube/raw/*.json
        
        # Force rebuild existing cleaned files
        faq-builder youtube clean-transcript --force data/youtube/raw/*.json
    """
    
    successful_cleans = []
    failed_cleans = []
    skipped_cleans = []
    
    for i, transcript_file in enumerate(transcript_files, 1):
        click.echo(f"📄 [{i}/{len(transcript_files)}] Processing: {transcript_file}")
        
        try:
            # Determine output file path - same filename in cleaned directory
            input_path = os.path.abspath(transcript_file)
            filename = os.path.basename(input_path)
            output_file = os.path.join(output_dir, "youtube", "cleaned_test" if max_lines else "cleaned", filename)

            # Check if output file already exists and we're not forcing rebuild
            if not force and os.path.exists(output_file):
                click.echo(f"⏭️  Cleaned version already exists: {output_file}")
                skipped_cleans.append(transcript_file)
                continue

            logger.debug(f"Output will be saved to: {output_file}")

            # Get the formatted text (same as show-transcript)
            formatted_text = format_transcript_readable(transcript_file)
            
            # Optionally truncate for testing
            if max_lines:
                lines = formatted_text.split('\n')
                if len(lines) > max_lines:
                    formatted_text = '\n'.join(lines[:max_lines])
                    logger.debug(f"Truncated to {max_lines} lines for testing")
            
            # Count tokens for cost estimation
            encoding = tiktoken.encoding_for_model("gpt-4")
            token_count = len(encoding.encode(formatted_text))
            logger.debug(f"Processing {token_count:,} tokens")
            
            # Initialize LLM prompt
            client = get_openai_client()
            prompt = TranscriptCleaningPrompt(client)
            
            logger.debug("Sending to LLM for cleaning and segmentation...")
            
            # Execute the prompt
            cleaned_result = prompt.execute(transcript_text=formatted_text)
            
            # Create output directory if needed
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            # Save the result as JSON
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(cleaned_result.model_dump(), f, indent=2, ensure_ascii=False)
            
            click.echo(f"✅ Cleaned transcript saved to: {output_file}")
            successful_cleans.append(transcript_file)
            
            # Basic validation - check we got chapters and content
            if not cleaned_result.chapters:
                click.echo("⚠️  Warning: No chapters found in cleaned transcript")
            else:
                logger.info(f"Created {len(cleaned_result.chapters)} chapters")
                
        except Exception as e:
            error_msg = f"Error cleaning transcript: {e}"
            click.echo(f"❌ {error_msg}", err=True)
            failed_cleans.append((transcript_file, error_msg))
            # Continue processing other files instead of crashing
            continue
    
    # Summary
    click.echo("=" * 60)
    click.echo(f"📊 Summary: {len(successful_cleans)} cleaned, {len(skipped_cleans)} skipped, {len(failed_cleans)} failed")
    
    if successful_cleans:
        click.echo("✅ Successfully cleaned:")
        for file in successful_cleans:
            click.echo(f"   - {os.path.basename(file)}")
    
    if skipped_cleans:
        click.echo("⏭️  Skipped (already exists):")
        for file in skipped_cleans:
            click.echo(f"   - {os.path.basename(file)}")
    
    if failed_cleans:
        click.echo("❌ Failed:")
        for file, error in failed_cleans:
            click.echo(f"   - {os.path.basename(file)}: {error}")


@youtube.command("show-cleaned-transcript")
@click.argument("video_id_or_file", type=str)
@click.option("--cleaned-dir", default="data/youtube/cleaned", help="Directory containing cleaned transcript files (default: data/youtube/cleaned)")
def show_cleaned_transcript(video_id_or_file: str, cleaned_dir: str) -> None:
    """Display a cleaned transcript in human-readable format.
    
    Can take either a video ID (looks for *_{video_id}.json in cleaned-dir) or a direct path to a cleaned transcript file.
    Output can be piped to 'less' for paging through long transcripts.
    
    Examples:
        # Using video ID (finds matching file with date prefix)
        faq-builder youtube show-cleaned-transcript Ms1BLfwLRNY
        
        # Using full path
        faq-builder youtube show-cleaned-transcript data/youtube/cleaned/2025-05-16_Ms1BLfwLRNY.json
    """
    try:
        # Determine if input is a video ID or file path
        if os.path.exists(video_id_or_file):
            cleaned_file = video_id_or_file
        else:
            cleaned_file = find_cleaned_transcript_file(video_id_or_file, cleaned_dir)
        
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
