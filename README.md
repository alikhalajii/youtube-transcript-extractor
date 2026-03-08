# YouTube Transcript Extractor

Extract YouTube video transcripts from the command line and save them in LLM-friendly formats (Markdown with frontmatter, JSON, TXT, and SRT).

Lightweight Python CLI for transcript extraction, subtitle generation, and downstream content workflows.


## Features

- CLI input supports full YouTube URLs or raw video IDs.
- Output formats: `markdown`, `json`, `txt`, `srt`, or `all`.
- Optional timestamped transcript output.
- Language preference fallback via repeated `--language` options.
- Structured metadata for downstream LLM/RAG pipelines.

## Use Cases

- Build subtitle files (`.srt`) from available captions.
- Archive transcripts in structured Markdown and JSON.
- Prepare source text for search, analytics, and summarization.
- Feed normalized transcripts into RAG or ingestion pipelines.

## Requirements

- Python `>=3.9`
- `uv` (recommended) or `pip`

## Installation

```bash
# clone and enter repository
git clone https://github.com/alikhalajii/youtube-transcript-extractor.git
cd youtube-transcript-extractor

# create environment and install
uv venv
source .venv/bin/activate
uv pip install -e .
```

With development tools:

```bash
uv pip install -e ".[dev]"
```

## Quick Start

```bash
# basic (markdown output)
yt-transcript https://www.youtube.com/watch?v=rfscVS0vtbw

# all formats, with timestamps
yt-transcript rfscVS0vtbw -f all -t

# subtitle file (SRT)
yt-transcript rfscVS0vtbw -f srt

# custom output directory
yt-transcript rfscVS0vtbw -o outputs

# language preference order
yt-transcript rfscVS0vtbw -l en -l es
```

## CLI Reference

```text
yt-transcript [OPTIONS] URL
```

| Option | Short | Description | Default |
|---|---|---|---|
| `--output-dir` | `-o` | Directory for output files | `transcripts` |
| `--format` | `-f` | `markdown`, `json`, `txt`, `srt`, `all` | `markdown` |
| `--timestamps / --no-timestamps` | `-t / -T` | Include timestamps in text output | `--no-timestamps` |
| `--language` | `-l` | Preferred language code(s), repeatable | `en` |

## Output

### Markdown (`.md`)

Best for LLM ingestion. Includes YAML frontmatter:

```yaml
video_id: rfscVS0vtbw
video_url: https://www.youtube.com/watch?v=rfscVS0vtbw
language: English
language_code: en
is_generated: false
is_translatable: true
extracted_at: 2026-03-08T13:35:26.502073
total_segments: 2935
```

### JSON (`.json`)

Machine-friendly metadata and transcript segments with timing.

### Text (`.txt`)

Plain transcript content, optionally timestamped.

### SubRip (`.srt`)

Subtitle-ready output using the standard `HH:MM:SS,mmm --> HH:MM:SS,mmm` format.

## Project Structure

```text
youtube-transcript-extractor/
├── examples/
│   ├── demo.py
│   └── examples.sh
├── youtube_transcript/
│   ├── __init__.py
│   ├── cli.py
│   ├── extractor.py
│   └── writer.py
├── .gitignore
├── LICENSE
├── pyproject.toml
└── README.md
```

## Development

```bash
black youtube_transcript/
ruff check youtube_transcript/
pytest
```

Install a commit-time gate that mirrors CI checks:

```bash
uv pip install -e ".[dev]"
pre-commit install
```

This runs `black --check`, `ruff check`, `mypy`, and `pytest` before each commit.

## Troubleshooting

- If captions are disabled by the video owner, transcript extraction will fail.
- If a requested language does not exist, pass multiple `-l` values as fallback.
- If `yt-transcript` is not found, ensure your virtual environment is activated.

## License

This project is licensed under the MIT License. See `LICENSE`.
