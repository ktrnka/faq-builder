"""Test imports for CLI components."""


def test_cli_imports():
    """Test that CLI module can be imported."""
    from src import cli
    
    assert cli is not None


def test_cli_groups():
    """Test that CLI groups are properly configured."""
    from src.cli import reddit, youtube
    
    # Check that groups exist
    assert youtube is not None
    assert reddit is not None
    