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
    "manage_xticks": True,
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
    "medianprops": None,
    "meanprops": None
}


@gen_action(["y"],
            {**box_option, "presenter": None})
def box(df: DataSource, ys: Union[str, List[str]], *arg, presenter=None, **kwargs)->PlotAction:
    """
    Generate box plots for indicated columns.
    """
    _ys = ys if type(ys) is list else [ys]

    @gen_plotter
    def plot(ax):
        artist = ax.boxplot(
            [df[y].dropna() for y in _ys],
            labels=_ys,
            positions=range(0, len(_ys)),
            **kwargs
        )
        if callable(presenter):
            presenter(res)
        return artist
    return plot


@gen_action(["data", "x", "y"],
            {**box_option, "xfactor": None, "presenter": None})
def factor_box(data: DataSource, x, y, xfactor=None, presenter=None, **kwargs)->PlotAction:
    """
    Generate box plots grouped by a factor column in DataFrame.

    """
    _factor_series, _factor, position = Iget_factor(data, x, xfactor)
    _factor_detector = pd.Categorical(
        _factor_series, ordered=True, categories=_factor)

    _group = data.groupby(_factor_detector)
    _data_without_nan = [data.loc[_group.groups[fname]][y].dropna()
                         for fname in _factor]

    @gen_plotter
    def plot(ax):
        if len(_data_without_nan) is 0:
            print("No data for box plot")
            return None
        artist = ax.boxplot(
            _data_without_nan,
            labels=_factor,
            positions=position,
            **kwargs
        )

        if callable(presenter):
            presenter(res)

        if kwargs.get("vert", True):
            ax.set_xticks(position)
            ax.set_xticklabels(_factor)
            #ax.set_xlim([-1, len(_factor)])
        else:
            ax.set_yticks(position)
            ax.set_yticklabels(_factor)
            #ax.set_ylim([-1, len(_factor)])
        return artist
    return plot
