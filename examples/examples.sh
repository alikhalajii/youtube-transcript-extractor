#!/bin/bash

# Example usage script for YouTube Transcript Extractor

# Example 1: Basic usage - extract to markdown
echo "Example 1: Basic markdown extraction"
yt-transcript https://www.youtube.com/watch?v=jNQXAC9IVRw

# Example 2: Extract with timestamps to JSON
echo -e "\nExample 2: JSON with timestamps"
yt-transcript https://www.youtube.com/watch?v=jNQXAC9IVRw -f json -t

# Example 3: Save all formats to custom directory
echo -e "\nExample 3: All formats to custom directory"
yt-transcript https://www.youtube.com/watch?v=jNQXAC9IVRw -f all -o my_transcripts

# Example 4: Multi-language preference
echo -e "\nExample 4: Multi-language (English, Spanish)"
yt-transcript https://www.youtube.com/watch?v=jNQXAC9IVRw -l en -l es

# Example 5: Just video ID works too
echo -e "\nExample 5: Using video ID directly"
yt-transcript jNQXAC9IVRw

# Example 6: Short URL format
echo -e "\nExample 6: Short YouTube URL"
yt-transcript https://youtu.be/jNQXAC9IVRw
