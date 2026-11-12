import importlib.resources

from aesa_pbs import __version__
from aesa_pbs.aesa_pbs import generate_excel_from_yaml


def test_version_is_available():
    """Test that the package version resolves to a non-empty string."""
    assert isinstance(__version__, str)
    assert __version__


def test_generate_excel_from_yaml(tmp_path):
    """Test that a packaged YAML file is converted to Excel in the output dir."""
    with importlib.resources.path(
        "aesa_pbs.data", "aesa_FreshwaterUse_Global.yaml"
    ) as yaml_path:
        generate_excel_from_yaml(filepath=str(yaml_path), outdir=str(tmp_path))

    excel_file = tmp_path / "aesa_FreshwaterUse_Global.xlsx"
    assert excel_file.exists()
