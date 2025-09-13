# YouTube Data Pipeline Design

## Overview

A multi-stage ETL pipeline for extracting, cleaning, segmenting, and processing YouTube transcripts from office hours sessions for FAQ generation. The pipeline focuses on Keith's weekly officExample makefile rule:
```makefile
data/youtube/processed/%.json: data/youtube/raw/%.json
    uv run faq-builder youtube clean-and-segment-transcript $< --output $@
```

## Next Implementation Steps

### Immediate Priority: Prompt Development
1. **Iterative Prompt Engineering**: Develop and test prompts for combined cleaning + segmentation
2. **Sample Processing**: Use `show-transcript` output to manually create example of desired output
3. **Validation Approach**: Compare LLM output against manual examples
4. **Cost Estimation**: Track token usage and costs during development

### Prompt Design Considerations
- **Input Format**: Use output from `show-transcript` as consistent input format
- **Combined Operations**: Single prompt that handles both cleaning and segmentation
- **Speaker Attribution**: Leverage context clues to identify Keith vs. students/participants
- **Topic Boundaries**: Use natural conversation flow and question patterns to identify segments
- **Technical Accuracy**: Preserve ML/AI terminology and technical discussions accurately

### Development Workflow

**Cost-Effective Iteration Strategy:**
1. Run `show-transcript` on sample video to get human-readable format
2. **Use partial transcripts for iteration**: Take first ~300 lines (`head -300`) for prompt development
3. Manually create "gold standard" cleaned and segmented version for the partial transcript
4. Develop prompt to reproduce this output on the partial transcript
5. **Iterate rapidly on small samples**: Test and refine prompt using partial transcripts (~$0.05-0.10 per test vs ~$0.50-1.00 for full video)
6. Once prompt quality is good on partial transcripts, test on full video
7. Validate generalization across different videos
8. Implement as `clean-and-segment-transcript` command

**Rationale for Partial Transcript Iteration:**
- 300 lines ≈ 1-2k tokens vs 22-24k tokens for full transcript
- ~10-20x cost reduction during prompt development phase
- Faster iteration cycles for prompt refinement
- Can test multiple prompt variations economically
- Transition to full processing once confident in prompt quality

## Success Metrics

- **Cleaning Quality**: Improved readability and technical accuracy compared to raw transcripts
- **Segmentation Accuracy**: Segments align with natural topic boundaries and Q&A sessions
- **Processing Speed**: Individual video processing completes within reasonable time limits
- **Cost Efficiency**: API usage optimized for quality vs. cost trade-off
- **Pipeline Reliability**: Stages complete successfully with clear error handling

## Future Extensionsdesigned to be extensible to other speakers and content types.

## Goals

- Extract transcripts from YouTube videos (primarily Keith's office hours)
- Clean and improve auto-generated transcripts using LLMs
- Segment long-form content into topical sections
- Support experimentation with different processing strategies
- Build structured data suitable for FAQ generation and blog post creation

## Pipeline Architecture

**Updated Architecture (based on token analysis):**

```
Stage 1: Video Discovery & Transcript Extraction (✅ Implemented)
list-videos → download-transcript → data/youtube/raw/{date}_{video_id}.json

Stage 1.5: Analysis & Planning (✅ Implemented)  
show-transcript, count-tokens → human review and model selection

Stage 2: Combined Cleaning & Segmentation (Current Focus)
clean-and-segment-transcript → data/youtube/processed/{date}_{video_id}_processed.json

Stage 3: Processing/FAQ Generation (Future)
process-youtube-data → final FAQ/blog content
```

**Rationale for Combined Stage 2:**
- Token analysis shows videos are 22-24k tokens (too large for multiple API calls)
- Combining cleaning + segmentation reduces API costs and maintains context
- Single LLM pass can better understand conversation flow for segmentation

## Stage 1: Video Discovery & Transcript Extraction

### Current Implementation
- **Command**: `list-videos` - Discovers videos in playlists by search term
- **Command**: `download-transcript` - Extracts raw transcripts with metadata

**Current Output Format**: 
```json
{
  "metadata": {
    "kind": "youtube#video",
    "id": "video_id",
    "snippet": {
      "publishedAt": "timestamp",
      "title": "video title",
      "description": "video description",
      "channelTitle": "Joy of Coding"
    },
    "contentDetails": {"duration": "PT1H11M9S"},
    "statistics": {"viewCount": "0", "likeCount": "0"}
  },
  "transcript": {
    "video_id": "video_id",
    "language": "English (auto-generated)",
    "language_code": "en", 
    "is_generated": true,
    "snippets": [
      {
        "text": "transcript text",
        "start": 5.52,
        "duration": 4.159
      }
    ]
  }
}
```

**File Naming**: `{date}_{video_id}.json` (e.g., `2025-09-06__-tRDk3P7bg.json`)

### Analysis Commands (Implemented)
- **Command**: `show-transcript` - Displays human-readable formatted transcript with timestamps
- **Command**: `count-tokens` - Analyzes token count and model compatibility

#### Token Analysis Results
Real transcript analysis reveals that office hours videos are significantly larger than initially anticipated:

- **Typical video length**: ~22-24k tokens for 1-hour sessions
- **Character-to-token ratio**: ~3.0 characters per token
- **GitHub models compatibility**: ❌ Not viable (2k input limit vs 22k+ tokens needed)
- **GPT-4 Turbo compatibility**: ✅ Viable (128k context window)

**Implications**: 
- GitHub's free models are not suitable for full transcript processing
- Must use OpenAI API directly with GPT-4 Turbo or similar large-context models
- Cost considerations become important for batch processing
- May need chunking strategies for very long videos (2+ hours)

### Future Enhancements
- Support multiple playlists beyond "TechJoy Academy Replays"
- Batch processing capabilities for pipeline efficiency
- Resume capability for interrupted downloads

## Stage 2: Transcript Cleaning & Segmentation (Combined Approach)

### Updated Strategy
Based on token analysis, we're revising the approach to combine cleaning and segmentation into a single stage to optimize for the large context requirements and reduce API costs.

### Command: `clean-and-segment-transcript`

**Purpose**: Improve auto-generated transcripts using LLMs to create clean, readable text suitable for downstream processing.

**Input**: Raw transcript JSON from Stage 1
**Output**: Cleaned transcript with speaker attribution and corrected text

### Cleaning Operations

#### Text Improvements
- **Remove filler words**: "um", "uh", "like", "you know", etc.
- **Fix speech repairs**: Remove false starts and self-corrections
- **Correct auto-transcript errors**: Leverage LLM understanding of technical terminology
- **Normalize punctuation**: Add proper sentence boundaries and capitalization
- **Fix technical terms**: Ensure ML/AI terminology is correctly transcribed

#### Speaker Attribution
- **Identify speakers**: Distinguish between "Keith" and "Student"/"Participant"
- **Handle unknown speakers**: Use generic labels when identification isn't possible
- **Context-based detection**: Use speech patterns and content cues for attribution

## Stage 3: Content Segmentation

### Command: `segment-transcript`

**Purpose**: Break long-form office hours into topical segments that align with questions, explanations, or demonstrations.

**Input**: Cleaned transcript JSON from Stage 2
**Output**: Segmented content with topic labels and categories

### Segmentation Strategies

#### Automatic Topic Detection
- **LLM-based analysis**: Use context understanding to identify topic boundaries
- **Question identification**: Detect Q&A patterns and student questions
- **Content type recognition**: Distinguish between explanations, live coding, discussions

#### Segment Types
- **Q&A Sessions**: Student question followed by Keith's response
- **Explanations**: Keith explaining concepts or techniques
- **Live Coding**: Hands-on programming demonstrations
- **Discussions**: General conversation or exploratory topics
- **Administrative**: Session setup, announcements, wrap-up

## Implementation Strategy

### Phase 1: Analysis & Planning (✅ Completed)
1. ✅ Create `show-transcript` command for human-readable output
2. ✅ Create `count-tokens` command for model compatibility analysis
3. ✅ Analyze real transcript data to understand scale and constraints
4. ✅ Determine that GitHub models are not viable, OpenAI API required

### Phase 2: Combined Cleaning & Segmentation (Current Priority)
1. Create `clean-and-segment-transcript` command
2. Implement single-pass LLM processing for both cleaning and segmentation
3. Develop specialized prompts for combined operations
4. Test on individual videos to iterate on prompt quality
5. Add speaker attribution and topic detection

### Phase 3: Batch Processing & Cost Optimization
1. Add batch processing capabilities for multiple videos
2. Implement chunking strategies for very long videos (2+ hours)
3. Add retry logic and progress tracking for expensive LLM calls
4. Create makefile-compatible workflows

### Phase 4: Integration & FAQ Generation
1. Integrate with Reddit pipeline outputs
2. Develop cross-platform topic identification
3. Create FAQ generation from combined YouTube + Reddit data

## Technical Considerations

### LLM Integration (Updated)
- **Model Selection**: OpenAI GPT-4 Turbo (128k context) - GitHub models not viable
- **API Integration**: Use OpenAI Python library directly
- **Cost Management**: 
  - Single video processing during development (~$0.50-1.00 per video estimated)
  - Careful prompt engineering to maximize output quality per API call
  - Consider combining cleaning + segmentation to reduce API calls
- **Prompt Engineering**: Iterative development of prompts for both cleaning and segmentation
- **Error Handling**: Robust retry logic for expensive API calls
- **Rate Limiting**: Respect OpenAI rate limits during batch processing

### Context Window Management
- **Full Transcript Processing**: Leverage 128k context to process entire videos in single calls
- **Chunking Strategy**: For videos >100k tokens, implement overlap-based chunking
- **Prompt Overhead**: Reserve ~2-4k tokens for system prompts and instructions
- **Output Size**: Plan for cleaned output to be smaller than input (removed fillers, etc.)

### Data Quality
- **Confidence Scoring**: Track cleaning and segmentation confidence levels
- **Manual Review**: Support for human verification of processed content
- **Version Tracking**: Maintain provenance of processing steps and model versions

### Scalability  
- **Incremental Processing**: Only process new or updated content
- **Resumable Operations**: Handle interruptions in long-running batch jobs
- **Storage Efficiency**: Compress or archive intermediate processing files

### Pipeline Dependencies
- **Makefile Compatibility**: Structure file naming for easy dependency specification
- **Atomic Operations**: Each stage produces complete output or fails cleanly
- **Dependency Tracking**: Clear input/output relationships between stages

## File Organization

**Updated Structure (reflects combined processing):**

```
data/youtube/
├── raw/                    # Stage 1 output (✅ current implementation)
│   ├── 2025-09-06__-tRDk3P7bg.json
│   └── 2025-08-30_2FcOn-1IZY0.json
├── processed/              # Stage 2 output (combined cleaning + segmentation)
│   ├── 2025-09-06__-tRDk3P7bg_processed.json
│   └── 2025-08-30_2FcOn-1IZY0_processed.json
└── final/                  # Stage 3 output (FAQ/blog generation)
    ├── faq_content.json
    └── blog_drafts/
```

**Rationale for Simplified Structure:**
- Eliminates intermediate `cleaned/` and `segmented/` directories
- Single `processed/` output contains both cleaned text and segmentation
- Reduces complexity and file management overhead
- Better aligns with combined API processing approach

### Makefile-Friendly Naming Convention
- **Input dependency**: `data/youtube/raw/{date}_{video_id}.json`
- **Output target**: `data/youtube/processed/{date}_{video_id}_processed.json`
- **Base name**: `{date}_{video_id}` (consistent across all stages)

Example makefile rule:
```makefile
data/youtube/cleaned/%.json: data/youtube/raw/%.json
    uv run faq-builder clean-transcript $< --output $@
```

## Success Metrics

- **Cleaning Quality**: Improved readability and technical accuracy compared to raw transcripts
- **Segmentation Accuracy**: Segments align with natural topic boundaries and Q&A sessions
- **Processing Speed**: Individual video processing completes within reasonable time limits
- **Cost Efficiency**: LLM usage optimized for development and eventual batch processing
- **Pipeline Reliability**: Stages complete successfully with clear error handling

## Future Extensions

- **Multi-speaker Support**: Enhanced speaker identification for guest appearances
- **Cross-video Analysis**: Identify recurring topics and questions across sessions
- **Interactive Transcripts**: Link segments back to video timestamps for review
- **Content Recommendation**: Suggest related segments within and across videos
- **Quality Metrics**: Automatic assessment of segment quality and completeness
- **Export Formats**: Generate markdown, HTML, or other formats for different use cases

## Integration with Overall FAQ System

### Data Flow to FAQ Generation
1. **YouTube Pipeline**: Produces segmented office hours content
2. **Reddit Pipeline**: Produces enriched conversation threads  
3. **Cross-Platform Analysis**: Identify common themes and questions
4. **FAQ Synthesis**: Generate comprehensive answers using both data sources
5. **Blog Post Generation**: Create detailed technical content from combined insights

### Pydantic Models (Conceptual - Updated)
- `RawTranscript`: Stage 1 output structure (current implementation)
- `ProcessedTranscript`: Stage 2 output with combined cleaning + segmentation
- `FAQContent`: Stage 3 output ready for FAQ/blog generation
- `CrossPlatformTopic`: Combined YouTube + Reddit insights on specific topics
