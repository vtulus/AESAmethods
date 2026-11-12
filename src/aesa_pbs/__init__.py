import importlib.metadata

__all__ = [
    "add_aesa_pbs",
    "get_nitrogenous_fertilizers",
    "update_nitrogen_fertilizer_exchanges",
    "remove_nitrogen_fertilizer_exchanges",
    "DataConverter",
]

try:
    __version__ = importlib.metadata.version("aesa_pbs")
except importlib.metadata.PackageNotFoundError:  # pragma: no cover
    # Package is used from a source checkout without being installed.
    __version__ = "0.0.0"

from .aesa_pbs import add_aesa_pbs
from .n_direct_fixation import (
    get_nitrogenous_fertilizers,
    remove_nitrogen_fertilizer_exchanges,
    update_nitrogen_fertilizer_exchanges,
)
from .data_converter import DataConverter
