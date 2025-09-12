# Reddit Data Pipeline Design

## Overview

A multi-stage ETL pipeline for extracting, enriching, and processing Reddit comments for FAQ generation. The goal is to create a flexible system that allows local experimentation with different data processing approaches.

## Goals

- Extract user comments from multiple subreddits
- Enrich comments with conversational context 
- Support experimentation with different processing strategies
- Build structured data suitable for summarization and FAQ generation

## Pipeline Architecture

```
Stage 1: Raw Extraction
download-user-comments → data/reddit/{username}_{subreddits}_{timestamp}.json

Stage 2: Context Enrichment  
enrich-reddit-comments → data/reddit/{username}_{subreddits}_{timestamp}_enriched.json

Stage 3: Processing/Summarization (Future)
process-reddit-data → final FAQ content
```

## Stage 1: Raw Comment Extraction

### Command: `download-user-comments`

**Purpose**: Extract all direct comments from a specified user across multiple subreddits.

**Parameters**:
- `--username`: Reddit username (default: "trnka")
- `--subreddits`: Comma-separated list of subreddit names (default: "mlquestions")
- `--limit`: Maximum total comments across all subreddits (default: 50)
- `--output-dir`: Output directory (default: "data")

**Output Format**: Single JSON file containing all comments from all specified subreddits.

**Data Structure**:
```json
[
  {
    "id": "comment_id",
    "text": "comment body text",
    "timestamp": "2025-09-12T10:30:00",
    "permalink": "https://reddit.com/...",
    "score": 5,
    "subreddit": "MLQuestions", 
    "post_title": "How to improve model accuracy?",
    "post_url": "https://reddit.com/r/MLQuestions/...",
    "post_id": "post_id"
  }
]
```

**File Naming**: `{username}_{subreddit1,subreddit2}_{timestamp}.json`

## Stage 2: Context Enrichment

### Command: `enrich-reddit-comments`

**Purpose**: Expand raw comments with conversational context to create coherent discussion threads.

**Input**: JSON file from Stage 1
**Output**: Enriched JSON file with conversation contexts

### Conversation Types & Strategies

#### Type 1: Simple Q&A
- **Pattern**: OP asks question → User responds
- **Context**: Just the original post + user's response
- **Processing**: Minimal - treat as standalone Q&A pair

#### Type 2: Extended Discussion
- **Pattern**: OP ↔ User back-and-forth conversation
- **Context**: Full conversation thread in chronological order
- **Processing**: Treat as chat/dialogue format

#### Type 3: Multi-part Response
- **Pattern**: User posts multiple comments in sequence (due to length limits)
- **Context**: All sequential comments from user in response to same trigger
- **Processing**: Concatenate into single logical response

#### Type 4: Complex Thread (Future)
- **Pattern**: Multiple participants, branching discussions
- **Context**: TBD - may need thread tree analysis
- **Processing**: Advanced threading logic

### Enriched Data Structure

```json
[
  {
    "conversation_id": "unique_id",
    "conversation_type": "simple_qa|extended_discussion|multi_part|complex",
    "original_post": {
      "id": "post_id",
      "title": "post title",
      "text": "post body",
      "url": "post_url",
      "author": "op_username",
      "timestamp": "timestamp"
    },
    "comments": [
      {
        "id": "comment_id",
        "text": "comment text",
        "author": "comment_author",
        "timestamp": "timestamp", 
        "score": 5,
        "is_user_comment": true,
        "parent_id": "parent_comment_id",
        "permalink": "comment_permalink"
      }
    ],
    "metadata": {
      "subreddit": "MLQuestions",
      "total_comments": 3,
      "user_comment_count": 2,
      "conversation_duration_hours": 2.5
    }
  }
]
```

## Implementation Strategy

### Phase 1: Update Existing Command
1. Rename `download-reddit-comments` → `download-user-comments`
2. Modify to accept multiple subreddits
3. Update file naming convention
4. Ensure single output file with all comments

### Phase 2: Add Enrichment Command
1. Create `enrich-reddit-comments` command
2. Implement conversation detection algorithms
3. Start with simple Q&A and multi-part response detection
4. Add extended discussion detection

### Phase 3: Advanced Features (Future)
1. Complex thread analysis
2. Content summarization integration
3. FAQ generation workflows
4. Quality scoring and filtering

## Technical Considerations

### Rate Limiting
- Respect Reddit API rate limits
- Add delays between requests
- Handle API errors gracefully

### Data Quality
- Handle deleted/removed comments
- Deal with empty or very short comments
- Manage private/inaccessible content

### Scalability
- Support incremental updates
- Allow resuming interrupted downloads
- Efficient storage for large datasets

### Configuration
- Support multiple user profiles
- Configurable conversation detection rules
- Flexible output formats

## File Organization

```
data/reddit/
├── raw/
│   ├── trnka_mlquestions_2025-09-12_143022.json
│   └── trnka_mlquestions,datascience_2025-09-12_150000.json
├── enriched/
│   ├── trnka_mlquestions_2025-09-12_143022_enriched.json
│   └── trnka_mlquestions,datascience_2025-09-12_150000_enriched.json
└── processed/ (future)
    └── faq_content.json
```

## Success Metrics

- **Coverage**: Capture all relevant user comments from target subreddits
- **Context**: Successfully identify and group related comments into conversations
- **Quality**: Maintain comment relationships and chronological order
- **Flexibility**: Support experimentation with different processing approaches
- **Reliability**: Handle API limitations and edge cases gracefully

## Future Extensions

- Support for multiple users
- Cross-platform integration (Twitter, Discord, etc.)
- Real-time monitoring and updates
- Machine learning for conversation classification
- Integration with LLMs for content analysis
