"""Basic tests for the FAQ builder project structure."""


def test_project_structure():
    """Test that main project modules can be imported."""
    import src
    
    assert src is not None


def test_main_modules():
    """Test that main modules exist and can be imported."""
    from src import cli, llm
    
    assert cli is not None
    assert llm is not None
