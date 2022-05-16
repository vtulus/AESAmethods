import brightway2 as bw


def get_nitrogenous_fertilizers(db_name: str) -> list:
    """Get list of nitrogenous fertilizers

    Get all activities classified according to CPC as
    "Class 3461: Mineral of chemical fertilizers, nitrogenous", 
    except "market"-type activities

    Parameters
    ----------
    db_name : str
        Name of the database to search for the activities

    Returns
    -------
    list
        List of activities producing nitrogenous fertilizers
    """
    list_to_return = []
    for act in bw.Database(db_name):
        for classification in act["classifications"]:
            if "cpc" in classification[0].lower() and classification[1].startswith(
                "3461"
            ):
                if "market" not in act["name"]:
                    list_to_return.append(act)
    return list_to_return


def update_nitrogen_fertilizer_exchanges(activities: list, show_updated=True) -> None:
    """Create exchanges for 'nitrogen fertilizer' in `activities` if they don't exist already.

    Does not return anything, but modified `activities` inplace.

    Parameters
    ----------
    activities : list
        List of activities producing nitrogenous fertilizers.
        May be retrieved automatically with `get_nitrogenous_fertilizers()`
    show_updated : bool, optional
        Whether to show the set of updated activities, by default True
    """
    flow = [flow for flow in bw.Database("A_technosphere_flows")][
        0
    ]  # select the only flow in the `A_technosphere_flows` db

    def is_exchange(exc):
        return bw.get_activity(exc["input"])[
            "name"
        ] == "nitrogen fertilizer" and bw.get_activity(exc["input"])["categories"] == (
            "inventory",
        )

    print("Updating activities that produce nitrogen fertilizer...")
    updated_act = set()
    for act in activities:
        if not list(filter(is_exchange, [exc for exc in act.biosphere()])):
            act.new_exchange(
                **{
                    "name": bw.get_activity(flow)["name"],
                    "input": (
                        bw.get_activity(flow)["database"],
                        bw.get_activity(flow)["code"],
                    ),
                    "type": "biosphere",
                    "amount": 1,
                    "unit": bw.get_activity(flow)["unit"],
                }
            ).save()
            updated_act.add(act)
            if show_updated:
                print(f"__ 1 new exchange has been added to {act}.")
        else:
            if show_updated:
                print(f"xx {act} already contains the necessary exchanges.")
    print(f"Updated {len(updated_act)} out of {len(activities)}.")


def remove_nitrogen_fertilizer_exchanges(activities: list, show_cleaned=True) -> None:
    """Delete exchanges for 'nitrogen fertilizer' from `activities`.

    Does not return anything, but modified `activities` inplace.

    Parameters
    ----------
    activities : list
        List of activities producing nitrogenous fertilizers (to be cleaned).
        May be retrieved automatically with `get_nitrogenous_fertilizers()`
    show_cleaned : bool, optional
        Whether to show the set of cleaned activities, by default True
    """

    def is_exchange(exc):
        return bw.get_activity(exc["input"])[
            "name"
        ] == "nitrogen fertilizer" and bw.get_activity(exc["input"])["categories"] == (
            "inventory",
        )

    print(
        "Cleaning 'nitrogen fertilizer' exchanges from the activities that produce nitrogen fertilizer..."
    )
    cleaned_act = set()
    for act in activities:
        for exc in act.biosphere():
            if is_exchange(exc):
                exc.delete()
                cleaned_act.add(act)
    if show_cleaned:
        print(
            f"These {len(cleaned_act)} activities have been cleaned: \n{list(cleaned_act)}."
        )
    else:
        print(f"{len(cleaned_act)} activities have been cleaned.")
