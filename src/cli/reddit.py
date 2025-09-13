"""Reddit-related CLI commands."""

import json
import os
from datetime import datetime

import click
import praw
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


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


@click.group()
def reddit():
    """Reddit comment processing commands."""
    pass


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
