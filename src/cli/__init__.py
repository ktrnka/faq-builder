"""Main CLI entry point for FAQ Builder."""

import logging

import click

from .reddit import reddit
from .youtube import youtube

# Configure logging for the entire CLI application
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:%(name)s:%(message)s'
)


@click.group()
def cli():
    """FAQ Builder - Build FAQs from various sources."""
    pass


# Add command groups
cli.add_command(youtube)
cli.add_command(reddit)


__all__ = ["cli", "youtube", "reddit"]
