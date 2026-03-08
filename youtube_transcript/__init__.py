"""Yt Transcript Extractor - Extract and save YouTube video transcriptions."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("yt-transcript-extractor")
except PackageNotFoundError:
    # Fallback for local source usage before installation.
    __version__ = "0.1.0"

__author__ = "ALI KHALAJI"
