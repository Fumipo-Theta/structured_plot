from __future__ import annotations
from ..kit import gen_action, gen_plotter, get_subset, Iget_factor
from ..type_set import DataSource, PlotAction
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
            box_option | {
                "labels": None, "presenter": None, "summarizer": None,
                "map_of_position": lambda p: p, "map_of_xlabel": lambda label: label,
                "positions": None
})
def box(
        data: DataSource,
        x: str | list[str],
        *arg,
        labels=None,
        presenter=None,
        summarizer=None,
        positions=None,
        map_of_position=lambda x: x,
        map_of_xlabel=lambda x: x,
        **kwargs) -> PlotAction:
    """
    Generate box plots for indicated columns.
    """
    _xs = x if type(x) is list else [x]

    _data_without_nan = [data[x].dropna() for x in _xs]

    if summarizer is not None:
        summarizer(zip(_xs, _data_without_nan))

    _labels = labels or _xs

    if callable(map_of_xlabel):
        _labels = list(map(map_of_xlabel, _labels))
    elif isinstance(map_of_xlabel, dict):
        _labels = [map_of_xlabel.get(k, k) for k in _labels]
    else:
        _labels = _labels

    _positions = positions or range(0, len(_xs))
    if callable(map_of_position):
        _positions = list(map(map_of_position, _positions))
    elif isinstance(map_of_position, dict):
        _positions = [map_of_position.get(k, k) for k in _positions]
    else:
        _positions = _positions

    @gen_plotter
    def plot(ax):
        artist = ax.boxplot(
            _data_without_nan,
            labels=_labels,
            positions=_positions,
            **kwargs
        )
        return artist
    return plot


@gen_action(["data", "x", "y"],
            {**box_option, "xfactor": None, "presenter": None, "summarizer": None,
             "map_of_position": lambda p: p,
             "map_of_xlabel": lambda label: label
             })
def factor_box(data: DataSource, x, y, xfactor=None, presenter=None, summarizer=None, map_of_position=lambda x: x, map_of_xlabel=lambda x: x, **kwargs) -> PlotAction:
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

    _labels = _factor
    if callable(map_of_xlabel):
        _labels = list(map(map_of_xlabel, _labels))
    elif isinstance(map_of_xlabel, dict):
        _labels = [map_of_xlabel.get(k, k) for k in _labels]
    else:
        _labels = _labels

    @gen_plotter
    def plot(ax):
        if len(_data_without_nan) == 0:
            print("No data for box plot")
            return None
        artist = ax.boxplot(
            _data_without_nan,
            labels=_labels,
            positions=list(map(map_of_position, position)),
            **kwargs
        )

        if kwargs.get("vert", True):
            ax.set_xticks(position)
            ax.set_xticklabels(_labels)
        else:
            ax.set_yticks(position)
            ax.set_yticklabels(_labels)
        return artist
    return plot
