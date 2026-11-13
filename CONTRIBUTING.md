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

This project uses `ruff` for linting and formatting via `pre-commit`:

```bash
# Run all checks (lint + format)
uv run pre-commit run --all-files
```

Pre-commit hooks are configured to run automatically on commit.

## Contribution Workflow

This project uses a **trunk-based development** model:

1. **Branch** from `main` for each feature/fix:

   ```bash
   git checkout main
   git pull
   git checkout -b my-feature
   ```

2. **Develop** with small, focused commits. Run checks locally:

   ```bash
   uv run pytest
   uv run pre-commit run --all-files
   ```

3. **Open a Pull Request** against `main`. CI runs automatically.

4. **Squash merge** after review and passing CI.

5. **Delete** the feature branch after merge.

No long-lived `develop` branch — `main` is always deployable.

## Release Process

Maintainers: see [RELEASE.md](RELEASE.md).

## Reporting Issues

Please use the [GitHub issue tracker](https://github.com/vtulus/AESAmethods/issues) to report bugs or request features.

## License

By contributing, you agree that your contributions will be licensed under the BSD License.
