import json

from pathlib import Path

from bw2io import ExcelLCIAImporter

from .biosphere import get_biosphere_database
from .version import __version__

DATA_DIR = Path(__file__).resolve().parent / "data"
# CHANGELOG = Path(__file__).resolve().parents[2] / "CHANGELOG.md"


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
    - land-system change
        - global
    - freshwater use
        - global
    - change in biosphere integrity
        - functional diversity

    Parameters
    ----------
    verbose : bool, optional
        Display applied strategies, by default True
    """
    get_biosphere_database()

    # In categories:
    # name: (method, categories)
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
            ("AESA (PBs-LCIA)", "climate change", "atmospheric CO2 concentration"),
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
            ("AESA (PBs-LCIA)", "ozone depletion", "stratospheric O3 concentration"),
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
            ("AESA (PBs-LCIA)", "ocean acidification", "carbonate ion concentration"),
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
            ("AESA (PBs-LCIA)", "biogeochemical flows", "phosphorus"),
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
            ("AESA (PBs-LCIA)", "biogeochemical flows", "nitrogen"),
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
            "aesa_BiogeochemicalFlows_N.xlsx",
        ),
        (
            ("AESA (PBs-LCIA)", "land-system change", "global"),
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
            ("AESA (PBs-LCIA)", "freshwater use", "global"),
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
                "change in biosphere integrity",
                "functional diversity",
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
    }

    for cat in categories:
        print(f"Adding {cat[0]}")
        method = ExcelLCIAImporter(
            filepath=DATA_DIR / cat[-1],
            name=cat[0],
            unit=cat[1],
            description=cat[2],
            filename=cat[-1],
        )

        # apply strategies
        method.apply_strategies(method.strategies + [drop_empty_lines], verbose=verbose)

        # confirm that everything is correctly linked
        assert len(list(method.unlinked)) == 0

        # write method
        method.write_methods(overwrite=True, verbose=verbose)
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
