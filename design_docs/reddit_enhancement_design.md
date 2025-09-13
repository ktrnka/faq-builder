# Reddit Pipeline Enhancement Design

## Overview
Extend the existing Reddit comment download system to support thread extraction and readable formatting, similar to the YouTube pipeline.

## Current Implementation Status
- ✅ `reddit download-user-comments` - Downloads user comments from specified subreddits
- ✅ Saves to `data/reddit/{username}_{subreddits}_comments_{timestamp}.json`

## Target Enhancement: Thread Interaction Display

### New Command: `reddit show-thread`
**Purpose**: Extract and display a specific Reddit conversation thread where Keith interacted with an OP.

**Usage Examples**:
```bash
# By Reddit post URL
uv run faq-builder reddit show-thread https://www.reddit.com/r/MachineLearning/comments/abc123/title/

# By post ID  
uv run faq-builder reddit show-thread abc123

# With specific user focus
uv run faq-builder reddit show-thread abc123 --user trnka
```

### Expected Output Format
```
Post: [Title from Reddit post]
Subreddit: r/MachineLearning
Date: 2025-05-15
URL: https://www.reddit.com/r/MachineLearning/comments/abc123/title/

## Original Post
[OP's question/content]

## Thread Conversation

**OP**: Follow-up question or clarification...

**trnka**: [Keith's response with technical advice]

**OP**: Thanks! One more question about X...

**trnka**: [Keith's detailed explanation]

---
Thread Stats: 4 messages, 2 by trnka
```

## Implementation Strategy

### Phase 1: Data Enhancement
1. Enhance Reddit download to capture thread context
2. Store post titles, OP usernames, and thread relationships
3. Index comments by post ID for fast thread reconstruction

### Phase 2: Thread Extraction
1. Add Reddit API calls to fetch full post context
2. Build thread reconstruction logic (reply chains)
3. Filter for threads where Keith participated

### Phase 3: Display Formatting
1. Create readable conversation format
2. Add speaker attribution (OP vs Keith vs Others)
3. Include post metadata and statistics

## Data Structure Enhancements

### Enhanced Comment Storage
```json
{
  "post_id": "abc123",
  "post_title": "Question about neural networks",
  "post_url": "https://reddit.com/r/ML/...",
  "op_username": "student_user",
  "thread_participants": ["trnka", "student_user", "other_user"],
  "comments": [
    {
      "id": "comment_id",
      "author": "trnka", 
      "text": "comment text",
      "parent_id": "parent_comment_id",
      "depth": 1,
      "timestamp": "2025-05-15T10:30:00Z"
    }
  ]
}
```

## Integration with YouTube Pipeline

### Future Cross-Platform Features
- **Topic Linking**: Connect Reddit discussions to related YouTube segments
- **FAQ Generation**: Combine YouTube explanations with Reddit Q&As
- **Content Discovery**: Find Reddit threads that reference YouTube topics

## Success Metrics
- **Thread Reconstruction**: Accurately rebuilds conversation flow
- **Context Preservation**: Maintains post context and participant clarity  
- **Readable Output**: Easy to follow conversation format
- **Discovery**: Efficiently finds Keith's meaningful interactions
