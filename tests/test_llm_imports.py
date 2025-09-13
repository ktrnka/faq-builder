"""Test imports for the LLM module."""


def test_llm_base_imports():
    """Test that core LLM components can be imported."""
    from src.llm import BasePrompt
    
    assert BasePrompt is not None


def test_llm_model_imports():
    """Test that LLM models can be imported."""
    from src.llm.prompts.transcript_cleaning import Chapter, CleanedSegment, CleanedTranscript
    
    assert CleanedTranscript is not None
    assert Chapter is not None
    assert CleanedSegment is not None


def test_prompt_imports():
    """Test that prompt classes can be imported."""
    from src.llm.prompts import TranscriptCleaningPrompt
    assert TranscriptCleaningPrompt is not None


def test_prompt_structure():
    """Test that the prompt has expected structure."""
    from src.llm.prompts.transcript_cleaning import CleanedTranscript, TranscriptCleaningPrompt

    assert CleanedTranscript is not None
    
    # Check class attributes
    assert len(TranscriptCleaningPrompt.system_prompt) > 100  # Should have substantial content


def test_cost_estimation():
    """Test cost estimation function."""
    from src.llm import estimate_cost
    
    # Test with known model
    cost = estimate_cost("gpt-4-turbo", 1000, 500)
    assert cost > 0
    assert isinstance(cost, float)
    
    # Test with unknown model (should return 0)
    cost_unknown = estimate_cost("unknown-model", 1000, 500)
    assert cost_unknown == 0.0
