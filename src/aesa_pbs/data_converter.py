import logging
from pathlib import Path

import pandas as pd
import yaml

logging.basicConfig(format="%(levelname)s: %(message)s")  # , level=logging.WARNING)


class DumperBlankLine(yaml.SafeDumper):
    """HACK: insert blank lines between top-level objects.

    inspired by https://github.com/yaml/pyyaml/issues/127#issuecomment-525800484
    """

    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break()


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
            self.data = self._from_excel()
        elif self.file_suffix == ".yaml":
            self.data = self._from_yaml()

    def _from_excel(self) -> pd.DataFrame:
        """Read an xlsx file with 'name', 'categories' and 'amount' columns.

        Returns
        -------
        pd.DataFrame
            Data from excel file
        """
        data = pd.read_excel(self.filepath)
        return _sanitize(data, self.filepath.name)

    def _from_yaml(self) -> pd.DataFrame:
        """Read an yaml file with 'name', 'categories' and 'amount' keys.

        Returns
        -------
        pd.DataFrame
            Data from yaml file
        """
        with open(self.filepath, "r") as file:
            loaded = yaml.safe_load(file)
        data = pd.DataFrame(loaded, columns=["name", "categories", "amount"])
        return _sanitize(data, self.filepath.name)

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
            dir_path = self.filepath.resolve().parent
            outfilepath = str(dir_path) + f"/{filename}.yaml"
        _validate_extension(outfilepath, ".yaml")

        make_dir(Path(outfilepath).resolve().parent)  # make directories if missing
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
            dir_path = self.filepath.resolve().parent
            outfilepath = str(dir_path) + f"/excels/{filename}.xlsx"
        _validate_extension(outfilepath, ".xlsx")

        make_dir(Path(outfilepath).resolve().parent)  # make directories if missing
        output_file_path = Path(outfilepath)

        with pd.ExcelWriter(  # pylint: disable=abstract-class-instantiated
            output_file_path, mode="w", engine="openpyxl"
        ) as writer:
            self.data.to_excel(writer, index=False)
        if verbose:
            print(f"File created in {output_file_path}")


def _validate_extension(filepath: str, extension: str) -> None:
    """Validate if filepath extension is correct.

    Parameters
    ----------
    filepath : str
        Absolute file path.
    extension : str
        Desired extension of the file.
    """
    assert (
        Path(filepath).suffix == extension
    ), f"Filepath extension ('{Path(filepath).suffix}') is not valid. Must be '{extension}'."


def _sanitize(data: pd.DataFrame, filename: str) -> pd.DataFrame:
    """Check for missing values and duplicated rows in the data.

    Uses `remove_missing()` and `remove_duplicates()`.

    Parameters
    ----------
    data : pd.DataFrame
        Data to sanitize
    filename : str
        Name of the file from where the data is retrieved

    Returns
    -------
    pd.DataFrame
        Sanitized data without missing values, nor duplicates
    """
    assert {"name", "categories", "amount"}.issubset(
        data.columns
    ), "Data must contain 'name', 'categories' and 'amount' column labels."
    data = data[["name", "categories", "amount"]]  # the extra columns are dropped

    # "amount" column should have only numeric values,
    # to_numeric() converts non-numeric values to NaN
    data["amount"] = pd.to_numeric(data["amount"], errors="coerce")
    sanitized_data = _remove_missing(data, filename)
    sanitized_data = _remove_duplicates(sanitized_data, filename)
    return sanitized_data


def _remove_missing(data: pd.DataFrame, filename: str) -> pd.DataFrame:
    """Remove rows containing NaN values.

    Parameters
    ----------
    data : pd.DataFrame
        Data to check for missing values
    filename : str
        Name of the file from where the data is retrieved

    Returns
    -------
    pd.DataFrame
        Clean data without missing values

    Raises
    ------
    ValueError
        If the resulting DataFrame is empty
    """
    missing_data = data[data.isna().any(axis=1)]
    if missing_data.empty:
        clean_data = data
    else:
        clean_data = data.dropna(axis=0, how="any")
        if not missing_data.isna().values.all():
            message_missing = (
                f"Some data is missing (or invalid) in {filename} "
                "(see below incomplete sets):\n"
            )
            message_missing += missing_data.to_markdown(
                index=False, tablefmt="pretty", stralign="left"
            )
            message_missing += "\nNote: These sets will be omitted.\n"
            logging.warning(message_missing)
    if clean_data.empty:
        raise ValueError(f"Data in {filename} is not valid.")
    return clean_data


def _remove_duplicates(data: pd.DataFrame, filename: str) -> pd.DataFrame:
    """Remove duplicated rows.

    Parameters
    ----------
    data : pd.DataFrame
        Data to check for duplicated rows.
    filename : str
        Name of the file from where the data is retrieved

    Returns
    -------
    pd.DataFrame
        Clean data without duplicates

    Raises
    ------
    ValueError
        If the resulting DataFrame is empty
    """
    duplicates = data[
        data.duplicated(subset=["name", "categories", "amount"], keep="first")
    ]
    if duplicates.empty:
        clean_data = data
    else:
        message_duplicate = f"Duplicated flows found in {filename} (see below):\n"
        message_duplicate += duplicates.to_markdown(
            index=False, tablefmt="pretty", stralign="left"
        )
        message_duplicate += "\nNote: All duplicates will be removed.\n"
        logging.warning(message_duplicate)
        clean_data = data.drop_duplicates(keep="first", ignore_index=True)
    if clean_data.empty:
        raise ValueError(f"Data in {filename} is not valid.")
    return clean_data


def file_exists(filepath: str) -> bool:
    "Check if file exists in passed filepath."
    if not Path(filepath).is_file():
        raise FileNotFoundError(f"{filepath} does not exist.")
    return True


def make_dir(dirpath: str) -> None:
    "Make missing directory(ies)."
    Path(dirpath).mkdir(parents=True, exist_ok=True)
