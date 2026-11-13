import functools
import importlib.resources as importlib_resources
import json
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path

import brightway2 as bw
from bw2io import ExcelLCIAImporter, strategies
from prettytable import PrettyTable

from .biosphere import get_biosphere_database
from .data_converter import DataConverter
from . import __version__


@dataclass(frozen=True, slots=True)
class MethodSpec:
    name_parts: tuple[str, ...]
    unit: str
    overview: str
    authors: str
    doi: str | None
    filename: str

    def description(self) -> str:
        return json.dumps(
            {
                "overview": self.overview,
                "authors": self.authors,
                "doi": self.doi,
                "current_version": "v" + __version__,
                "changelog": CHANGELOG,
                "implemented_by": MAINTAINER,
            }
        )

    def full_name(self) -> tuple[str, ...]:
        return ("AESA (PBs-LCIA)", str(__version__), *self.name_parts)


# write_methods() does not write metadata other than "description",
# "unit" and "filename"
# store everything in the description using json.dumps()
# later can be retrieved with json.loads()
def add_aesa_pbs(verbose=True):
    """Add AESA (PBs-LCIA) method to a bw project.
    Included categories are:
    - climate change
        - atmospheric CO2 concentration
        - energy imbalance at top-of-atmosphere
    - ozone depletion
        - stratospheric O3 concentration
    - ocean acidification
        - carbonate ion concentration
    - biogeochemical flows
        - phosphorus
        - nitrogen
            - inverse modelling, surface water
            - directly fixated
    - land-system change
        - global
    - freshwater use
        - global
    - change in biosphere integrity
        - functional diversity
            - total
            - direct land use
            - CO2eq emissions

    Parameters
    ----------
    verbose : bool, optional
        Display applied strategies, by default True
    """
    get_biosphere_database()

    # In categories:
    # name: (method, version, categories)
    # unit: unit
    # description:
    # {overview: "overview text",
    #  authors: of the method/category,
    #  doi: doi of published work,
    #  current_version: current version
    #  changelog: CHANGELOG,
    #  implemented_by: author implemented}
    # filename: excel file with categories

    methods: list[MethodSpec] = [
        MethodSpec(
            name_parts=("climate change", "atmospheric CO2 concentration"),
            unit="ppm",
            overview="",
            authors=RYBERG_ET_AL,
            doi=DOI_RYBERG,
            filename="aesa_ClimateChange_AtmosphericCO2Concentration.xlsx",
        ),
        MethodSpec(
            name_parts=("climate change", "energy imbalance at top-of-atmosphere"),
            unit="Wm-2",
            overview="",
            authors=RYBERG_ET_AL,
            doi=DOI_RYBERG,
            filename="aesa_ClimateChange_EnergyImbalance.xlsx",
        ),
        MethodSpec(
            name_parts=("ozone depletion", "stratospheric O3 concentration"),
            unit="Dobson unit",
            overview="",
            authors=RYBERG_ET_AL,
            doi=DOI_RYBERG,
            filename="aesa_OzoneDepletion_StratosphericO3Concentration.xlsx",
        ),
        MethodSpec(
            name_parts=("ocean acidification", "carbonate ion concentration"),
            unit="omega aragonite",
            overview="",
            authors=RYBERG_ET_AL,
            doi=DOI_RYBERG,
            filename="aesa_OceanAcidification_CarbontateIonConcentration.xlsx",
        ),
        MethodSpec(
            name_parts=("biogeochemical flows", "phosphorus"),
            unit="Tg P",
            overview="P flow from freshwater systems into the ocean",
            authors=RYBERG_ET_AL,
            doi=DOI_RYBERG,
            filename="aesa_BiogeochemicalFlows_P.xlsx",
        ),
        MethodSpec(
            name_parts=(
                "biogeochemical flows",
                "nitrogen",
                "inverse modelling, surface water",
            ),
            unit="Tg N",
            overview="industrial and intentional biological fixation of N",
            authors=RYBERG_ET_AL,
            doi=DOI_RYBERG,
            filename="aesa_BiogeochemicalFlows_N_inverseModelling_surfaceWater.xlsx",
        ),
        MethodSpec(
            name_parts=(
                "biogeochemical flows",
                "nitrogen",
                "directly fixated",
            ),
            unit="Tg N",
            overview=(
                "direct quantification of industrial and intentional"
                " biological fixation of N fertilizer"
            ),
            authors=MAINTAINER,
            doi=None,
            filename="aesa_BiogeochemicalFlows_N_directlyFixated.xlsx",
        ),
        MethodSpec(
            name_parts=("land-system change", "global"),
            unit="% forested land",
            overview="Unit: area of forested land as % of original forest cover",
            authors=RYBERG_ET_AL,
            doi=DOI_RYBERG,
            filename="aesa_LandSystemChange_Global.xlsx",
        ),
        MethodSpec(
            name_parts=("freshwater use", "global"),
            unit="km3",
            overview="Unit: Maximum amount of consumptive blue water use per year",
            authors=RYBERG_ET_AL,
            doi=DOI_RYBERG,
            filename="aesa_FreshwaterUse_Global.xlsx",
        ),
        MethodSpec(
            name_parts=(
                "change in biosphere integrity",
                "functional diversity",
                "total",
            ),
            unit="% BII loss",
            overview="Unit: % of Biosphere Intactness Index loss",
            authors=GALAN_ET_AL,
            doi=DOI_GALAN,
            filename="aesa_ChangeBiosphereIntegrity_FunctionalDiversity_Hierarchist.xlsx",
        ),
        MethodSpec(
            name_parts=(
                "change in biosphere integrity",
                "functional diversity",
                "direct land use",
            ),
            unit="% BII loss",
            overview="Unit: % of Biosphere Intactness Index loss",
            authors=GALAN_ET_AL,
            doi=DOI_GALAN,
            filename="aesa_ChangeBiosphereIntegrity_FunctionalDiversity_Hierarchist_land_use.xlsx",
        ),
        MethodSpec(
            name_parts=(
                "change in biosphere integrity",
                "functional diversity",
                "CO2eq emissions",
            ),
            unit="% BII loss",
            overview="Unit: % of Biosphere Intactness Index loss",
            authors=GALAN_ET_AL,
            doi=DOI_GALAN,
            filename="aesa_ChangeBiosphereIntegrity_FunctionalDiversity_Hierarchist_CO2eq_emissions.xlsx",
        ),
    ]

    temp_dir = tempfile.mkdtemp()
    try:
        for spec in methods:
            yaml_filename = Path(spec.filename).with_suffix(".yaml").name
            with importlib_resources.path("aesa_pbs.data", yaml_filename) as yaml_path:
                generate_excel_from_yaml(filepath=str(yaml_path), outdir=temp_dir)

        for spec in methods:
            if verbose:
                print(f"Adding {spec.full_name()}")
            excel_path = Path(temp_dir) / spec.filename
            method = ExcelLCIAImporter(
                filepath=excel_path,
                name=spec.full_name(),
                unit=spec.unit,
                description=spec.description(),
                filename=spec.filename,
            )

            # flows of the method for directly fixated nitrogen may not be linked
            # because of the missing database `A_technosphere_flows`
            if all(
                map(
                    lambda item: item in " ".join(spec.full_name()).lower(),
                    ["nitrogen", "directly fixated"],
                )
            ):
                if "A_technosphere_flows" not in bw.databases:
                    # throw a warning and install the missing database
                    warning_directly_fixated_n()
                    # write new database
                    bw.Database("A_technosphere_flows").write(
                        {
                            ("A_technosphere_flows", "n-fert"): {  # (db name, code)
                                "name": "nitrogen fertilizer",
                                "unit": "kilogram",
                                "type": "inventory flow",
                                "categories": ("inventory",),
                            }
                        }
                    )
                # apply strategies
                method.apply_strategies(
                    method.strategies
                    + [
                        drop_empty_lines,
                        functools.partial(
                            strategies.link_iterable_by_fields,
                            other=bw.Database("A_technosphere_flows"),
                            kind="biosphere",
                            fields=("name", "categories"),
                        ),
                    ],
                    verbose=verbose,
                )
            else:
                # apply strategies
                method.apply_strategies(
                    method.strategies + [drop_empty_lines], verbose=verbose
                )

            # confirm that everything is correctly linked
            assert len(list(method.unlinked)) == 0, (
                f"{spec.full_name()} method contains unlinked flows; "
                "method could not be installed."
            )

            # write method
            method.write_methods(overwrite=True, verbose=verbose)
            if verbose:
                print("")
    finally:
        shutil.rmtree(temp_dir)


# def get_changelog():
#     """Get changelog information from CHANGELOG.md
#
#     Returns
#     -------
#     str
#         Changelog information
#     """
#     with open(CHANGELOG, "r") as f:
#         return f.read()


# refs
RYBERG_ET_AL = "Ryberg, M. W.; Owsianiak, M.; Richardson, K.; Hauschild, M. Z."
GALAN_ET_AL = (
    "Galán-Martín, Á.; Tulus, V.; Díaz, I.; Pozo, C.; Pérez-Ramírez, J.;"
    " Guillén-Gosálbez, G."
)
DOI_RYBERG = "https://doi.org/10.1016/j.ecolind.2017.12.065"
DOI_GALAN = "https://doi.org/10.1016/j.oneear.2021.04.001"
MAINTAINER = "Tulus, V."
# CHANGELOG = get_changelog()
CHANGELOG = "Find changelog here: https://github.com/vtulus/AESAmethods/blob/master/CHANGELOG.md"


def drop_empty_lines(data):
    """Strategy for removing empty lines in excel.

    Returns modified data
    """
    for method in data:
        method["exchanges"] = [obj for obj in method["exchanges"] if obj.get("name")]
    return data


# TODO: substitute the print with logging?
def warning_directly_fixated_n() -> None:
    """Printing a warning regarding a missing database."""
    message = PrettyTable(["Warning"])
    message.add_row(
        [
            "The method for quantification of directly fixated nitrogen\n"
            "requires an additional database `A_technosphere_flows`.\n"
            "This database was not found in the current project.\n"
            "It will be generated now.\n"
            # "No further actions needed."
            "\nNext steps:\n"
            "1. Use `aesa_pbs.get_nitrogenous_fertilizers()` to filter\n"
            "   activities producing nitrogenous fertilizers in a\n"
            "   specific background database.\n"
            "2. Use `aesa_pbs.update_nitrogen_fertilizer_exchanges()`\n"
            "   to modify those activities.\n\n"
            "Optionally, \n"
            "modified activities can be cleaned with\n"
            "   `aesa_pbs.remove_nitrogen_fertilizer_exchanges()`."
        ]
    )
    # align text to the left
    message.align = "l"
    print(message)


def generate_excel_from_yaml(filepath: str, outdir: str) -> None:
    """Generate xlsx file from yaml file.

    Parameters
    ----------
    filepath : str
        Absolute path to a file for conversion
    outdir : str
        Absolute path to the output directory
    """
    convert = DataConverter(filepath)
    output_filepath = Path(outdir) / (Path(filepath).stem + ".xlsx")
    convert.to_excel(outfilepath=output_filepath, verbose=False)
