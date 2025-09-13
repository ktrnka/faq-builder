"""Abstract base class for all OpenAI prompts."""

import logging
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from openai import OpenAI
from openai.types.chat import ChatCompletion
from pydantic import BaseModel

from .client import estimate_cost

T = TypeVar('T', bound=BaseModel)


class BasePrompt(ABC, Generic[T]):
    """Abstract base class for all OpenAI prompts.
    
    Subclasses must define:
    - model: OpenAI model to use
    - system_prompt: Instructions for the AI
    - output_model: Pydantic model for structured output
    - format_input(): Method to convert input data to prompt text
    """
    
    # Class attributes to be defined by subclasses
    model: str = "gpt-4-turbo"
    system_prompt: str
    output_model: type[T]
    
    def __init__(self, client: OpenAI):
        self.client = client
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    def format_input(self, **kwargs) -> str:
        """Convert input data into the user message string.
        
        Args:
            **kwargs: Input data specific to each prompt type
            
        Returns:
            Formatted string to send as user message
        """
        pass
    
    def execute_raw(self, **kwargs) -> ChatCompletion:
        """Execute prompt and return raw OpenAI response.
        
        Args:
            **kwargs: Input data for format_input()
            
        Returns:
            Raw ChatCompletion response from OpenAI
        """
        user_message = self.format_input(**kwargs)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_message}
            ],
            response_format={"type": "json_object"}  # For Pydantic parsing
        )
        
        # Log usage and cost
        usage = response.usage
        if usage:
            cost = estimate_cost(self.model, usage.prompt_tokens, usage.completion_tokens)
            
            self.logger.info(
                f"LLM call completed - Model: {self.model}, "
                f"Tokens: {usage.prompt_tokens}+{usage.completion_tokens}, "
                f"Cost: ${cost:.4f}"
            )
        
        return response
    
    def execute(self, **kwargs) -> T:
        """Execute prompt and return parsed Pydantic model.
        
        Args:
            **kwargs: Input data for format_input()
            
        Returns:
            Parsed output using the defined output_model
        """
        response = self.execute_raw(**kwargs)
        
        # Parse response content using Pydantic model
        content = response.choices[0].message.content
        if not content:
            raise ValueError("Empty response from OpenAI")
            
        return self.output_model.model_validate_json(content)
