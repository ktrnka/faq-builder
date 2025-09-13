# YouTube Data Pipeline Design

## Overview

A multi-stage ETL pipeline for extracting, cleaning, segmenting, and processing YouTube transcripts from office hours sessions for FAQ generation. The pipeline focuses on Keith's weekly office hours with AI/ML content.

## Current Implementation Status ✅

**Completed Phase 1 & 2 (September 2025):**
- ✅ Video discovery and transcript extraction
- ✅ Token analysis and model selection (GPT-4.1-mini)
- ✅ Combined transcript cleaning and segmentation
- ✅ Human-readable display commands
- ✅ Cost tracking and logging
- ✅ Modular CLI structure
- ✅ Clean directory organization (raw/ and cleaned/)

## Goals

- Extract transcripts from YouTube videos (primarily Keith's office hours)
- Clean and improve auto-generated transcripts using LLMs
- Segment long-form content into topical sections with speaker attribution
- Support experimentation with different processing strategies
- Build structured data suitable for FAQ generation and blog post creation

## Current Pipeline Architecture

```
Stage 1: Video Discovery & Transcript Extraction (✅ Implemented)
├── list-videos → filter videos by search term
├── download-transcript → data/youtube/raw/{date}_{video_id}.json
├── show-transcript → human-readable format with timestamps
└── count-tokens → model compatibility analysis

Stage 2: Combined Cleaning & Segmentation (✅ Implemented)
├── clean-transcript → data/youtube/cleaned/{date}_{video_id}.json
└── show-cleaned-transcript → formatted output with chapters

Stage 3: Batch Processing & Automation (Next Phase)
├── manifest generation for batch operations
├── Makefile for dependency management
└── Full pipeline automation

Stage 4: FAQ Generation (Future)
└── process-youtube-data → final FAQ/blog content
```
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

## Stage 1: Video Discovery & Transcript Extraction (✅ Implemented)

### Current Commands
- **`list-videos`** - Discovers videos in playlists by search term
- **`download-transcript`** - Extracts raw transcripts with metadata  
- **`show-transcript`** - Displays human-readable formatted transcript with timestamps
- **`count-tokens`** - Analyzes token count and model compatibility

### Current Output Format & Storage
**File Location**: `data/youtube/raw/{date}_{video_id}.json`

**JSON Structure**:
```json
{
  "metadata": {
    "snippet": {
      "title": "AI / Open Q & A w/Coach Keith",
      "publishedAt": "2025-09-05T23:01:57Z"
    }
  },
  "transcript": {
    "video_id": "video_id",
    "language": "English (auto-generated)", 
    "is_generated": true,
    "snippets": [
      {"text": "transcript text", "start": 5.52, "duration": 4.159}
    ]
  }
}
```

### Token Analysis Results (Actual Data)
- **Typical video length**: 22-24k tokens for 1-hour sessions
- **Character-to-token ratio**: ~3.0 chars/token
- **Model selection**: GPT-4.1-mini (128k context, cost-effective)
- **Cost per video**: ~$0.0008-0.0015 for cleaning (very affordable)

## Stage 2: Transcript Cleaning & Segmentation (✅ Implemented)

### Current Commands  
- **`clean-transcript`** - Combined cleaning and segmentation using LLM
- **`show-cleaned-transcript`** - Formatted display with chapters and speakers

### Implementation Details
**Model Used**: GPT-4.1-mini via OpenAI structured outputs API
**Cost Tracking**: Automatic logging with token usage and cost estimates
**Quality Focus**: Readability, coherence, content preservation

### Current Output Format & Storage
**File Location**: `data/youtube/cleaned/{date}_{video_id}.json`

**Pydantic Structure**:
```python
class CleanedTranscript(BaseModel):
    title: str
    date: str  
    total_duration_seconds: float
    chapters: list[Chapter]
    processing_notes: list[str]

class Chapter(BaseModel):
    title: str
    chapter_type: Literal["qa", "explanation", "live_coding", "admin", "discussion"]
    start_time: float
    segments: list[CleanedSegment]

class CleanedSegment(BaseModel):
    speaker: Literal["Host", "Student", "Other"]
    text: str
```

### Processing Quality Achieved
- **Content Preservation**: Maintains all substantive information
- **Readability**: Transforms speech into clear, coherent prose
- **Speaker Attribution**: Identifies Host, Student, Other speakers
- **Chapter Segmentation**: Logical topic-based divisions
- **Cost Efficiency**: ~$0.0008 per video for full processing

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

## Current File Organization (✅ Implemented)

```
data/youtube/
├── raw/                    # Stage 1 output - original transcripts
│   ├── 2025-09-06__-tRDk3P7bg.json
│   ├── 2025-08-30_2FcOn-1IZY0.json
│   └── [14 total videos as of Sept 2025]
└── cleaned/                # Stage 2 output - processed transcripts  
    ├── 2025-09-06__-tRDk3P7bg.json
    └── [processed as needed]
```

### Makefile-Friendly Design
- **Consistent naming**: Same filename in raw/ and cleaned/ directories
- **Clear dependencies**: `raw/video.json` → `cleaned/video.json`
- **Conditional processing**: Only clean if raw file is newer
- **Batch operations**: Easy to process entire directories

Example makefile patterns:
```makefile
# Single file processing
data/youtube/cleaned/%.json: data/youtube/raw/%.json
	uv run faq-builder youtube clean-transcript $<

# Process all raw transcripts
clean-all: $(patsubst data/youtube/raw/%.json,data/youtube/cleaned/%.json,$(wildcard data/youtube/raw/*.json))
```

## Next Phase: Batch Processing & Automation

### Immediate Priorities (from TODO.md)
1. **Manifest Generation**: Update `list-videos` to create manifest file
2. **Batch Operations**: Commands that work with manifest files
3. **Makefile Creation**: Full dependency automation
4. **Scale-up**: Process all 14 raw transcripts

### Future Pipeline Extensions
- **FAQ Generation**: Convert cleaned transcripts to FAQ format
- **Cross-referencing**: Link YouTube content with Reddit discussions
- **Search/Index**: Make content searchable and browsable

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
