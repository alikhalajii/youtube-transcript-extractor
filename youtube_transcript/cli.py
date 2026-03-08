"""Command-line interface for yt-transcript-extractor."""

import sys

import click
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled

from youtube_transcript.extractor import YouTubeTranscriptExtractor
from youtube_transcript.writer import TranscriptWriter


@click.command()
@click.argument("url", required=True)
@click.option(
    "--output-dir",
    "-o",
    default="transcripts",
    help="Output directory for transcript files (default: transcripts)",
    type=click.Path(),
)
@click.option(
    "--format",
    "-f",
    type=click.Choice(["markdown", "json", "txt", "srt", "all"], case_sensitive=False),
    default="markdown",
    help="Output format (default: markdown)",
)
@click.option(
    "--timestamps/--no-timestamps",
    "-t/-T",
    default=False,
    help="Include timestamps in transcript (default: no timestamps)",
)
@click.option(
    "--language",
    "-l",
    multiple=True,
    default=["en"],
    help="Preferred language codes (can be specified multiple times, e.g., -l en -l es)",
)
def main(url: str, output_dir: str, format: str, timestamps: bool, language: tuple):
    """
    Extract transcription from a YouTube video.

    URL can be a full YouTube URL or just a video ID.

    Examples:

        yt-transcript https://www.youtube.com/watch?v=dQw4w9WgXcQ

        yt-transcript dQw4w9WgXcQ -f json -t

        yt-transcript https://youtu.be/dQw4w9WgXcQ -o my_transcripts -l en -l es
    """
    click.echo("yt-transcript-extractor\n")

    # Extract video ID
    extractor = YouTubeTranscriptExtractor()
    video_id = extractor.extract_video_id(url)

    if not video_id:
        click.echo(f"Error: Could not extract video ID from URL: {url}", err=True)
        sys.exit(1)

    click.echo(f"Video ID: {video_id}")

    # Fetch transcript
    try:
        click.echo(f"Fetching transcript (languages: {', '.join(language)})...")
        transcript_info = extractor.get_transcript(video_id, list(language))

        click.echo("Transcript found.")
        click.echo(
            f"   Language: {transcript_info['language']} ({transcript_info['language_code']})"
        )
        click.echo(f"   Type: {'Auto-generated' if transcript_info['is_generated'] else 'Manual'}")
        click.echo(f"   Segments: {len(transcript_info['transcript'])}")

    except TranscriptsDisabled:
        click.echo("Error: Transcripts are disabled for this video.", err=True)
        sys.exit(1)
    except NoTranscriptFound:
        click.echo(f"Error: No transcript found for languages: {', '.join(language)}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    # Save transcript
    writer = TranscriptWriter(output_dir)
    saved_files = []

    try:
        click.echo("\nSaving transcript...")

        # Reconstruct proper video URL
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        if format in ["markdown", "all"]:
            filepath = writer.save_markdown(transcript_info, video_url, timestamps)
            saved_files.append(filepath)
            click.echo(f"   Markdown: {filepath}")

        if format in ["json", "all"]:
            filepath = writer.save_json(transcript_info, video_url)
            saved_files.append(filepath)
            click.echo(f"   JSON: {filepath}")

        if format in ["txt", "all"]:
            filepath = writer.save_txt(transcript_info, timestamps)
            saved_files.append(filepath)
            click.echo(f"   Text: {filepath}")

        if format in ["srt", "all"]:
            filepath = writer.save_srt(transcript_info)
            saved_files.append(filepath)
            click.echo(f"   SRT: {filepath}")

        click.echo(f"\nDone. Transcript{'s' if len(saved_files) > 1 else ''} saved successfully.")

    except Exception as e:
        click.echo(f"Error saving transcript: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
