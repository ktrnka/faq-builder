#!/usr/bin/env python3
"""
FAQ Builder CLI - A tool for building FAQs from various sources.
"""

import os
import click
from dotenv import load_dotenv
from googleapiclient.discovery import build


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


if __name__ == "__main__":
    cli()
