"""OpenAI client initialization and cost calculation utilities."""

import logging
import os

from dotenv import load_dotenv
from openai import OpenAI


def get_openai_client() -> OpenAI:
    """Initialize OpenAI client with API key from environment."""
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    return OpenAI(api_key=api_key)


def estimate_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    """Estimate cost based on OpenAI pricing.
    
    Args:
        model: OpenAI model name
        prompt_tokens: Number of input tokens
        completion_tokens: Number of output tokens
        
    Returns:
        Estimated cost in USD
    """
    # Pricing as of Sept 2025 (update as needed)
    pricing = {
        "gpt-4-turbo": {"input": 0.01000, "output": 0.03000},  # per 1K tokens
        "gpt-4": {"input": 0.03000, "output": 0.06000},
        "gpt-4o-mini": {"input": 0.000150, "output": 0.000600},
        "gpt-4o": {"input": 0.005000, "output": 0.015000},
    }
    
    if model not in pricing:
        logging.warning(f"Unknown model '{model}' for cost estimation")
        return 0.0
    
    input_cost = (prompt_tokens / 1000) * pricing[model]["input"]
    output_cost = (completion_tokens / 1000) * pricing[model]["output"]
    
    return input_cost + output_cost
