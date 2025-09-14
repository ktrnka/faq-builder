# Reddit Pipeline

## Status: ✅ Fully Implemented

Complete Reddit pipeline with 3 CLI commands, successfully processing 131 threads.

**Usage**: `uv run faq-builder reddit --help`

## Design Goals

- **Extract user comments** from multiple subreddits efficiently
- **Enrich comments with conversational context** to understand thread discussions  
- **Support experimentation** with different processing strategies
- **Build structured data** suitable for summarization and FAQ generation
- **Create flexible system** that allows local experimentation with data processing approaches
- **Mirror YouTube pipeline structure** for consistency and future integration

## Commands

### 1. Download User Comments
```bash
uv run faq-builder reddit download-user-comments --username trnka --subreddits mlquestions,machinelearning
```
- Fetches user comments from specified subreddits
- Output: `data/reddit/{username}_{subreddits}_comments_{timestamp}.json`

### 2. Enrich Threads  
```bash
uv run faq-builder reddit enrich-threads data/reddit/trnka_*.json
```
- Fetches full thread context for each comment
- Output: Individual `data/reddit/threads/{post_id}.json` files

### 3. Show Thread
```bash
uv run faq-builder reddit show-thread 10qqyhz --user trnka
```
- Displays thread in readable conversation format
- Highlights specified user's contributions

## Pipeline Flow

```
User Comments → Thread Enrichment → Readable Display
     ↓                ↓                    ↓
   Raw JSON      Individual Files    Conversation
```

## Data Structure

### Thread File (`{post_id}.json`)
```json
{
  "submission": {
    "id": "10qqyhz",
    "title": "Question about neural networks",
    "selftext": "Post content...",
    "author": "learning_to_meditate",
    "created_utc": 1675209104,
    "subreddit": "MLQuestions"
  },
  "comments": [
    {
      "id": "j8z9abc",
      "author": "trnka",
      "body": "Great question! Here are some techniques...",
      "created_utc": 1675258930,
      "parent_id": "t3_10qqyhz",
      "replies": [...]
    }
  ]
}
```

## Display Format

```
Post: [Question about neural networks]
Subreddit: r/MLQuestions  
Date: 2023-02-01
URL: https://reddit.com/r/MLQuestions/comments/10qqyhz/...

# learning_to_meditate (2023-02-01T03:11:44)
Hi, I'm currently going through a learning journey...

# trnka (2023-02-01T15:22:10)
Great question! Here are some additional techniques...

---
Thread Stats: 4 messages, 2 by trnka
```

## File Organization

```
data/reddit/
├── trnka_mlquestions,machinelearning_comments_2025-09-12_152303.json
└── threads/
    ├── 10oazg7.json
    ├── 10qqyhz.json  
    └── ... (131 total)
```

## Technical Details

- **API**: Uses PRAW (Python Reddit API Wrapper)
- **Rate Limiting**: Respects Reddit API limits with delays between requests
- **Data Quality**: Handles deleted comments, private content, and edge cases
- **Testing**: Comprehensive test suite with 6 tests covering models and core logic
- **Scalability**: Individual thread files support efficient processing
- **Configuration**: Flexible subreddit lists, user profiles, and output formats

### Design Considerations

**Rate Limiting**
- Respect Reddit API rate limits
- Add delays between requests  
- Handle API errors gracefully

**Data Quality**
- Handle deleted/removed comments
- Deal with empty or very short comments
- Manage private/inaccessible content

**Flexibility**
- Support multiple user profiles
- Configurable conversation detection
- Individual thread files for easy experimentation

## Future Work

- FAQ generation from thread conversations
- Topic linking with YouTube pipeline
- Content summarization integration