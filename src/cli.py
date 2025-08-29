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


@click.group()
def cli():
    """FAQ Builder - Build FAQs from various sources."""
    pass


@cli.command()
@click.option("--search-term", default="Keith", help="Search term to filter video titles (default: Keith)")
@click.option("--playlist-id", default=TECHJOYLIVE_PLAYLIST_ID, help="YouTube playlist ID to scan")
def list_videos(search_term, playlist_id):
    """List videos from a YouTube playlist that contain the search term in the title."""
    
    try:
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
    
    except click.ClickException:
        # Re-raise click exceptions (like our API key error)
        raise
    except Exception as e:
        raise click.ClickException(f"Error accessing YouTube API: {e}")


@cli.command()
@click.argument("video_id")
@click.option("--timestamps", is_flag=True, help="Include timestamps in the output")
@click.option("--languages", default="en", help="Comma-separated list of language codes (default: en)")
def download_transcript(video_id, timestamps, languages):
    """Download and display the transcript for a YouTube video.
    
    VIDEO_ID can be either a YouTube video ID (e.g., 'dQw4w9WgXcQ') 
    or a full YouTube URL (e.g., 'https://www.youtube.com/watch?v=dQw4w9WgXcQ').
    """
    
    # Extract video ID from URL if needed
    if "youtube.com/watch?v=" in video_id or "youtu.be/" in video_id:
        if "youtube.com/watch?v=" in video_id:
            video_id = video_id.split("watch?v=")[1].split("&")[0]
        elif "youtu.be/" in video_id:
            video_id = video_id.split("youtu.be/")[1].split("?")[0]
    
    try:
        # Parse language codes
        language_codes = [lang.strip() for lang in languages.split(",")]
        
        click.echo(f"🔍 Fetching transcript for video ID: {video_id}")
        click.echo(f"📝 Languages: {', '.join(language_codes)}")
        click.echo()
        
        # Get transcript
        ytt_api = YouTubeTranscriptApi()
        fetched_transcript = ytt_api.fetch(video_id)
        
        if not fetched_transcript or len(fetched_transcript) == 0:
            click.echo("❌ No transcript found for this video.")
            return
        
        click.echo(f"✅ Found transcript with {len(fetched_transcript)} segments:")
        click.echo(f"📝 Language: {fetched_transcript.language} ({fetched_transcript.language_code})")
        click.echo(f"🤖 Generated: {'Yes' if fetched_transcript.is_generated else 'No'}")
        click.echo("=" * 60)
        
        # Display transcript
        for snippet in fetched_transcript:
            text = snippet.text.strip()
            
            if timestamps:
                # Convert start time to minutes:seconds format
                start_seconds = int(snippet.start)
                minutes = start_seconds // 60
                seconds = start_seconds % 60
                timestamp = f"[{minutes:02d}:{seconds:02d}]"
                click.echo(f"{timestamp} {text}")
            else:
                click.echo(text)
        
        click.echo("=" * 60)
        click.echo(f"📊 Total segments: {len(fetched_transcript)}")
        
        # Calculate total duration
        if len(fetched_transcript) > 0:
            last_snippet = fetched_transcript[-1]
            total_duration = int(last_snippet.start + last_snippet.duration)
            total_minutes = total_duration // 60
            total_seconds = total_duration % 60
            click.echo(f"⏱️  Total duration: {total_minutes:02d}:{total_seconds:02d}")
    
    except Exception as e:
        raise click.ClickException(f"Error fetching transcript: {e}")


if __name__ == "__main__":
    cli()
