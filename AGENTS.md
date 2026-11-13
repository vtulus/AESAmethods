## Agent skills

### Issue tracker

GitHub Issues (vtulus/AESAmethods) via `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Default five canonical labels: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context layout: `GLOSSARY.md` + `docs/adr/` at repo root. See `docs/agents/domain.md`.

## Commands

- Install: `uv sync --all-extras`
- Tests (coverage gate at 90%): `uv run pytest`
- Lint: `uvx ruff@0.17.5 check . --exclude notebooks`
- Format: `uvx ruff@0.17.5 format .`
- Pre-commit: `uvx pre-commit run --all-files`

Tests that touch Brightway create a throw-away project in a temporary
`BRIGHTWAY2_DIR` (see `tests/conftest.py`), so no ecoinvent installation is
needed.
