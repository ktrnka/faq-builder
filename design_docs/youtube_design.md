# YouTube Data Pipeline Design

## Overview

A multi-stage ETL pipeline for extracting, cleaning, segmenting, and processing YouTube transcripts from office hours sessions for FAQ generation. The pipeline focuses on Keith's weekly office hours but is designed to be extensible to other speakers and content types.

## Goals

- Extract transcripts from YouTube videos (primarily Keith's office hours)
- Clean and improve auto-generated transcripts using LLMs
- Segment long-form content into topical sections
- Support experimentation with different processing strategies
- Build structured data suitable for FAQ generation and blog post creation

## Pipeline Architecture

```
Stage 1: Video Discovery & Transcript Extraction
list-videos → download-transcript → data/youtube/raw/{date}_{video_id}.json

Stage 2: Transcript Cleaning
clean-transcript → data/youtube/cleaned/{date}_{video_id}_cleaned.json

Stage 3: Content Segmentation
segment-transcript → data/youtube/segmented/{date}_{video_id}_segmented.json

Stage 4: Processing/FAQ Generation (Future)
process-youtube-data → final FAQ/blog content
```

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

### Future Enhancements
- Batch processing capabilities for pipeline efficiency

## Stage 2: Transcript Cleaning

### Command: `clean-transcript`

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

### Phase 1: Transcript Cleaning (Priority)
1. Create `clean-transcript` command
2. Implement LLM-based text cleaning pipeline
3. Add speaker attribution logic
4. Test on existing transcript files

### Phase 2: Content Segmentation
1. Create `segment-transcript` command  
2. Implement topic boundary detection
3. Add segment type classification
4. Create summary generation for segments

### Phase 3: Batch Processing & Integration
1. Add batch processing capabilities for all stages
2. Create makefile-compatible workflows
3. Integrate with Reddit pipeline outputs
4. Develop FAQ generation from combined data

## Technical Considerations

### LLM Integration
- **Model Selection**: Use GPT-4 or similar for high-quality text processing
- **Cost Management**: Process single videos during development, batch for production
- **Prompt Engineering**: Develop specialized prompts for cleaning and segmentation
- **Error Handling**: Graceful degradation when LLM services are unavailable

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

```
data/youtube/
├── raw/                    # Stage 1 output
│   ├── 2025-09-06__-tRDk3P7bg.json
│   └── 2025-08-30_2FcOn-1IZY0.json
├── cleaned/                # Stage 2 output  
│   ├── 2025-09-06__-tRDk3P7bg_cleaned.json
│   └── 2025-08-30_2FcOn-1IZY0_cleaned.json
├── segmented/              # Stage 3 output
│   ├── 2025-09-06__-tRDk3P7bg_segmented.json
│   └── 2025-08-30_2FcOn-1IZY0_segmented.json
└── processed/              # Stage 4 output (future)
    ├── faq_content.json
    └── blog_drafts/
```

### Makefile-Friendly Naming Convention
- **Input dependency**: `{stage_dir}/{base_name}.json`
- **Output target**: `{next_stage_dir}/{base_name}_{stage_suffix}.json`
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

### Pydantic Models (Conceptual)
- `RawTranscript`: Stage 1 output structure
- `CleanedTranscript`: Stage 2 output with speaker attribution
- `SegmentedContent`: Stage 3 output with topical breakdown
- `ProcessedContent`: Stage 4 output ready for FAQ/blog generation
- `CrossPlatformTopic`: Combined YouTube + Reddit insights on specific topics
