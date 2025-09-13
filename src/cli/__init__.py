"""Main CLI entry point for FAQ Builder."""

import click

from .reddit import reddit
from .youtube import youtube


@click.group()
def cli():
    """FAQ Builder - Build FAQs from various sources."""
    pass


# Add command groups
cli.add_command(youtube)
cli.add_command(reddit)


__all__ = ["cli", "youtube", "reddit"]
