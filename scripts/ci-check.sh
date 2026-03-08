#!/usr/bin/env bash
set -euo pipefail

# Run the same quality checks used in CI so commits fail fast locally.
black --check --diff .
ruff check .
mypy youtube_transcript/

if [[ "${CI:-}" == "true" ]]; then
	pytest --cov=youtube_transcript --cov-report=term-missing --cov-report=xml
else
	pytest --cov=youtube_transcript --cov-report=term-missing
fi
