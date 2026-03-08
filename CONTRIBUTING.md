# Contributing to yt-transcript-extractor

## Setting Up Development Environment

```bash
git clone https://github.com/alikhalajii/yt-transcript-extractor.git
cd yt-transcript-extractor

uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

## Local Quality Checks

Before committing, ensure all checks pass locally:

```bash
pre-commit install
```

This runs `black --check`, `ruff check`, `mypy`, and `pytest` automatically before each commit.

Or run them manually:

```bash
black youtube_transcript/
ruff check youtube_transcript/
mypy youtube_transcript/
pytest
```

## Release Process

To prepare a release locally, run the complete validation:

```bash
bash scripts/release-check.sh
```

This check validates:
- Code formatting (`black --check`)
- Linting (`ruff check`)
- Type checking (`mypy`)
- Tests (`pytest` with coverage)
- Package build (`python -m build`)
- Package metadata (`twine check`)

### Publishing to PyPI

1. **One-time setup**: Configure PyPI Trusted Publisher for this repository:
   - Go to PyPI project settings for `yt-transcript-extractor`
   - Add GitHub as a Trusted Publisher
   - Specify repository: `alikhalajii/yt-transcript-extractor`
   - Workflow file: `.github/workflows/publish.yml`

2. **Create a release on GitHub**:
   - Tag: `v<version>` (e.g., `v0.2.0`)
   - Release title and description
   - Click "Publish release"

3. **Automated publishing**:
   - `.github/workflows/publish.yml` runs automatically
   - Builds both `sdist` and `wheel` distributions
   - Publishes to PyPI using Trusted Publisher (no secrets needed)

## Code Style

- **Line length**: 100 characters
- **Python target**: 3.9+
- **Formatter**: Black
- **Linter**: Ruff (E, F, I, N, W rules)
- **Type checker**: mypy with strict mode

## Testing

Ensure tests pass on all supported Python versions (3.9, 3.10, 3.11, 3.12):

```bash
pytest --cov=youtube_transcript --cov-report=term-missing
```

GitHub Actions matrix testing covers all versions on push/PR.
