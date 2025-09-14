"""Tests for Reddit CLI functionality."""

def test_import():
    from src.cli.reddit import RedditComment, extract_unique_post_ids

    assert RedditComment is not None
    assert extract_unique_post_ids is not None

