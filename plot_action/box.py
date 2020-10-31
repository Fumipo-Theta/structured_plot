from ..kit import gen_action, gen_plotter, get_subset, Iget_factor
from ..type_set import DataSource, PlotAction
from typing import Union, List
import pandas as pd

box_option = {
    "vert": True,
    "notch": False,
    "sym": None,  # Symbol setting for out lier
    "whis": 1.5,
    "bootstrap": None,
    "usermedians": None,
    "conf_intervals": None,
    "widths": 0.5,
    "patch_artist": False,
    "manage_ticks": True,
    "autorange": False,
    "meanline": False,
    "zorder": None,
    "showcaps": True,
    "showbox": True,
    "showfliers": True,
    "showmeans": False,
    "capprops": None,
    "boxprops": None,
    "whiskerprops": None,
    "flierprops": None,
    "medianprops": {"color": "black"},
    "meanprops": {"marker": "o", "markerfacecolor": "black", "markeredgecolor": "black"}
}


@gen_action(["data", "x"],
            {**box_option, "labels": None, "presenter": None, "summarizer": None})
def box(data: DataSource, x: Union[str, List[str]], *arg, labels=None, presenter=None, summarizer=None, **kwargs) -> PlotAction:
    """
    Generate box plots for indicated columns.
    """
    _xs = x if type(x) is list else [x]

    _data_without_nan = [data[x].dropna() for x in _xs]

    if summarizer is not None:
        summarizer(zip(_xs, _data_without_nan))

    @gen_plotter
    def plot(ax):
        artist = ax.boxplot(
            _data_without_nan,
            labels=labels if labels else _xs,
            positions=range(0, len(_xs)),
            **kwargs
        )
        return artist
    return plot


@gen_action(["data", "x", "y"],
            {**box_option, "xfactor": None, "presenter": None, "summarizer": None,
             "map_of_xlabel": lambda label: label
             })
def factor_box(data: DataSource, x, y, xfactor=None, presenter=None, summarizer=None, map_of_xlabel=lambda x: x, **kwargs) -> PlotAction:
    """
    Generate box plots grouped by a factor column in DataFrame.

    """
    _factor_series, _factor, position = Iget_factor(data, x, xfactor)
    _factor_detector = pd.Categorical(
        _factor_series, ordered=True, categories=_factor)

    _group = data.groupby(_factor_detector)
    _data_without_nan = [get_subset()(data.loc[_group.groups[fname]], y).dropna()
                         for fname in _factor]

    if summarizer is not None:
        summarizer(zip(_factor, _data_without_nan))

    labels = list(map(map_of_xlabel, _factor))

    @gen_plotter
    def plot(ax):
        if len(_data_without_nan) is 0:
            print("No data for box plot")
            return None
        artist = ax.boxplot(
            _data_without_nan,
            labels=labels,
            positions=position,
            **kwargs
        )

        if kwargs.get("vert", True):
            ax.set_xticks(position)
            ax.set_xticklabels(labels)
        else:
            ax.set_yticks(position)
            ax.set_yticklabels(labels)
        return artist
    return plot
