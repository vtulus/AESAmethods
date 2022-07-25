import sys
from datetime import datetime

import brightway2 as bw
import pandas as pd


def solve_lca(activities: list, methods: list) -> pd.DataFrame:
    """Perform LCA calculation given a list of activities and LCIA methods.

    Parameters
    ----------
    activities : list
        List of Brightway activities
    methods : list
        List of Brightway LCIA methods

    Returns
    -------
    pd.DataFrame
        LCA results for all activities with all methods
    """

    results = []
    for act in activities:
        lca = bw.LCA({act: 1})
        lca.lci()
        for method in methods:
            lca.switch_method(method)
            lca.lcia()
            results.append(
                (
                    act["name"],
                    act["location"],
                    " - ".join(
                        [method[2], method[3]]
                    ),  # method[0] - method name, method[1] - method version
                    lca.score,
                    bw.methods.get(method).get("unit"),
                )
            )
    to_return = pd.DataFrame(
        results, columns=["Name", "Location", "Method", "Score", "Unit"]
    )
    to_return = pd.pivot_table(
        to_return,
        index=["Name", "Location"],
        columns=["Method", "Unit"],
        values="Score",
    )
    return to_return


def progressbar(itobj: list, **kwargs):
    """Generate a progress bar.
    Progress bar adapted from https://stackoverflow.com/a/34482761/14485040

    Parameters
    ----------
    itobj : list-like
        Iterable object
        
    **kwargs
    --------
    total : int, default len(itobj)
        Size of the iterable object
    prefix : str, default ""
        String preceding the progress bar
    size : int, default 30
        Number of icons conforming the progress bar
    unit : str, default ""
        String following the progress bar, intended to be used for units
    icon_done : str, default "🟩"
        str-like symbol to be used as "done"-icon
    icon_todo : str, default "🔳"
        str-like symbol to be used as "to do"-icon
        
    Example
    -------
    lst = [5, 3, 4]
    for i in progressbar(itobj=lst, total=len(lst), prefix="Progress: ", size=5, unit="datapoint"):
        # do_something
    """
    start_time = datetime.now()
    file = sys.stdout

    try:
        iter(itobj)  # check if provided `itobj` is iterable
    except TypeError as err:
        raise TypeError from err

    # if "total" in kwargs:
    #     total = kwargs["total"]
    # else:
    #     total = len(itobj)
    # refactor the above to:
    try:
        len_itobj = len(itobj)
    except TypeError:
        len_itobj = int(5)  # placeholder
    total = kwargs.get("total", len_itobj)
    # similarly for the rest
    prefix = kwargs.get("prefix", "")
    size = kwargs.get("size", 30)
    unit = kwargs.get("unit", "")
    icon_done = kwargs.get("icon_done", "🟩")
    icon_todo = kwargs.get("icon_todo", "🔳")

    def show(j):
        icons_to_show = int(size * j / total)
        # some ASCII symbol or emoji alternatives

        # |, *, #, %, ▒. ▓, █, ■, ♢, ⚃ ⚄ ⚅
        # 🦾, 👍, 🔴, 🟡 🟢 🔵 🟣 ⚫️ ⚪️, 🔸 🔹 🔶 🔷 🔳 🔲 ▪️ ▫️ ◾️ ◽️ ◼️ ◻️ 🟥 🟧 🟨 🟩 🟦 🟪 ⬛️ ⬜️, ▶️

        file.write(
            "%s[%s%s] %i/%i %s\r"
            % (
                prefix,
                icon_done * icons_to_show,
                icon_todo * (size - icons_to_show),
                j,
                total,
                unit,
            )
        )
        file.flush()

    show(0)
    for i, item in enumerate(itobj):
        yield item
        show(i + 1)
    file.write("\n")
    file.flush()

    end_time = datetime.now()
    print("Duration: {}".format(end_time - start_time))
