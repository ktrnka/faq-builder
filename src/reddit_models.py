"""Pydantic models for Reddit data serialization."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class RedditComment(BaseModel):
    """Reddit comment model based on PRAW Comment."""
    
    id: str
    author: Optional[str] = None  # Can be None for deleted users
    body: str
    body_html: Optional[str] = None
    created_utc: float
    score: int
    ups: int
    downs: int
    permalink: str
    parent_id: Optional[str] = None  # Full name (e.g., "t1_comment_id" or "t3_post_id")
    depth: int = 0
    is_submitter: bool = False
    stickied: bool = False
    edited: bool = False
    distinguished: Optional[str] = None  # "moderator", "admin", or None
    
    # Derived fields for convenience
    timestamp: str = Field(description="ISO formatted timestamp derived from created_utc")
    
    @classmethod
    def from_praw_comment(cls, comment) -> "RedditComment":
        """Create RedditComment from PRAW comment object."""
        return cls(
            id=comment.id,
            author=comment.author.name if comment.author else None,
            body=comment.body,
            body_html=getattr(comment, 'body_html', None),
            created_utc=comment.created_utc,
            score=comment.score,
            ups=comment.ups,
            downs=comment.downs,
            permalink=comment.permalink,
            parent_id=comment.parent_id,
            depth=getattr(comment, 'depth', 0),
            is_submitter=comment.is_submitter,
            stickied=comment.stickied,
            edited=bool(comment.edited),
            distinguished=comment.distinguished,
            timestamp=datetime.fromtimestamp(comment.created_utc).isoformat()
        )


class RedditSubmission(BaseModel):
    """Reddit submission model based on PRAW Submission."""
    
    id: str
    title: str
    author: Optional[str] = None  # Can be None for deleted users
    selftext: str = ""  # Body text for self posts
    selftext_html: Optional[str] = None
    url: str
    permalink: str
    subreddit: str  # Display name of subreddit
    created_utc: float
    score: int
    ups: int
    downs: int
    upvote_ratio: float
    num_comments: int
    is_self: bool
    over_18: bool = False
    spoiler: bool = False
    stickied: bool = False
    locked: bool = False
    archived: bool = False
    distinguished: Optional[str] = None
    link_flair_text: Optional[str] = None
    
    # Derived fields for convenience
    timestamp: str = Field(description="ISO formatted timestamp derived from created_utc")
    
    @classmethod
    def from_praw_submission(cls, submission) -> "RedditSubmission":
        """Create RedditSubmission from PRAW submission object."""
        return cls(
            id=submission.id,
            title=submission.title,
            author=submission.author.name if submission.author else None,
            selftext=submission.selftext or "",
            selftext_html=getattr(submission, 'selftext_html', None),
            url=submission.url,
            permalink=submission.permalink,
            subreddit=submission.subreddit.display_name,
            created_utc=submission.created_utc,
            score=submission.score,
            ups=submission.ups,
            downs=submission.downs,
            upvote_ratio=submission.upvote_ratio,
            num_comments=submission.num_comments,
            is_self=submission.is_self,
            over_18=submission.over_18,
            spoiler=submission.spoiler,
            stickied=submission.stickied,
            locked=submission.locked,
            archived=submission.archived,
            distinguished=submission.distinguished,
            link_flair_text=submission.link_flair_text,
            timestamp=datetime.fromtimestamp(submission.created_utc).isoformat()
        )


class RedditThread(BaseModel):
    """Complete Reddit thread with submission and comments."""
    
    submission: RedditSubmission
    comments: List[RedditComment]
    total_comments: int
    fetched_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    
    @classmethod
    def from_praw_data(cls, submission, comments: List) -> "RedditThread":
        """Create RedditThread from PRAW submission and comment list."""
        return cls(
            submission=RedditSubmission.from_praw_submission(submission),
            comments=[RedditComment.from_praw_comment(comment) for comment in comments],
            total_comments=len(comments),
            fetched_at=datetime.now().isoformat()
        )


class UserComment(BaseModel):
    """User comment from existing JSON data (input format)."""
    
    id: str
    text: str
    timestamp: str
    permalink: str
    score: int
    subreddit: str
    post_title: str
    post_url: str
    post_id: str