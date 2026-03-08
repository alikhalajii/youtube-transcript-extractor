from youtube_transcript import __version__
from youtube_transcript.extractor import YouTubeTranscriptExtractor
from youtube_transcript.writer import TranscriptWriter


def test_package_metadata_exposed() -> None:
    assert isinstance(__version__, str)
    assert __version__


def test_extract_video_id_from_common_inputs() -> None:
    assert YouTubeTranscriptExtractor.extract_video_id("dQw4w9WgXcQ") == "dQw4w9WgXcQ"
    assert (
        YouTubeTranscriptExtractor.extract_video_id(
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        )
        == "dQw4w9WgXcQ"
    )
    assert (
        YouTubeTranscriptExtractor.extract_video_id("https://youtu.be/dQw4w9WgXcQ")
        == "dQw4w9WgXcQ"
    )


def test_srt_timestamp_formatting() -> None:
    assert TranscriptWriter._to_srt_timestamp(0.0) == "00:00:00,000"
    assert TranscriptWriter._to_srt_timestamp(61.5) == "00:01:01,500"
