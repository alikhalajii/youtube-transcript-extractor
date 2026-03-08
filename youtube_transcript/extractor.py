"""Core functionality for extracting YouTube transcriptions."""

import re
from typing import Dict, List, Optional
from urllib.parse import parse_qs, urlparse

from youtube_transcript_api import YouTubeTranscriptApi


class YouTubeTranscriptExtractor:
    """Extract transcriptions from YouTube videos."""

    @staticmethod
    def extract_video_id(url: str) -> Optional[str]:
        """
        Extract video ID from various YouTube URL formats.

        Args:
            url: YouTube video URL or video ID

        Returns:
            Video ID if found, None otherwise
        """
        # If it's already a video ID (11 characters)
        if re.match(r"^[A-Za-z0-9_-]{11}$", url):
            return url

        # Parse URL
        parsed_url = urlparse(url)

        # Handle various YouTube URL formats
        if parsed_url.hostname in ("www.youtube.com", "youtube.com", "m.youtube.com"):
            if parsed_url.path == "/watch":
                query_params = parse_qs(parsed_url.query)
                return query_params.get("v", [None])[0]
            elif parsed_url.path.startswith("/embed/"):
                return parsed_url.path.split("/")[2]
            elif parsed_url.path.startswith("/v/"):
                return parsed_url.path.split("/")[2]
        elif parsed_url.hostname in ("youtu.be", "www.youtu.be"):
            return parsed_url.path[1:]

        return None

    @staticmethod
    def get_transcript(video_id: str, languages: Optional[List[str]] = None) -> Dict:
        """
        Fetch transcript for a YouTube video.

        Args:
            video_id: YouTube video ID
            languages: Preferred language codes (e.g., ['en', 'es'])

        Returns:
            Dictionary containing transcript data and metadata

        Raises:
            TranscriptsDisabled: If transcripts are disabled for the video
            NoTranscriptFound: If no transcript is available in requested languages
            Exception: For other errors
        """
        if languages is None:
            languages = ["en"]

        api = YouTubeTranscriptApi()

        try:
            # Try to fetch transcript with preferred languages
            fetched_transcript = api.fetch(video_id, languages=tuple(languages))
            used_language = languages[0]
        except Exception:
            # If fails, try without language specification (default to English)
            try:
                fetched_transcript = api.fetch(video_id)
                used_language = "en"
            except Exception:
                raise

        # Convert FetchedTranscript to list of dicts
        transcript_data = []
        for snippet in fetched_transcript:
            transcript_data.append(
                {"text": snippet.text, "start": snippet.start, "duration": snippet.duration}
            )

        # Determine language name
        language_names = {
            "en": "English",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "it": "Italian",
            "pt": "Portuguese",
            "ru": "Russian",
            "ja": "Japanese",
            "ko": "Korean",
            "zh": "Chinese",
            "zh-CN": "Chinese (Simplified)",
            "zh-TW": "Chinese (Traditional)",
        }
        language_name = language_names.get(
            used_language,
            used_language.title() if used_language else "Unknown",
        )

        return {
            "video_id": video_id,
            "language": language_name,
            "language_code": used_language,
            "is_generated": False,  # fetchedTranscript doesn't provide this info directly
            "is_translatable": True,  # Assume translatable
            "transcript": transcript_data,
        }

    @staticmethod
    def format_transcript_text(transcript_data: List[Dict]) -> str:
        """
        Format transcript data into readable text.

        Args:
            transcript_data: List of transcript segments with text and timing

        Returns:
            Formatted transcript text
        """
        lines = []
        for segment in transcript_data:
            text = segment["text"].strip()
            if text:
                lines.append(text)

        return " ".join(lines)

    @staticmethod
    def format_transcript_with_timestamps(transcript_data: List[Dict]) -> str:
        """
        Format transcript data with timestamps.

        Args:
            transcript_data: List of transcript segments with text and timing

        Returns:
            Formatted transcript with timestamps
        """
        lines = []
        for segment in transcript_data:
            start_time = segment["start"]
            text = segment["text"].strip()

            # Convert seconds to HH:MM:SS format
            hours = int(start_time // 3600)
            minutes = int((start_time % 3600) // 60)
            seconds = int(start_time % 60)

            timestamp = f"[{hours:02d}:{minutes:02d}:{seconds:02d}]"

            if text:
                lines.append(f"{timestamp} {text}")

        return "\n".join(lines)
