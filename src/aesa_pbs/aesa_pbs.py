import functools
import json
from pathlib import Path

import brightway2 as bw
from bw2io import ExcelLCIAImporter, strategies
from prettytable import PrettyTable

from .biosphere import get_biosphere_database
from .data_converter import DATA_DIR, DATA_EXCELS, DataConverter
from .version import __version__


# write_methods() does not write metadata other than "description", "unit" and "filename"
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
    #  changelog: changelog,
    #  implemented_by: author implemented}
    # filename: excel file with categories

    categories = {
        (
            (
                "AESA (PBs-LCIA)",
                str(__version__),
                "climate change",
                "atmospheric CO2 concentration",
            ),
            "ppm",
            json.dumps(
                {
                    "overview": "",
                    "authors": RYBERG_ET_AL,
                    "doi": DOI_RYBERG,
                    "current_version": "v" + __version__,
                    "changelog": changelog,
                    "implemented_by": MAINTAINER,
                }
            ),
            "aesa_ClimateChange_AtmosphericCO2Concentration.xlsx",
        ),
        (
            (
                "AESA (PBs-LCIA)",
                str(__version__),
                "climate change",
                "energy imbalance at top-of-atmosphere",
            ),
            "Wm-2",
            json.dumps(
                {
                    "overview": "",
                    "authors": RYBERG_ET_AL,
                    "doi": DOI_RYBERG,
                    "current_version": "v" + __version__,
                    "changelog": changelog,
                    "implemented_by": MAINTAINER,
                }
            ),
            "aesa_ClimateChange_EnergyImbalance.xlsx",
        ),
        (
            (
                "AESA (PBs-LCIA)",
                str(__version__),
                "ozone depletion",
                "stratospheric O3 concentration",
            ),
            "Dobson unit",
            json.dumps(
                {
                    "overview": "",
                    "authors": RYBERG_ET_AL,
                    "doi": DOI_RYBERG,
                    "current_version": "v" + __version__,
                    "changelog": changelog,
                    "implemented_by": MAINTAINER,
                }
            ),
            "aesa_OzoneDepletion_StratosphericO3Concentration.xlsx",
        ),
        (
            (
                "AESA (PBs-LCIA)",
                str(__version__),
                "ocean acidification",
                "carbonate ion concentration",
            ),
            "omega aragonite",
            json.dumps(
                {
                    "overview": "",
                    "authors": RYBERG_ET_AL,
                    "doi": DOI_RYBERG,
                    "current_version": "v" + __version__,
                    "changelog": changelog,
                    "implemented_by": MAINTAINER,
                }
            ),
            "aesa_OceanAcidification_CarbontateIonConcentration.xlsx",
        ),
        (
            ("AESA (PBs-LCIA)", str(__version__), "biogeochemical flows", "phosphorus"),
            "Tg P",
            json.dumps(
                {
                    "overview": "P flow from freshwater systems into the ocean",
                    "authors": RYBERG_ET_AL,
                    "doi": DOI_RYBERG,
                    "current_version": "v" + __version__,
                    "changelog": changelog,
                    "implemented_by": MAINTAINER,
                }
            ),
            "aesa_BiogeochemicalFlows_P.xlsx",
        ),
        (
            (
                "AESA (PBs-LCIA)",
                str(__version__),
                "biogeochemical flows",
                "nitrogen",
                "inverse modelling, surface water",
            ),
            "Tg N",
            json.dumps(
                {
                    "overview": "industrial and intentional biological fixation of N",
                    "authors": RYBERG_ET_AL,
                    "doi": DOI_RYBERG,
                    "current_version": "v" + __version__,
                    "changelog": changelog,
                    "implemented_by": MAINTAINER,
                }
            ),
            "aesa_BiogeochemicalFlows_N_inverseModelling_surfaceWater.xlsx",
        ),
        (
            (
                "AESA (PBs-LCIA)",
                str(__version__),
                "biogeochemical flows",
                "nitrogen",
                "directly fixated",
            ),
            "Tg N",
            json.dumps(
                {
                    "overview": "direct quantification of industrial and intentional biological fixation of N fertilizer",
                    "authors": MAINTAINER,
                    "doi": None,
                    "current_version": "v" + __version__,
                    "changelog": changelog,
                    "implemented_by": MAINTAINER,
                }
            ),
            "aesa_BiogeochemicalFlows_N_directlyFixated.xlsx",
        ),
        (
            ("AESA (PBs-LCIA)", str(__version__), "land-system change", "global"),
            "% forested land",
            json.dumps(
                {
                    "overview": "Unit: area of forested land as % of original forest cover",
                    "authors": RYBERG_ET_AL,
                    "doi": DOI_RYBERG,
                    "current_version": "v" + __version__,
                    "changelog": changelog,
                    "implemented_by": MAINTAINER,
                }
            ),
            "aesa_LandSystemChange_Global.xlsx",
        ),
        (
            ("AESA (PBs-LCIA)", str(__version__), "freshwater use", "global"),
            "km3",
            json.dumps(
                {
                    "overview": "Unit: Maximum amount of consumptive blue water use per year",
                    "authors": RYBERG_ET_AL,
                    "doi": DOI_RYBERG,
                    "current_version": "v" + __version__,
                    "changelog": changelog,
                    "implemented_by": MAINTAINER,
                }
            ),
            "aesa_FreshwaterUse_Global.xlsx",
        ),
        (
            (
                "AESA (PBs-LCIA)",
                str(__version__),
                "change in biosphere integrity",
                "functional diversity",
                "total",
            ),
            "% BII loss",
            json.dumps(
                {
                    "overview": "Unit: % of Biosphere Intactness Index loss",
                    "authors": GALAN_ET_AL,
                    "doi": DOI_GALAN,
                    "current_version": "v" + __version__,
                    "changelog": changelog,
                    "implemented_by": MAINTAINER,
                }
            ),
            "aesa_ChangeBiosphereIntegrity_FunctionalDiversity_Hierarchist.xlsx",
        ),
        (
            (
                "AESA (PBs-LCIA)",
                str(__version__),
                "change in biosphere integrity",
                "functional diversity",
                "direct land use",
            ),
            "% BII loss",
            json.dumps(
                {
                    "overview": "Unit: % of Biosphere Intactness Index loss",
                    "authors": GALAN_ET_AL,
                    "doi": DOI_GALAN,
                    "current_version": "v" + __version__,
                    "changelog": changelog,
                    "implemented_by": MAINTAINER,
                }
            ),
            "aesa_ChangeBiosphereIntegrity_FunctionalDiversity_Hierarchist_land_use.xlsx",
        ),
        (
            (
                "AESA (PBs-LCIA)",
                str(__version__),
                "change in biosphere integrity",
                "functional diversity",
                "CO2eq emissions",
            ),
            "% BII loss",
            json.dumps(
                {
                    "overview": "Unit: % of Biosphere Intactness Index loss",
                    "authors": GALAN_ET_AL,
                    "doi": DOI_GALAN,
                    "current_version": "v" + __version__,
                    "changelog": changelog,
                    "implemented_by": MAINTAINER,
                }
            ),
            "aesa_ChangeBiosphereIntegrity_FunctionalDiversity_Hierarchist_CO2eq_emissions.xlsx",
        ),
    }

    for cat in categories:
        generate_excel_from_yaml(
            filepath=Path(str(DATA_DIR) + f"/{cat[-1]}").with_suffix(".yaml")
        )

    for cat in categories:
        print(f"Adding {cat[0]}")
        method = ExcelLCIAImporter(
            filepath=DATA_EXCELS / cat[-1],
            name=cat[0],
            unit=cat[1],
            description=cat[2],
            filename=cat[-1],
        )

        # flows of the method for directly fixated nitrogen may not be linked
        # because of the missing database `A_technosphere_flows`
        if all(
            map(
                lambda item: item in str(cat[0]).lower(),
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
        assert (
            len(list(method.unlinked)) == 0
        ), f"{cat[0]} method contains unlinked flows. Method could not be installed."

        # write method
        method.write_methods(overwrite=True, verbose=verbose)
        if verbose:
            print("")


# def get_changelog():
#     """Get changelog information from CHANGELOG.md

#     Returns
#     -------
#     str
#         Changelog information
#     """
#     with open(CHANGELOG, "r") as f:
#         return f.read()


# refs
RYBERG_ET_AL = "Ryberg, M. W.; Owsianiak, M.; Richardson, K.; Hauschild, M. Z."
GALAN_ET_AL = "Galán-Martín, Á.; Tulus, V.; Díaz, I.; Pozo, C.; Pérez-Ramírez, J.; Guillén-Gosálbez, G."
DOI_RYBERG = "https://doi.org/10.1016/j.ecolind.2017.12.065"
DOI_GALAN = "https://doi.org/10.1016/j.oneear.2021.04.001"
MAINTAINER = "Tulus, V."
# changelog = get_changelog()
changelog = "Find changelog here: https://github.com/vtulus/AESAmethods/blob/master/CHANGELOG.md"


def drop_empty_lines(data):
    """Strategy for removing empty lines in excel.

    Returns modified data
    """
    for method in data:
        method["exchanges"] = [obj for obj in method["exchanges"] if obj["name"]]
    return data


def warning_directly_fixated_n() -> None:
    """Printing a warning regarding a missing database.
    """
    t = PrettyTable(["Warning"])
    t.add_row(
        [
            "The method for quantification of directly fixated nitrogen\n"
            "requires an additional database `A_technosphere_flows`.\n"
            "This database was not found in the current project.\n"
            "It will be generated now.\n"
            # "No further actions needed."
            "\nNext steps:\n"
            "1. Use `aesa_pbs.get_nitrogenous_fertilizers()` to filter activities\n"
            "\tproducing nitrogenous fertilizers in a specific background database.\n"
            "2. Use `aesa_pbs.update_nitrogen_fertilizer_exchanges()` to modify those activities.\n\n"
            "Optionally, \n"
            "modified activities can be cleaned with `aesa_pbs.remove_nitrogen_fertilizer_exchanges()`."
        ]
    )
    # align text to the left
    t.align = "l"
    print(t)


def generate_excel_from_yaml(filepath: str) -> None:
    """Generate xlsx file from yaml file.

    Parameters
    ----------
    filepath : str
        Absolute path to a file for conversion
    """
    convert = DataConverter(filepath)
    convert.to_excel(verbose=True)
