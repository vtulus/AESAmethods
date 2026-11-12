# Contributing to AESAmethods

Thank you for your interest in contributing to AESAmethods!

## Development Setup

```bash
# Clone the repository
git clone https://github.com/vtulus/AESAmethods.git
cd AESAmethods

# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync --all-extras
```

## Running Tests

```bash
uv run pytest
```

## Code Style

This project uses `ruff` for linting and formatting:

```bash
# Check for issues
uv run ruff check .

# Auto-fix issues
uv run ruff check . --fix

# Format code
uv run ruff format .
```

Pre-commit hooks are configured to run automatically on commit.

## Release Process (for maintainers)

Releases are automated via GitHub Actions. This project uses the [Keep a Changelog](https://keepachangelog.com/) format with an `[Unreleased]` section.

To create a new release:

1. **Update the version** in `pyproject.toml` (e.g., `version = "0.11.0"`)
2. **Move changes from `[Unreleased]` to a new versioned section** in `CHANGELOG.md`:

   ```markdown
   ## 0.11.0 (2026-11-13)

   ### Added
   - New feature description

   ### Changed
   - Change description
   ```

   Leave an empty `[Unreleased]` section for the next development cycle.
   The changelog entry **must** be present for the release workflow to succeed.
3. **Commit and tag**:

   ```bash
   git add pyproject.toml CHANGELOG.md
   git commit -m "Release 0.11.0"
   git tag v0.11.0
   git push origin main --tags
   ```

4. The workflow will:
   - Validate the tag matches `pyproject.toml` version
   - Verify version is higher than published on PyPI
   - Run tests
   - Build the package
   - Create a GitHub Release with changelog notes from `CHANGELOG.md`
   - Publish to PyPI (if configured)

## Reporting Issues

Please use the [GitHub issue tracker](https://github.com/vtulus/AESAmethods/issues) to report bugs or request features.

## License

By contributing, you agree that your contributions will be licensed under the BSD License.
