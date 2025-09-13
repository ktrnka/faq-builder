"""YouTube transcript cleaning and segmentation prompt."""

from typing import Literal

from pydantic import BaseModel

from ..base import BasePrompt


class CleanedSegment(BaseModel):
    """Individual speaker turn within a chapter."""
    speaker: Literal["Host", "Student", "Other"]
    text: str


class Chapter(BaseModel):
    """Topical section of a transcript with timing and classification."""
    title: str
    chapter_type: Literal["qa", "explanation", "live_coding", "admin", "discussion"]
    start_time: float  # seconds from beginning of video
    segments: list[CleanedSegment]


class CleanedTranscript(BaseModel):
    """Complete cleaned and segmented transcript output."""
    title: str
    date: str
    total_duration_seconds: float
    chapters: list[Chapter]
    processing_notes: list[str]


class TranscriptCleaningPrompt(BasePrompt[CleanedTranscript]):
    """Prompt for cleaning and segmenting YouTube office hours transcripts."""
    
    model = "gpt-4.1-mini"
    output_model = CleanedTranscript
    
    system_prompt = """You are an expert at cleaning and segmenting YouTube transcripts from technical office hours sessions.

Your tasks:
1. Clean the transcript by removing filler words (um, uh, like, you know), fixing speech errors, and correcting technical terminology
2. Identify speakers as "Host" (the instructor), "Student" (participants asking questions), or "Other" (unclear/multiple speakers)
3. Segment the content into logical chapters based on topics and conversation flow
4. Classify each chapter by type: qa, explanation, live_coding, admin, or discussion

Chapter Guidelines:
- Start new chapters when topics change or new questions begin
- Chapter timing should be approximate - close enough for navigation
- Choose descriptive titles that would help students find specific topics
- qa: Question and answer sessions
- explanation: Host explaining concepts or techniques  
- live_coding: Hands-on programming demonstrations
- admin: Session setup, announcements, wrap-up
- discussion: General conversation or exploratory topics

Cleaning Guidelines:
- PRESERVE ALL CONTENT: Only remove obvious filler words, false starts, and repetition - never remove substantive content
- MAXIMIZE READABILITY: Transform speech into clear, coherent text that reads naturally
- COMPLETE SENTENCES: Turn speech fragments into complete, well-formed sentences
- SMOOTH FLOW: Remove stutters, repeated words, and speech repairs while maintaining natural conversation flow
- CONSERVATIVE EDITING: When in doubt, keep the original meaning rather than risk losing information
- Fix obvious transcription errors and clarify unclear references when context makes the meaning obvious
- Maintain chronological order and preserve the speaker's intent and tone

Speaker Recognition Guidelines:
- Only identify speakers when clearly distinguishable from context
- Host: Usually introduces topics, explains concepts, leads the session
- Student: Asks questions, responds to Host prompts, seeks clarification
- Other: When unsure, multiple speakers, or overlapping speech

Output the result as valid JSON matching the specified schema."""

    def format_input(self, **kwargs) -> str:
        """Format transcript text for cleaning and segmentation.
        
        Args:
            transcript_text: Human-readable transcript from show-transcript command
            
        Returns:
            Formatted prompt text
        """
        transcript_text = kwargs.get('transcript_text', '')
        if not transcript_text:
            raise ValueError("transcript_text is required")
            
        return f"""Please clean and segment this YouTube office hours transcript into readable, coherent text:

{transcript_text}

Focus on making the output highly readable while preserving all substantive content. Transform speech patterns into clear prose that flows naturally.

Return the cleaned and segmented transcript as valid JSON matching the CleanedTranscript schema."""
