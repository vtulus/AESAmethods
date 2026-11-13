"""Shared fixtures for the AESA test suite.

Tests that touch Brightway run against a throw-away project created inside a
temporary directory: ``BRIGHTWAY2_DIR`` is pointed at that directory *before*
``bw2data`` is imported, so a real project on the machine is never touched and
no ecoinvent data is required.
"""

from __future__ import annotations

import importlib.resources
import os
import tempfile
import uuid
from pathlib import Path

import pytest
import yaml

# Must run before bw2data/brightway2 are imported: the data directory is only
# read once, at import time.
os.environ["BRIGHTWAY2_DIR"] = tempfile.mkdtemp(prefix="aesa-bw-")

import brightway2 as bw  # noqa: E402
import bw2data as bd  # noqa: E402


def data_dir() -> Path:
    """Return the directory holding the packaged YAML characterisation files."""
    return Path(str(importlib.resources.files("aesa_pbs") / "data"))


def packaged_yaml_files() -> list[Path]:
    """Return the packaged YAML files, sorted by name."""
    return sorted(data_dir().glob("*.yaml"))


def load_rows(path: Path) -> list[dict]:
    """Load a characterisation-factor YAML file as a list of rows."""
    with open(path) as file:
        return yaml.safe_load(file)


def biosphere_flows() -> dict[tuple, tuple[str, tuple]]:
    """Collect every flow referenced by the packaged CF files.

    The ecoinvent biosphere uses one spelling per flow, while the CF files were
    authored independently and occasionally differ in case. Keying on the
    lower-cased name and categories keeps the synthetic biosphere unambiguous,
    which is what ``bw2io`` needs for unique linking.
    """
    flows: dict[tuple, tuple[str, tuple]] = {}
    for path in packaged_yaml_files():
        for row in load_rows(path):
            name = str(row["name"]).strip()
            categories = tuple(
                part.strip() for part in str(row["categories"]).split("::")
            )
            key = (
                name.lower(),
                tuple(category.lower() for category in categories),
            )
            flows.setdefault(key, (name, categories))
    return flows


class _SqliteConnectionTracker:
    """Record every connection opened through the wrapped ``connect``."""

    def __init__(self, connect):
        self._connect = connect
        self.connections = []

    def connect(self, *args, **kwargs):
        connection = self._connect(*args, **kwargs)
        self.connections.append(connection)
        return connection


@pytest.fixture(autouse=True)
def close_sqlite_connections(monkeypatch):
    """Close every sqlite connection a test opens.

    Two bw2data code paths leak connections:

    * ``SQLiteBackend.process()`` reads exchanges through a raw
      ``sqlite3.connect`` handle that never leaves the function.
    * peewee keeps the connection of each project's metadata databases open
      until the interpreter exits.

    Neither handle escapes, so the only way to release them is to track the
    connections at creation time and close them when the test ends. Patching
    ``sqlite3.connect`` covers both, because peewee calls it through the module.
    """
    import sqlite3

    tracker = _SqliteConnectionTracker(sqlite3.connect)
    monkeypatch.setattr(sqlite3, "connect", tracker.connect)

    yield

    while tracker.connections:
        tracker.connections.pop().close()


@pytest.fixture
def project():
    """Yield a fresh, empty Brightway project and delete it afterwards."""
    name = f"aesa-tests-{uuid.uuid4().hex[:10]}"
    bd.projects.set_current(name)
    yield name
    bd.projects.delete_project(name, delete_dir=True)


@pytest.fixture
def biosphere(project):
    """Write a synthetic ``biosphere3`` built from the packaged CF files.

    The nitrogen fertiliser flow is left out: in ecoinvent it lives in the
    ``A_technosphere_flows`` database that ``add_aesa_pbs`` creates, so the
    directly fixated nitrogen method must link to that database instead.
    """
    flows = biosphere_flows()
    flows = {
        key: value
        for key, value in flows.items()
        if value != ("nitrogen fertilizer", ("inventory",))
    }
    bd.Database("biosphere3").write(
        {
            ("biosphere3", f"bio{i:05d}"): {
                "name": name,
                "categories": categories,
                "type": "emission",
                "unit": "kilogram",
                "exchanges": [],
            }
            for i, (name, categories) in enumerate(flows.values())
        }
    )
    return bd.Database("biosphere3")


@pytest.fixture
def aesa_methods(biosphere):
    """Install the AESA methods into the synthetic project."""
    from aesa_pbs.aesa_pbs import add_aesa_pbs

    add_aesa_pbs(verbose=False)
    return sorted(bw.methods)


@pytest.fixture(scope="session", autouse=True)
def close_project_database():
    """Close the project metadata database when the session ends.

    The project registry connection is recreated while the last test is torn
    down, so the per-test tracker no longer sees it; without this it stays open
    until the interpreter exits.
    """
    yield
    bd.projects.db.db.close()
