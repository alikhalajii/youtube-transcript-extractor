"""Simple test/demo script for the YouTube Transcript Extractor."""

from youtube_transcript.extractor import YouTubeTranscriptExtractor
from youtube_transcript.writer import TranscriptWriter


def demo_extraction():
    """Demonstrate basic transcript extraction."""

    # Example YouTube URLs
    test_urls = [
        "https://www.youtube.com/watch?v=jNQXAC9IVRw",  # Full URL
        "https://youtu.be/jNQXAC9IVRw",  # Short URL
        "jNQXAC9IVRw",  # Just video ID
    ]

    extractor = YouTubeTranscriptExtractor()

    print("🧪 Testing Video ID extraction...\n")
    for url in test_urls:
        video_id = extractor.extract_video_id(url)
        print(f"Input: {url}")
        print(f"Video ID: {video_id}\n")

    print("\n" + "=" * 60)
    print("🎥 Testing Transcript Extraction...")
    print("=" * 60 + "\n")

    try:
        # Extract transcript
        video_id = "jNQXAC9IVRw"  # "Me at the zoo" - first YouTube video
        print(f"Fetching transcript for video: {video_id}\n")

        transcript_info = extractor.get_transcript(video_id, ["en"])

        print("✅ Success!")
        print(f"   Language: {transcript_info['language']} ({transcript_info['language_code']})")
        print(f"   Type: {'Auto-generated' if transcript_info['is_generated'] else 'Manual'}")
        print(f"   Segments: {len(transcript_info['transcript'])}")
        print(f"   Translatable: {transcript_info['is_translatable']}")

        # Format transcript
        text = extractor.format_transcript_text(transcript_info["transcript"])
        print("\n📝 First 200 characters of transcript:")
        print(f"   {text[:200]}...")

        # Save to file
        print("\n💾 Saving transcript files...")
        writer = TranscriptWriter("demo_output")
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        md_file = writer.save_markdown(transcript_info, video_url, include_timestamps=True)
        json_file = writer.save_json(transcript_info, video_url)
        txt_file = writer.save_txt(transcript_info, include_timestamps=False)

        print(f"   ✓ Markdown: {md_file}")
        print(f"   ✓ JSON: {json_file}")
        print(f"   ✓ Text: {txt_file}")

        print("\n✨ Demo complete! Check the 'demo_output' directory for results.")

    except Exception as e:
        print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    demo_extraction()
