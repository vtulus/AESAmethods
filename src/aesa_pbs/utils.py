import warnings
from pathlib import Path

import pandas as pd
import yaml

DATA_EXCELS = Path(__file__).resolve().parent / "data_excels"
DATA_DIR = Path(__file__).resolve().parent / "data"


class DataConverter:
    """Class to convert data from/to *.xlsx or *.yaml formats.

    Class reads characterization factors (CFs) data from
    an xlsx or yaml file into a `pandas.DataFrame` and
    contains methods to write it to an xlsx or yaml file.

    Parameters
        ----------
        filepath : Path
            Path to a file for conversion
    """

    def __init__(self, filepath: Path) -> None:
        """Initialize an instance of a DataConverter"""
        self.filepath = check_filepath(filepath)
        self.file_suffix = self.filepath.suffix

        if self.file_suffix == ".xlsx":
            self.data = self.from_excel()
        elif self.file_suffix == ".yaml":
            self.data = self.from_yaml()

    # TODO: check for duplicates (drop duplicates)
    def from_excel(self) -> pd.DataFrame:
        """Read an excel file with 'name', 'categories' and 'amount' columns.

        Returns
        -------
        pd.DataFrame
            Data from excel file
        """
        data = pd.read_excel(self.filepath)
        assert sorted(list(data.columns)) == sorted(
            ["name", "categories", "amount"]
        ), "Excel file must contain only 'name', 'categories' and 'amount' columns."
        if data.isna().values.any():
            data_clean = data.dropna(axis=0, how="any")
            if data_clean.empty:
                raise ValueError(f"Data in {self.filepath} is not valid.")
            warnings.warn(
                f"\n\nSome data are missing in {self.filepath}."
                "\nRows with incomplete data are removed.\n"
            )
        else:
            data_clean = data
        return data_clean

    def from_yaml(self) -> pd.DataFrame:
        """Read an yaml file with 'name', 'categories' and 'amount' keys.

        Returns
        -------
        pd.DataFrame
            Data from yaml file
        """
        with open(self.filepath, "r") as file:
            loaded = yaml.safe_load(file)
        data = pd.DataFrame(loaded, columns=["name", "categories", "amount"])
        if data.isna().values.any():
            data_clean = data.dropna(axis=0, how="any")
            if data_clean.empty:
                raise ValueError(f"Data in {self.filepath} is not valid.")
            warnings.warn(
                f"\n\nSome data are missing in {self.filepath}."
                "\nRows with incomplete data are removed.\n"
            )
        else:
            data_clean = data
        return data_clean

    def to_yaml(self, filename: str = None, verbose=True) -> None:
        """Write data to yaml file.

        Parameters
        ----------
        filename : str, optional
            File name without extension. If None is provided, uses input file name.
        verbose : bool, optional
            Print completion message, by default True
        """
        data_dict = self.data.to_dict(orient="records")
        if not filename:
            filename = self.filepath.stem

        output_file_path = Path(str(DATA_DIR) + f"/{filename}.yaml")

        with open(output_file_path, "w") as file:
            yaml.dump(
                data_dict,
                file,
                Dumper=DumperBlankLine,
                default_flow_style=False,
                default_style=None,
                sort_keys=False,
                indent=None,
            )
        if verbose:
            print(f"File created in {output_file_path}")

    def to_excel(self, filename: str = None, verbose=True) -> None:
        """_summary_

        Parameters
        ----------
        filename : str, optional
            File name without extension. If None is provided, uses input file name.
        verbose : bool, optional
            Print completion message, by default True
        """
        if not filename:
            filename = self.filepath.stem

        output_file_path = Path(str(DATA_DIR) + f"/{filename}.xlsx")

        with pd.ExcelWriter( # pylint: disable=abstract-class-instantiated
            output_file_path, mode="w", engine="openpyxl"
        ) as writer:  
            self.data.to_excel(writer, index=False)
        if verbose:
            print(f"File created in {output_file_path}")


class DumperBlankLine(yaml.SafeDumper):
    """HACK: insert blank lines between top-level objects.

    inspired by https://github.com/yaml/pyyaml/issues/127#issuecomment-525800484
    """

    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break()


def check_filepath(filepath: Path) -> Path:
    "Check if file exists in passed filepath."

    if not Path(filepath).is_file():
        raise FileNotFoundError(f"{filepath} does not exist.")
    return filepath
