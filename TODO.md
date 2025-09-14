# FAQ Builder TODO

## Content Categorization & Blog Post Development

### 1. Data Collection & Preparation
- [ ] Download more YouTube transcripts (expand beyond current 27 videos)
- [ ] Complete inventory of all available Reddit threads
- [ ] Ensure we have comprehensive content coverage

### 2. Categorization System Implementation
- [ ] Split categorization analysis out of design doc into separate analysis document
  - Move content from `/design_docs/categorization_system.md` to `/analysis/content_categorization.md`
  - Keep design principles in design doc, move analysis results to analysis doc
- [ ] Review ALL Reddit threads systematically (not just sample of 30)
- [ ] Review ALL YouTube transcripts systematically (not just sample of 10)
- [ ] Refine category taxonomy based on complete content review

### 3. Blog Post Planning
- [ ] Group Reddit posts and YouTube chapters into candidate blog post clusters
- [ ] Identify top 3-5 blog post topics with strongest content coverage
- [ ] Create blog post outlines for highest-priority topics
- [ ] Map specific Reddit threads and YouTube chapters to each blog post

## Technical Infrastructure (Lower Priority)

### YouTube Pipeline Scale-Up
- [ ] Run download for remaining videos in manifest
- [ ] Add Scrapfly proxy integration to transcript downloader (YouTube blocking requests)
- [ ] Run LLM cleaning on all raw transcripts
- [ ] Verify cost estimates for full pipeline

### Build Automation
- [ ] Create Makefile with dependency chains:
  - Raw transcript download → Cleaned transcript → Display
  - Conditional execution (only process if source is newer)
  - Batch processing targets

### Technical Debt & Polish
- [ ] Add progress bars for batch operations
- [ ] Improve error handling in batch scenarios
- [ ] Add dry-run options for batch commands
- [ ] Consider parallel processing for LLM cleaning

## Future Considerations
- [ ] FAQ generation from cleaned transcripts
- [ ] Cross-reference YouTube + Reddit content
- [ ] Search/indexing capabilities
- [ ] Web interface for browsing content
