#!/usr/bin/env python3
"""
FAQ Builder CLI - A tool for building FAQs from various sources.
"""

import os
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
        raise click.ClickException(
            "YOUTUBE_API_KEY not found in environment variables. "
            "Please add your YouTube API key to the .env file."
        )
    return api_key


def download_video_transcript(video_id, languages, output_dir):
    """Download transcript for a video and save to file.
    
    Args:
        video_id: YouTube video ID (already cleaned)
        languages: List of language codes
        output_dir: Directory to save the file
        
    Returns:
        str: Path to the saved file
        
    Raises:
        click.ClickException: If file already exists or download fails
    """
    # Check if file already exists
    output_file = os.path.join(output_dir, f"{video_id}.txt")
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
    os.makedirs(output_dir, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write header information
        f.write("YouTube Video Transcript\n")
        f.write(f"Video ID: {video_id}\n")
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
def list_videos(search_term, playlist_id):
    """List videos from a YouTube playlist that contain the search term in the title."""
    
    # Get YouTube API key from environment
    api_key = get_youtube_api_key()
    
    # Build YouTube API client
    youtube = build("youtube", "v3", developerKey=api_key)
    
    click.echo(f"🔍 Searching for videos containing '{search_term}' in playlist...")
    click.echo()
    
    # Get playlist items
    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=playlist_id,
        maxResults=50
    )
    response = request.execute()
    
    matching_videos = []
    
    for item in response["items"]:
        title = item["snippet"]["title"]
        video_id = item["contentDetails"]["videoId"]
        
        # Check if search term is in the title (case-insensitive)
        if search_term.lower() in title.lower():
            matching_videos.append({
                "title": title,
                "video_id": video_id,
                "url": f"https://www.youtube.com/watch?v={video_id}"
            })
    
    # Display results
    if matching_videos:
        click.echo(f"✅ Found {len(matching_videos)} video(s) containing '{search_term}':")
        click.echo()
        
        for i, video in enumerate(matching_videos, 1):
            click.echo(f"{i}. {video['title']}")
            click.echo(f"   🔗 {video['url']}")
            click.echo()
    else:
        click.echo(f"❌ No videos found containing '{search_term}' in the title.")


@cli.command()
@click.argument("video_id")
@click.option("--languages", default="en", help="Comma-separated list of language codes (default: en)")
@click.option("--output-dir", default="data", help="Directory to save transcript files (default: data)")
def download_transcript(video_id, languages, output_dir):
    """Download and save the transcript for a YouTube video.
    
    VIDEO_ID can be either a YouTube video ID (e.g., 'dQw4w9WgXcQ') 
    or a full YouTube URL (e.g., 'https://www.youtube.com/watch?v=dQw4w9WgXcQ').
    
    Saves the transcript with timestamps to data/{video_id}.txt
    """
    
    # Extract video ID from URL if needed
    if "youtube.com/watch?v=" in video_id or "youtu.be/" in video_id:
        if "youtube.com/watch?v=" in video_id:
            video_id = video_id.split("watch?v=")[1].split("&")[0]
        elif "youtu.be/" in video_id:
            video_id = video_id.split("youtu.be/")[1].split("?")[0]
    
    # Parse language codes
    language_codes = [lang.strip() for lang in languages.split(",")]
    
    click.echo(f"🔍 Fetching transcript for video ID: {video_id}")
    click.echo(f"📝 Languages: {', '.join(language_codes)}")
    
    # Download transcript to file
    output_file = download_video_transcript(video_id, language_codes, output_dir)
    
    click.echo(f"💾 Transcript saved to: {output_file}")
    
    # Read back the file to get summary info
    with open(output_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    # Extract info from header
    segments_line = next((line for line in lines if line.startswith("Total segments:")), None)
    duration_line = next((line for line in lines if line.startswith("Total duration:")), None)
    
    if segments_line:
        click.echo(f"📊 {segments_line.strip()}")
    if duration_line:
        click.echo(f"⏱️  {duration_line.strip()}")


if __name__ == "__main__":
    cli()
