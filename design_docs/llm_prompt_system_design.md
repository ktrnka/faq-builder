# LLM/Prompt System Design

## Overview

A class-based system for managing OpenAI API interactions with structured prompts, Pydantic output models, and integrated cost tracking. The system provides a consistent interface for all LLM operations across the FAQ builder pipeline.

## Goals

- Standardize OpenAI API interactions across the project
- Provide type-safe prompt definitions with Pydantic output models
- Enable cost tracking and usage monitoring through logging
- Support rapid prompt iteration and experimentation
- Maintain clean separation between prompt logic and CLI commands

## Architecture

### Core Components

```
src/
├── llm/
│   ├── __init__.py
│   ├── client.py          # OpenAI client initialization and utilities
│   ├── base.py           # Base prompt class and common functionality
│   └── prompts/
│       ├── __init__.py
│       ├── transcript_cleaning.py    # YouTube transcript cleaning prompt
│       └── reddit_enrichment.py     # Reddit comment enrichment prompt (future)
```

### Component Responsibilities

- **`client.py`**: OpenAI client setup, environment variable loading, cost calculation utilities
- **`base.py`**: Abstract base class for all prompts with common functionality
- **`prompts/`**: Specific prompt implementations inheriting from base class

## Base Prompt Class Design

### Key Features

- **Abstract base class** with generic Pydantic output types
- **Model configuration**: Default `gpt-4-turbo`, overridable per prompt
- **Input formatting**: Abstract method for data preprocessing within each prompt class
- **Dual execution methods**:
  - `execute_raw()`: Returns full OpenAI response (for debugging/analysis)
  - `execute()`: Returns parsed Pydantic model (for normal usage)
- **Automatic cost tracking**: Logs token usage and estimated costs

### Prompt Implementation Pattern

Each prompt class inherits from `BasePrompt` and defines:
- `model`: OpenAI model to use
- `system_prompt`: Instructions for the AI
- `output_model`: Pydantic model for structured output
- `format_input()`: Method to convert input data to prompt text

## Data Models

### YouTube Transcript Cleaning Output

- **CleanedTranscript**: Main container with metadata and chapters
- **Chapter**: Topical sections with timing and type classification
- **CleanedSegment**: Individual speaker turns within chapters

### Key Design Decisions

- **Chapter-level timing**: Only track start_time for chapters, not individual segments
- **Speaker classification**: Host/Student/Other for office hours context
- **Type safety**: All outputs use Pydantic models for validation
- **Cost optimization**: Minimal output structure to reduce token usage

## Implementation Strategy

### Phase 1: Core Infrastructure
1. Create environment setup and OpenAI client initialization
2. Implement abstract base class with cost tracking
3. Add basic error handling and logging

### Phase 2: First Prompt Implementation
1. Create transcript cleaning prompt with updated data models
2. Test on partial transcripts for cost-effective iteration
3. Integrate with CLI for end-to-end workflow

### Phase 3: Extension & Refinement
1. Add additional prompts for Reddit processing
2. Optimize based on usage patterns and cost analysis
3. Add advanced features as needed

## Technical Considerations

### Environment & Dependencies
- Standard `OPENAI_API_KEY` environment variable
- OpenAI Python client library integration
- Python logging framework for cost tracking

### Cost Management
- Automatic token counting and cost estimation
- Development workflow supports partial transcript testing
- Cost logging for usage analysis and optimization

### Error Handling
- OpenAI API errors (rate limits, invalid responses)
- Pydantic validation errors for malformed outputs
- Environment configuration errors

### Future Extensions
- Retry logic for reliability
- Prompt versioning for reproducibility
- Batch processing optimization
- Advanced cost tracking and analysis
