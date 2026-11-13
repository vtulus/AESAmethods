import bw2data as bd
import pytest

from aesa_pbs import (
    get_nitrogenous_fertilizers,
    remove_nitrogen_fertilizer_exchanges,
    update_nitrogen_fertilizer_exchanges,
)

NITROGEN_CPC = ["CPC", "3461: Mineral or chemical fertilizers, nitrogenous"]


@pytest.fixture
def technosphere(project):
    """Write a technosphere with the nitrogen flow and three activities."""

    bd.Database("A_technosphere_flows").write(
        {
            ("A_technosphere_flows", "n-fert"): {
                "name": "nitrogen fertilizer",
                "unit": "kilogram",
                "type": "inventory flow",
                "categories": ("inventory",),
            }
        }
    )

    bd.Database("test_technosphere").write(
        {
            ("test_technosphere", "fertiliser"): {
                "name": "Nitrogen fertiliser production",
                "unit": "kilogram",
                "classifications": [NITROGEN_CPC],
                "exchanges": [],
            },
            ("test_technosphere", "fertiliser_market"): {
                "name": "market for nitrogen fertiliser",
                "unit": "kilogram",
                "classifications": [NITROGEN_CPC],
                "exchanges": [],
            },
            ("test_technosphere", "wheat"): {
                "name": "Wheat production",
                "unit": "kilogram",
                "classifications": [["CPC", "0111: Wheat"]],
                "exchanges": [],
            },
        }
    )
    return bd.Database("test_technosphere")


def test_get_nitrogenous_fertilizers_skips_markets(technosphere):
    """Only non-market activities producing nitrogen fertiliser are returned."""
    activities = get_nitrogenous_fertilizers("test_technosphere")

    assert [activity["name"] for activity in activities] == [
        "Nitrogen fertiliser production"
    ]


def test_get_nitrogenous_fertilizers_without_classifications(project):
    """Activities without classifications are ignored instead of raising."""

    bd.Database("test_technosphere").write(
        {
            ("test_technosphere", "bare"): {
                "name": "Bare activity",
                "unit": "kilogram",
                "exchanges": [],
            }
        }
    )

    assert get_nitrogenous_fertilizers("test_technosphere") == []


def test_update_nitrogen_fertilizer_exchanges(technosphere, capsys):
    """An exchange to the nitrogen flow is added once per activity."""
    fertiliser = technosphere.get("fertiliser")

    update_nitrogen_fertilizer_exchanges([fertiliser], show_updated=False)

    exchanges = list(fertiliser.biosphere())
    assert len(exchanges) == 1
    assert exchanges[0]["name"] == "nitrogen fertilizer"
    assert exchanges[0]["amount"] == 1
    assert "1 new exchange has been added" not in capsys.readouterr().out


def test_update_nitrogen_fertilizer_exchanges_is_idempotent(technosphere):
    """Updating an activity twice does not duplicate the exchange."""
    fertiliser = technosphere.get("fertiliser")

    update_nitrogen_fertilizer_exchanges([fertiliser], show_updated=False)
    update_nitrogen_fertilizer_exchanges([fertiliser], show_updated=False)

    assert len(list(fertiliser.biosphere())) == 1


def test_update_nitrogen_fertilizer_exchanges_reports(technosphere, capsys):
    """Updated activities are reported when show_updated is True."""
    fertiliser = technosphere.get("fertiliser")

    update_nitrogen_fertilizer_exchanges([fertiliser], show_updated=True)

    printed = capsys.readouterr().out
    assert "1 new exchange has been added" in printed
    assert "Updated 1 out of 1" in printed


def test_remove_nitrogen_fertilizer_exchanges(technosphere, capsys):
    """The nitrogen exchange is deleted from the activity."""
    fertiliser = technosphere.get("fertiliser")
    update_nitrogen_fertilizer_exchanges([fertiliser], show_updated=False)

    remove_nitrogen_fertilizer_exchanges([fertiliser], show_cleaned=True)

    assert list(fertiliser.biosphere()) == []
    assert "1 activities have been cleaned" in capsys.readouterr().out


def test_remove_nitrogen_fertilizer_exchanges_quiet(technosphere, capsys):
    """The quiet variant reports the count only."""
    fertiliser = technosphere.get("fertiliser")
    update_nitrogen_fertilizer_exchanges([fertiliser], show_updated=False)

    remove_nitrogen_fertilizer_exchanges([fertiliser], show_cleaned=False)

    assert list(fertiliser.biosphere()) == []
    assert "1 activities have been cleaned." in capsys.readouterr().out


def test_update_nitrogen_fertilizer_exchanges_reports_existing(technosphere, capsys):
    """Activities that already have the exchange are reported as untouched."""
    fertiliser = technosphere.get("fertiliser")
    update_nitrogen_fertilizer_exchanges([fertiliser], show_updated=True)
    capsys.readouterr()

    update_nitrogen_fertilizer_exchanges([fertiliser], show_updated=True)

    printed = capsys.readouterr().out
    assert "already contains the necessary exchanges" in printed
    assert "Updated 0 out of 1" in printed
