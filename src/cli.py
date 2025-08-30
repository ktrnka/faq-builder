#!/usr/bin/env python3
"""
FAQ Builder CLI - A tool for building FAQs from various sources.
"""

import os
import time

import click
from dotenv import load_dotenv
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables
load_dotenv()

# Hard-coded playlist ID for TechJoy Academy Replays
TECHJOYLIVE_PLAYLIST_ID = "PLuePfAWKCLvUbnk7vAcQIXtPlMDtz6Ses"


def get_youtube_api_key():
    """Get YouTube API key from environment variables.

    Returns:
        str: The API key if found

    Raises:
        click.ClickException: If API key is not found
    """
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise click.ClickException("YOUTUBE_API_KEY not found in environment variables. Please add your YouTube API key to the .env file.")
    return api_key


def download_video_transcript(video_id, languages, output_dir, youtube_client=None):
    """Download transcript for a video and save to file.

    Args:
        video_id: YouTube video ID (already cleaned)
        languages: List of language codes
        output_dir: Base directory to save the file
        youtube_client: Optional YouTube API client for getting video metadata

    Returns:
        str: Path to the saved file

    Raises:
        click.ClickException: If file already exists or download fails
    """
    # Get video metadata to extract publish date
    publish_date = "unknown"
    if youtube_client:
        try:
            video_request = youtube_client.videos().list(
                part="snippet",
                id=video_id
            )
            video_response = video_request.execute()
            
            if video_response["items"]:
                published_at = video_response["items"][0]["snippet"]["publishedAt"]
                # Convert from ISO format (2025-08-29T23:01:01Z) to YYYY-MM-DD
                publish_date = published_at.split("T")[0]
        except Exception:
            # If we can't get metadata, use unknown
            pass
    
    # Create youtube subdirectory structure
    youtube_dir = os.path.join(output_dir, "youtube")
    filename = f"{publish_date}_{video_id}.txt"
    output_file = os.path.join(youtube_dir, filename)
    
    # Check if file already exists
    if os.path.exists(output_file):
        raise click.ClickException(f"Transcript file already exists: {output_file}")

    # Get transcript
    ytt_api = YouTubeTranscriptApi()
    fetched_transcript = ytt_api.fetch(video_id)

    if not fetched_transcript or len(fetched_transcript) == 0:
        raise click.ClickException("No transcript found for this video.")

    # Prepare transcript content (always with timestamps)
    transcript_lines = []
    for snippet in fetched_transcript:
        text = snippet.text.strip()
        # Convert start time to minutes:seconds format
        start_seconds = int(snippet.start)
        minutes = start_seconds // 60
        seconds = start_seconds % 60
        timestamp = f"[{minutes:02d}:{seconds:02d}]"
        transcript_lines.append(f"{timestamp} {text}")

    # Calculate total duration
    total_minutes = 0
    total_seconds = 0
    if len(fetched_transcript) > 0:
        last_snippet = fetched_transcript[-1]
        total_duration = int(last_snippet.start + last_snippet.duration)
        total_minutes = total_duration // 60
        total_seconds = total_duration % 60

    # Create output directory and save file
    os.makedirs(youtube_dir, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        # Write header information
        f.write("YouTube Video Transcript\n")
        f.write(f"Video ID: {video_id}\n")
        f.write(f"Publish Date: {publish_date}\n")
        f.write(f"Language: {fetched_transcript.language} ({fetched_transcript.language_code})\n")
        f.write(f"Generated: {'Yes' if fetched_transcript.is_generated else 'No'}\n")
        f.write(f"Total segments: {len(fetched_transcript)}\n")
        f.write(f"Total duration: {total_minutes:02d}:{total_seconds:02d}\n")
        f.write("=" * 60 + "\n\n")

        # Write transcript content
        for line in transcript_lines:
            f.write(line + "\n")

    return output_file


@click.group()
def cli():
    """FAQ Builder - Build FAQs from various sources."""
    pass


@cli.command()
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


@cli.command()
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
        original_input = video_id
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
            
            # Read back the file to get summary info
            with open(output_file, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # Extract info from header
            segments_line = next((line for line in lines if line.startswith("Total segments:")), None)
            duration_line = next((line for line in lines if line.startswith("Total duration:")), None)

            if segments_line:
                click.echo(f"📊 {segments_line.strip()}")
            if duration_line:
                click.echo(f"⏱️  {duration_line.strip()}")
                
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


if __name__ == "__main__":
    cli()
