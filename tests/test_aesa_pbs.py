import importlib.resources
import json
from pathlib import Path

import brightway2 as bw
import bw2data as bd
import pandas as pd
import pytest

from aesa_pbs import __version__
from aesa_pbs.aesa_pbs import (
    MethodSpec,
    add_aesa_pbs,
    drop_empty_lines,
    generate_excel_from_yaml,
    warning_directly_fixated_n,
)
from aesa_pbs.biosphere import get_biosphere_database

from .conftest import load_rows, packaged_yaml_files


def test_version_is_available():
    """Test that the package version resolves to a non-empty string."""
    assert isinstance(__version__, str)
    assert __version__


def test_generate_excel_from_yaml(tmp_path):
    """A packaged YAML file is converted to Excel in the output dir."""
    with importlib.resources.path(
        "aesa_pbs.data", "aesa_FreshwaterUse_Global.yaml"
    ) as yaml_path:
        generate_excel_from_yaml(filepath=str(yaml_path), outdir=str(tmp_path))

    excel_file = tmp_path / "aesa_FreshwaterUse_Global.xlsx"
    assert excel_file.exists()


@pytest.mark.parametrize("yaml_path", packaged_yaml_files(), ids=lambda path: path.stem)
def test_packaged_yaml_files_convert_to_excel(yaml_path: Path, tmp_path):
    """Every packaged YAML file converts to a non-empty Excel sheet."""
    generate_excel_from_yaml(filepath=str(yaml_path), outdir=str(tmp_path))

    excel_file = tmp_path / (yaml_path.stem + ".xlsx")
    assert excel_file.exists()

    data = pd.read_excel(excel_file)
    assert {"name", "categories", "amount"}.issubset(data.columns)
    assert not data.empty
    assert data["amount"].notna().all()


def test_packaged_yaml_files_have_unique_flows():
    """No packaged file contains duplicated name/categories/amount rows."""
    for path in packaged_yaml_files():
        rows = pd.DataFrame(load_rows(path))
        assert not rows.empty, path.name
        assert not rows.duplicated().any(), path.name


def test_method_spec_full_name_and_description():
    """MethodSpec builds the Brightway method name and metadata blob."""
    spec = MethodSpec(
        name_parts=("climate change", "atmospheric CO2 concentration"),
        unit="ppm",
        overview="overview text",
        authors="Someone",
        doi="https://doi.org/10.1234/example",
        filename="example.yaml",
    )

    assert spec.full_name() == (
        "AESA (PBs-LCIA)",
        __version__,
        "climate change",
        "atmospheric CO2 concentration",
    )

    description = json.loads(spec.description())
    assert description["overview"] == "overview text"
    assert description["authors"] == "Someone"
    assert description["doi"] == "https://doi.org/10.1234/example"
    assert description["current_version"] == "v" + __version__
    assert "implemented_by" in description


def test_drop_empty_lines_removes_nameless_exchanges():
    """Strategy drops exchanges without a name."""
    data = [
        {
            "exchanges": [
                {"name": "Carbon dioxide"},
                {"name": ""},
                {"name": None},
                {"amount": 1},
            ]
        }
    ]

    assert drop_empty_lines(data) == [{"exchanges": [{"name": "Carbon dioxide"}]}]


def test_drop_empty_lines_keeps_empty_exchange_lists():
    """Methods without exchanges survive the strategy."""
    assert drop_empty_lines([{"exchanges": []}]) == [{"exchanges": []}]


def test_warning_directly_fixated_n(capsys):
    """The warning explains how to complete the nitrogen method setup."""
    warning_directly_fixated_n()

    printed = capsys.readouterr().out
    assert "A_technosphere_flows" in printed
    assert "get_nitrogenous_fertilizers" in printed
    assert "update_nitrogen_fertilizer_exchanges" in printed


def test_get_biosphere_database_requires_biosphere(project):
    """A missing biosphere3 database is reported as an error."""

    with pytest.raises(AssertionError, match="ecoinvent biosphere flows"):
        get_biosphere_database()

    bd.Database("biosphere3").write({})
    assert get_biosphere_database() == []


def test_add_aesa_pbs_installs_all_methods(aesa_methods):
    """All 12 AESA methods are registered with metadata."""

    assert len(aesa_methods) == 12
    assert all(
        method[:2] == ("AESA (PBs-LCIA)", __version__) for method in aesa_methods
    )

    for method in aesa_methods:
        metadata = bw.methods[method]
        assert metadata["unit"]
        assert metadata["filename"]

        description = json.loads(metadata["description"])
        assert description["current_version"] == "v" + __version__
        assert description["authors"]
        assert "changelog" in description


def test_add_aesa_pbs_methods_have_characterisation_factors(aesa_methods):
    """Every installed method has at least one exchange."""

    for method in aesa_methods:
        assert bw.Method(method).load(), method


def test_add_aesa_pbs_creates_technosphere_flows_database(aesa_methods):
    """The directly fixated nitrogen method gets its missing flow database."""

    assert "A_technosphere_flows" in bd.databases

    flows = list(bd.Database("A_technosphere_flows"))
    assert [flow["name"] for flow in flows] == ["nitrogen fertilizer"]
    assert flows[0]["unit"] == "kilogram"
    assert flows[0]["categories"] == ("inventory",)


def test_add_aesa_pbs_links_directly_fixated_nitrogen(aesa_methods):
    """The directly fixated nitrogen method links to its flow database."""

    method = (
        "AESA (PBs-LCIA)",
        __version__,
        "biogeochemical flows",
        "nitrogen",
        "directly fixated",
    )
    assert method in bw.methods

    # Method.load() stores node IDs; iterating the Method resolves IDs to nodes.
    exchanges = list(bw.Method(method))
    assert exchanges
    assert all(exchange[0].key[0] == "A_technosphere_flows" for exchange in exchanges)


def test_add_aesa_pbs_runs_on_existing_flow_database(biosphere):
    """A second installation does not duplicate the flow database."""

    add_aesa_pbs(verbose=False)
    add_aesa_pbs(verbose=False)

    assert len(list(bd.Database("A_technosphere_flows"))) == 1


def test_add_aesa_pbs_verbose_output(biosphere, capsys):
    """Verbose installation reports each method it adds."""
    add_aesa_pbs(verbose=True)

    printed = capsys.readouterr().out
    assert "Adding ('AESA (PBs-LCIA)'" in printed
    assert "freshwater use" in printed
