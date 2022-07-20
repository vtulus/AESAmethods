import tempfile
import warnings
from pathlib import Path

import pandas as pd
import yaml

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_EXCELS = Path(DATA_DIR).resolve() / "excels"


class DumperBlankLine(yaml.SafeDumper):
    """HACK: insert blank lines between top-level objects.

    inspired by https://github.com/yaml/pyyaml/issues/127#issuecomment-525800484
    """

    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break()


class DirectoryDoesNotExist(OSError):
    "Raised when directory path doesn't exist."


class DataConverter:
    """Class to convert data from/to `*.xlsx` or `*.yaml` formats.

    Class reads characterization factors (CFs) data from
    an xlsx or yaml file into a `pandas.DataFrame` and
    contains methods to write it to an xlsx or yaml file.

    Parameters
    ----------
    filepath : str
        Absolute path to a file for conversion
    """

    def __init__(self, filepath: str) -> None:
        """Initialize an instance of a DataConverter"""
        if file_exists(filepath):
            self.filepath = Path(filepath)
        self.file_suffix = self.filepath.suffix

        if self.file_suffix == ".xlsx":
            self.data = self.from_excel()
        elif self.file_suffix == ".yaml":
            self.data = self.from_yaml()

    def from_excel(self) -> pd.DataFrame:
        """Read an xlsx file with 'name', 'categories' and 'amount' columns.

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
        data_clean = data_clean.drop_duplicates(keep="first", ignore_index=True)
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
        data_clean = data_clean.drop_duplicates(keep="first", ignore_index=True)
        return data_clean

    def to_yaml(self, outfilepath: str = None, verbose=True) -> None:
        """Write data to yaml file.

        Parameters
        ----------
        outfilepath : str, optional
            Absolute file path. If None is provided, uses input file name and default directory.
        verbose : bool, optional
            Print completion message, by default True
        """
        data_dict = self.data.to_dict(orient="records")
        if not outfilepath:
            filename = self.filepath.stem
            outfilepath = str(DATA_DIR) + f"/{filename}.yaml"

        if parent_dir_exists(outfilepath):
            output_file_path = Path(outfilepath)

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

    def to_excel(self, outfilepath: str = None, verbose=True) -> None:
        """Write data to xlsx file.

        Parameters
        ----------
        outfilepath : str, optional
            Absolute file path. If None is provided, uses input file name and default directory.
        verbose : bool, optional
            Print completion message, by default True
        """
        if not outfilepath:
            filename = self.filepath.stem
            outfilepath = str(DATA_EXCELS) + f"/{filename}.xlsx"

        if parent_dir_exists(outfilepath):
            output_file_path = Path(outfilepath)

        with pd.ExcelWriter(  # pylint: disable=abstract-class-instantiated
            output_file_path, mode="w", engine="openpyxl"
        ) as writer:
            self.data.to_excel(writer, index=False)
        if verbose:
            print(f"File created in {output_file_path}")


def file_exists(filepath: str) -> bool:
    "Check if file exists in passed filepath."
    if not Path(filepath).is_file():
        raise FileNotFoundError(f"{filepath} does not exist.")
    return True


def parent_dir_exists(filepath: str) -> bool:
    """Check if parent directory of the passed filepath exists.

    inspired by https://stackoverflow.com/a/34102855/14485040
    """
    dirname = Path(filepath).resolve().parent
    try:
        with tempfile.TemporaryFile(dir=dirname):
            pass
        return True
    except EnvironmentError as exc:
        raise DirectoryDoesNotExist(
            f"{dirname} does not exist. Must provide a path to an existing directory."
        ) from exc
