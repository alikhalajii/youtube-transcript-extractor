"""Output writer for saving transcripts to files."""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict

import yaml


class TranscriptWriter:
    """Write transcripts to various formats with metadata."""

    def __init__(self, output_dir: str = "transcripts"):
        """
        Initialize the transcript writer.

        Args:
            output_dir: Directory to save transcript files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save_markdown(
        self, transcript_info: Dict, video_url: str, include_timestamps: bool = False
    ) -> Path:
        """
        Save transcript as Markdown with YAML frontmatter.

        Args:
            transcript_info: Transcript data and metadata
            video_url: Original YouTube video URL
            include_timestamps: Whether to include timestamps in transcript

        Returns:
            Path to the saved file
        """
        video_id = transcript_info["video_id"]
        filename = f"{video_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        filepath = self.output_dir / filename

        # Prepare metadata
        metadata = {
            "video_id": video_id,
            "video_url": video_url,
            "language": transcript_info["language"],
            "language_code": transcript_info["language_code"],
            "is_generated": transcript_info["is_generated"],
            "is_translatable": transcript_info["is_translatable"],
            "extracted_at": datetime.now().isoformat(),
            "total_segments": len(transcript_info["transcript"]),
        }

        # Format transcript
        from youtube_transcript.extractor import YouTubeTranscriptExtractor

        if include_timestamps:
            transcript_text = YouTubeTranscriptExtractor.format_transcript_with_timestamps(
                transcript_info["transcript"]
            )
        else:
            transcript_text = YouTubeTranscriptExtractor.format_transcript_text(
                transcript_info["transcript"]
            )

        # Create markdown content with frontmatter
        content = "---\n"
        content += yaml.dump(metadata, default_flow_style=False, sort_keys=False)
        content += "---\n\n"
        content += "# YouTube Video Transcript\n\n"
        content += f"**Video URL:** {video_url}\n\n"
        content += f"**Language:** {metadata['language']} ({metadata['language_code']})\n\n"
        content += f"**Type:** {'Auto-generated' if metadata['is_generated'] else 'Manual'}\n\n"
        content += "---\n\n"
        content += "## Transcript\n\n"
        content += transcript_text + "\n"

        # Write to file
        filepath.write_text(content, encoding="utf-8")

        return filepath

    def save_json(self, transcript_info: Dict, video_url: str) -> Path:
        """
        Save transcript as JSON with full metadata.

        Args:
            transcript_info: Transcript data and metadata
            video_url: Original YouTube video URL

        Returns:
            Path to the saved file
        """
        video_id = transcript_info["video_id"]
        filename = f"{video_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.output_dir / filename

        # Prepare full data
        data = {
            "metadata": {
                "video_id": video_id,
                "video_url": video_url,
                "language": transcript_info["language"],
                "language_code": transcript_info["language_code"],
                "is_generated": transcript_info["is_generated"],
                "is_translatable": transcript_info["is_translatable"],
                "extracted_at": datetime.now().isoformat(),
                "total_segments": len(transcript_info["transcript"]),
            },
            "transcript": transcript_info["transcript"],
        }

        # Write to file
        filepath.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

        return filepath

    def save_txt(self, transcript_info: Dict, include_timestamps: bool = False) -> Path:
        """
        Save transcript as plain text.

        Args:
            transcript_info: Transcript data and metadata
            include_timestamps: Whether to include timestamps in transcript

        Returns:
            Path to the saved file
        """
        video_id = transcript_info["video_id"]
        filename = f"{video_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        filepath = self.output_dir / filename

        # Format transcript
        from youtube_transcript.extractor import YouTubeTranscriptExtractor

        if include_timestamps:
            transcript_text = YouTubeTranscriptExtractor.format_transcript_with_timestamps(
                transcript_info["transcript"]
            )
        else:
            transcript_text = YouTubeTranscriptExtractor.format_transcript_text(
                transcript_info["transcript"]
            )

        # Write to file
        filepath.write_text(transcript_text, encoding="utf-8")

        return filepath

    @staticmethod
    def _to_srt_timestamp(total_seconds: float) -> str:
        """Convert seconds to SRT timestamp format HH:MM:SS,mmm."""
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        milliseconds = int(round((total_seconds - int(total_seconds)) * 1000))

        # Handle edge case where rounding pushes to next second
        if milliseconds == 1000:
            milliseconds = 0
            seconds += 1
            if seconds == 60:
                seconds = 0
                minutes += 1
                if minutes == 60:
                    minutes = 0
                    hours += 1

        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

    @staticmethod
    def _segment_value(segment, key: str, default=None):
        """Read transcript values from either dict-based or object-based segments."""
        if isinstance(segment, dict):
            return segment.get(key, default)
        return getattr(segment, key, default)

    def save_srt(self, transcript_info: Dict) -> Path:
        """Save transcript as SubRip subtitle (.srt) format."""
        video_id = transcript_info["video_id"]
        filename = f"{video_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.srt"
        filepath = self.output_dir / filename

        lines = []
        for index, segment in enumerate(transcript_info["transcript"], start=1):
            text = self._segment_value(segment, "text", "")
            start = float(self._segment_value(segment, "start", 0.0))
            duration = float(self._segment_value(segment, "duration", 0.0))
            end = start + duration

            if not text or not text.strip():
                continue

            start_ts = self._to_srt_timestamp(start)
            end_ts = self._to_srt_timestamp(end)

            lines.append(str(index))
            lines.append(f"{start_ts} --> {end_ts}")
            lines.append(text.strip())
            lines.append("")

        filepath.write_text("\n".join(lines), encoding="utf-8")
        return filepath
