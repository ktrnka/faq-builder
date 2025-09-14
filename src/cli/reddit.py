"""Reddit-related CLI commands."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Set

import click
import praw
from dotenv import load_dotenv

from src.reddit_models import RedditThread, UserComment

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


def load_user_comments(input_file: str) -> List[UserComment]:
    """Load user comments from JSON file."""
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    return [UserComment(**comment) for comment in data]


def extract_unique_post_ids(comments: List[UserComment]) -> Set[str]:
    """Extract unique post IDs from user comments."""
    return {comment.post_id for comment in comments if comment.post_id}


def fetch_reddit_thread(reddit: praw.Reddit, post_id: str) -> RedditThread:
    """Fetch full Reddit thread data using PRAW."""
    try:
        submission = reddit.submission(id=post_id)
        
        # Fetch comments with limit
        submission.comments.replace_more(limit=100)
        comments = submission.comments.list()
        
        return RedditThread.from_praw_data(submission, comments)
        
    except Exception as e:
        raise click.ClickException(f"Failed to fetch thread {post_id}: {e}")


def save_thread_to_file(thread: RedditThread, threads_dir: str) -> str:
    """Save thread to individual JSON file."""
    Path(threads_dir).mkdir(parents=True, exist_ok=True)
    
    filename = f"{thread.submission.id}.json"
    output_path = Path(threads_dir) / filename
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(thread.model_dump(), f, indent=2, ensure_ascii=False)
    
    return str(output_path)


@reddit.command("enrich-threads")
@click.argument("input_file", type=click.Path(exists=True))
@click.option("--output-dir", default="data/reddit/threads", help="Directory to save thread files (default: data/reddit/threads)")
def enrich_threads_cmd(input_file, output_dir):
    """Enrich user comments with full Reddit thread data.
    
    Takes a JSON file of user comments and fetches the complete thread data for each
    unique post, saving individual thread files to the output directory.
    """
    click.echo(f"🔍 Loading user comments from: {input_file}")
    
    try:
        # Load and process comments
        comments = load_user_comments(input_file)
        unique_post_ids = extract_unique_post_ids(comments)
        
        click.echo(f"📊 Found {len(comments)} comments across {len(unique_post_ids)} unique threads")
        
        # Initialize Reddit client
        reddit = get_reddit_client()
        
        # Process each thread
        threads_processed = 0
        threads_skipped = 0
        
        for post_id in unique_post_ids:
            thread_file = Path(output_dir) / f"{post_id}.json"
            
            if thread_file.exists():
                click.echo(f"⏭️  Skipping {post_id} (already exists)")
                threads_skipped += 1
                continue
            
            try:
                click.echo(f"📡 Fetching thread: {post_id}")
                thread = fetch_reddit_thread(reddit, post_id)
                output_path = save_thread_to_file(thread, output_dir)
                
                click.echo(f"💾 Saved thread with {thread.total_comments} comments to: {output_path}")
                threads_processed += 1
                
            except Exception as e:
                click.echo(f"❌ Failed to process {post_id}: {e}")
                continue
        
        click.echo()
        click.echo(f"✅ Successfully processed {threads_processed} threads")
        if threads_skipped > 0:
            click.echo(f"⏭️  Skipped {threads_skipped} existing threads")
        click.echo(f"📁 Threads saved to: {output_dir}")
        
    except Exception as e:
        click.echo(f"❌ Failed: {e}")


@reddit.command("show-thread")
@click.argument("post_id_or_file", type=str)
@click.option("--threads-dir", default="data/reddit/threads", help="Directory containing thread files (default: data/reddit/threads)")
@click.option("--user", default="trnka", help="Username to highlight in conversation (default: trnka)")
def show_thread_cmd(post_id_or_file, threads_dir, user):
    """Display a Reddit thread in readable format.
    
    Can take either a post ID (looks for {post_id}.json in threads-dir) or a direct path to a thread file.
    """
    try:
        # Determine if input is a post ID or file path
        if Path(post_id_or_file).exists():
            thread_file = post_id_or_file
        else:
            thread_file = Path(threads_dir) / f"{post_id_or_file}.json"
        
        if not Path(thread_file).exists():
            raise click.ClickException(f"Thread file not found: {thread_file}")
        
        # Load thread data
        with open(thread_file, "r", encoding="utf-8") as f:
            thread_data = json.load(f)
        
        thread = RedditThread(**thread_data)
        
        # Display thread
        display_thread(thread, highlight_user=user)
        
    except Exception as e:
        click.echo(f"❌ Failed: {e}")


def find_relevant_comments(thread: RedditThread, highlight_user: str) -> List:
    """Find comments that are relevant to the highlight_user's conversation.
    
    Returns comments that are:
    1. From the highlight_user
    2. Ancestors (parent comments) of the highlight_user's comments
    """
    relevant_comment_ids = set()
    user_comments = [c for c in thread.comments if c.author == highlight_user]
    
    # Add all user comments
    for comment in user_comments:
        relevant_comment_ids.add(comment.id)
    
    # For each user comment, walk up the parent chain to find ancestors
    for comment in user_comments:
        current_parent_id = comment.parent_id
        
        while current_parent_id:
            # Remove the prefix (t1_ for comments, t3_ for submissions)
            if current_parent_id.startswith('t1_'):
                parent_id = current_parent_id[3:]  # Remove 't1_' prefix
                # Find the parent comment
                parent_comment = next((c for c in thread.comments if c.id == parent_id), None)
                if parent_comment:
                    relevant_comment_ids.add(parent_comment.id)
                    current_parent_id = parent_comment.parent_id
                else:
                    break
            elif current_parent_id.startswith('t3_'):
                # This is a reference to the submission itself, stop here
                break
            else:
                break
    
    # Return filtered comments
    relevant_comments = [c for c in thread.comments if c.id in relevant_comment_ids]
    return relevant_comments


def display_thread(thread: RedditThread, highlight_user: str = "trnka"):
    """Display thread in a readable format, showing only relevant conversation."""
    submission = thread.submission
    
    # Header
    click.echo(f"Post: {submission.title}")
    click.echo(f"Subreddit: r/{submission.subreddit}")
    click.echo(f"Date: {submission.timestamp[:10]}")
    click.echo(f"URL: https://reddit.com{submission.permalink}")
    click.echo()
    
    # Original post
    click.echo(f"# {submission.author or '[deleted]'} ({submission.timestamp})")
    if submission.selftext:
        click.echo(submission.selftext)
    else:
        click.echo(f"[Link post: {submission.url}]")
    click.echo()
    click.echo()
    
    # Get relevant comments
    relevant_comments = find_relevant_comments(thread, highlight_user)
    
    if relevant_comments:
        # Sort by creation time
        sorted_comments = sorted(relevant_comments, key=lambda c: c.created_utc)
        
        for comment in sorted_comments:
            if comment.author is None:
                continue  # Skip deleted comments
                
            click.echo(f"# {comment.author} ({comment.timestamp})")
            click.echo(comment.body)
            click.echo()
            click.echo()
    else:
        click.echo("No relevant conversation found.")
        click.echo()
        click.echo()
    
    # Stats
    user_comment_count = len([c for c in thread.comments if c.author == highlight_user])
    total_displayed = len(relevant_comments)
    click.echo("---")
    click.echo(f"Thread Stats: {len(thread.comments)} total comments, {user_comment_count} by {highlight_user}, {total_displayed} displayed")

