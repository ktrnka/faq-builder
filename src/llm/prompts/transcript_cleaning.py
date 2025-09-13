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
    
    model = "gpt-4-turbo"
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
- Preserve all technical content and terminology accurately
- Maintain chronological order and natural conversation flow
- Remove repetitive speech repairs and false starts
- Correct obvious transcription errors, especially technical terms
- Keep the meaning and tone of the original speech

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
            
        return f"""Please clean and segment this YouTube office hours transcript:

{transcript_text}

Return the cleaned and segmented transcript as valid JSON matching the CleanedTranscript schema."""
