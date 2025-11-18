import os
import pandas as pd
import pytest
import yaml

from aesa_pbs.data_converter import DataConverter

# Sample data for testing
YAML_DATA = """
- name: flow1
  categories: [cat1, cat2]
  amount: 1.0
- name: flow2
  categories: [cat3, cat4]
  amount: 2.0
"""

EXCEL_DATA = {
    "name": ["flow1", "flow2"],
    "categories": ["[cat1, cat2]", "[cat3, cat4]"],
    "amount": [1.0, 2.0],
}

MISSING_DATA = {
    "name": ["flow1", None],
    "categories": ["[cat1, cat2]", "[cat3, cat4]"],
    "amount": [1.0, 2.0],
}

DUPLICATE_DATA = {
    "name": ["flow1", "flow1"],
    "categories": ["[cat1, cat2]", "[cat1, cat2]"],
    "amount": [1.0, 1.0],
}


@pytest.fixture
def create_test_files(tmp_path):
    """Create temporary YAML and Excel files for testing."""
    yaml_file = tmp_path / "test.yaml"
    with open(yaml_file, "w") as f:
        f.write(YAML_DATA)

    excel_file = tmp_path / "test.xlsx"
    pd.DataFrame(EXCEL_DATA).to_excel(excel_file, index=False)

    missing_data_file = tmp_path / "missing.xlsx"
    pd.DataFrame(MISSING_DATA).to_excel(missing_data_file, index=False)

    duplicate_data_file = tmp_path / "duplicate.xlsx"
    pd.DataFrame(DUPLICATE_DATA).to_excel(duplicate_data_file, index=False)

    return {
        "yaml": str(yaml_file),
        "excel": str(excel_file),
        "missing": str(missing_data_file),
        "duplicate": str(duplicate_data_file),
    }


def test_from_yaml(create_test_files):
    """Test reading data from a YAML file."""
    converter = DataConverter(create_test_files["yaml"])
    assert isinstance(converter.data, pd.DataFrame)
    assert len(converter.data) == 2


def test_from_excel(create_test_files):
    """Test reading data from an Excel file."""
    converter = DataConverter(create_test_files["excel"])
    assert isinstance(converter.data, pd.DataFrame)
    assert len(converter.data) == 2


def test_handle_missing_data(create_test_files):
    """Test that missing data is handled correctly."""
    converter = DataConverter(create_test_files["missing"])
    assert len(converter.data) == 1


def test_handle_duplicate_data(create_test_files):
    """Test that duplicate data is handled correctly."""
    converter = DataConverter(create_test_files["duplicate"])
    assert len(converter.data) == 1


def test_to_yaml(create_test_files, tmp_path):
    """Test writing data to a YAML file."""
    converter = DataConverter(create_test_files["excel"])
    output_file = tmp_path / "output.yaml"
    converter.to_yaml(outfilepath=str(output_file))
    assert os.path.exists(output_file)

    with open(output_file, "r") as f:
        data = yaml.safe_load(f)
    assert len(data) == 2


def test_to_excel(create_test_files, tmp_path):
    """Test writing data to an Excel file."""
    converter = DataConverter(create_test_files["yaml"])
    output_file = tmp_path / "output.xlsx"
    converter.to_excel(outfilepath=str(output_file))
    assert os.path.exists(output_file)

    df = pd.read_excel(output_file)
    assert len(df) == 2
