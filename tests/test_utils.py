import pytest

import bw2data as bd
from aesa_pbs import __version__
from aesa_pbs.utils.utils import progressbar, solve_lca

CLIMATE_CHANGE = (
    "AESA (PBs-LCIA)",
    __version__,
    "climate change",
    "atmospheric CO2 concentration",
)
ENERGY_IMBALANCE = (
    "AESA (PBs-LCIA)",
    __version__,
    "climate change",
    "energy imbalance at top-of-atmosphere",
)


def test_progressbar_yields_all_items(capsys):
    """The wrapper yields every item and reports progress."""
    assert list(progressbar([1, 2, 3], prefix="Progress: ", size=5)) == [1, 2, 3]

    printed = capsys.readouterr().out
    assert "Progress: " in printed
    assert "3/3" in printed
    assert "Duration" in printed


def test_progressbar_without_length(capsys):
    """Iterables without a length still run with a placeholder total."""
    values = (value for value in range(3))

    assert list(progressbar(values)) == [0, 1, 2]
    assert "3/5" in capsys.readouterr().out


def test_progressbar_rejects_non_iterable():
    """Non-iterables raise a TypeError."""
    with pytest.raises(TypeError):
        list(progressbar(5))


def test_solve_lca(aesa_methods, biosphere):
    """LCA scores an activity against an installed AESA method."""
    method = CLIMATE_CHANGE
    flow, cf_amount = _first_characterised_flow(method, biosphere)
    activity = _write_activity(flow)

    scores = solve_lca([activity], [method])

    assert scores.shape == (1, 1)
    assert scores.index.tolist() == [("Test activity", "CH")]
    assert scores.iloc[0, 0] == pytest.approx(2.0 * cf_amount)


def test_solve_lca_multiple_methods(aesa_methods, biosphere):
    """Several methods are reported as separate columns."""
    methods = [CLIMATE_CHANGE, ENERGY_IMBALANCE]
    flow, _ = _first_characterised_flow(CLIMATE_CHANGE, biosphere)
    activity = _write_activity(flow)

    scores = solve_lca([activity], methods)

    assert scores.shape == (1, 2)
    assert scores.notna().all().all()


def test_solve_lca_without_methods(aesa_methods, biosphere):
    """An empty method list returns an empty result."""
    import pandas as pd

    flow, _ = _first_characterised_flow(CLIMATE_CHANGE, biosphere)
    activity = _write_activity(flow)

    scores = solve_lca([activity], [])

    assert isinstance(scores, pd.DataFrame)
    assert scores.empty


def _first_characterised_flow(method, biosphere):
    """Return the biosphere flow characterised by the method's first CF."""
    import brightway2 as bw

    for key, amount in bw.Method(method).load():
        if key[0] != "biosphere3":
            continue
        activity = bd.Database("biosphere3").get(key[1])
        if activity is not None:
            return activity, amount
    raise LookupError(f"No characterised flow found for {method}")


def _write_activity(flow):
    bd.Database("test_activities").write(
        {
            ("test_activities", "activity-1"): {
                "name": "Test activity",
                "location": "CH",
                "unit": "kilogram",
                "exchanges": [
                    {
                        "input": flow.key,
                        "amount": 2.0,
                        "type": "biosphere",
                        "unit": flow["unit"],
                    }
                ],
            }
        }
    )
    return bd.Database("test_activities").get("activity-1")
