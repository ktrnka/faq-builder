# FAQ Builder TODO

## Immediate Next Steps (Priority Order)

### 1. Manifest & Batch Operations
- [ ] Update YouTube playlist scanning to create manifest file (JSON list of video IDs)
- [ ] Add commands to work with manifest files (e.g., `youtube download-from-manifest`)
- [ ] Test xargs integration for batch operations

### 2. Build Automation
- [ ] Create Makefile with dependency chains:
  - Raw transcript download → Cleaned transcript → Display
  - Conditional execution (only process if source is newer)
  - Batch processing targets

### 3. YouTube Pipeline Scale-Up
- [ ] Run download for all videos in manifest
- [ ] Run LLM cleaning on all raw transcripts
- [ ] Verify cost estimates for full pipeline

### 4. Reddit Pipeline Enhancement
- [ ] Build Reddit enrichment pipeline
- [ ] Add `reddit show-thread` command (by post ID/URL)
- [ ] Format Reddit interactions as readable conversation threads
- [ ] Test with actual Reddit data

## Design Document Updates Needed
- [ ] Update YouTube design doc with current implementation status
- [ ] Document Reddit pipeline design (thread extraction & formatting)
- [ ] Add Makefile/automation strategy to design docs

## Technical Debt & Polish
- [ ] Add progress bars for batch operations
- [ ] Improve error handling in batch scenarios
- [ ] Add dry-run options for batch commands
- [ ] Consider parallel processing for LLM cleaning

## Future Considerations
- [ ] FAQ generation from cleaned transcripts
- [ ] Cross-reference YouTube + Reddit content
- [ ] Search/indexing capabilities
- [ ] Web interface for browsing content
