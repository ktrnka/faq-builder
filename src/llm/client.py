"""OpenAI client initialization and cost calculation utilities."""

import logging
import os

from dotenv import load_dotenv
from openai import OpenAI
from openai.types import CompletionUsage


def get_openai_client() -> OpenAI:
    """Initialize OpenAI client with API key from environment."""
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    return OpenAI(api_key=api_key)


def estimate_cost(model: str, usage: CompletionUsage) -> float:
    """Estimate cost based on OpenAI pricing.
        
    Returns:
        Estimated cost in USD
    """
    # Pricing as of September 2025 (per 1K tokens)
    # Source: https://platform.openai.com/docs/pricing
    pricing_per_million = {
        # GPT-4.1 models (assuming no cached tokens)
        "gpt-4.1-nano": {"input": 0.10, "cached_input": 0.025, "output": 0.40},
        "gpt-4.1-mini": {"input": 0.40, "cached_input": 0.10, "output": 1.60},
        "gpt-4.1": {"input": 2.00, "cached_input": 0.50, "output": 8.00},
    }

    if model not in pricing_per_million:
        logging.warning(f"Unknown model '{model}' for cost estimation")
        return 0.0
    
    cached_input_tokens = 0
    if usage.prompt_tokens_details:
        cached_input_tokens = usage.prompt_tokens_details.cached_tokens or 0

    uncached_input_tokens = usage.prompt_tokens - cached_input_tokens

    uncached_input_cost = (uncached_input_tokens / 1e6) * pricing_per_million[model]["input"]
    cached_input_cost = (cached_input_tokens / 1e6) * pricing_per_million[model]["cached_input"]
    output_cost = (usage.completion_tokens / 1e6) * pricing_per_million[model]["output"]

    return uncached_input_cost + cached_input_cost + output_cost
