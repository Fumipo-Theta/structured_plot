from ..kit import gen_action, get_subset, Iget_factor
from ..type_set import DataSource, PlotAction
import pandas as pd
import numpy as np
from func_helper import pip
import iter_helper as it

violin_option = {
    "vert": True,
    "widths": 0.5,
    "showmeans": False,
    "showextrema": True,
    "showmedians": False,
    "points": 100,
    "bw_method": None,
    "positions": None,
    "scale": "width",  # "width" | "count"

    "bodies": None,
    "cmeans": None
}

"""
https: // matplotlib.org/api/_as_gen/matplotlib.axes.Axes.violin.html

bodies: {
    "facecolor": "#2196f3",
    "edgecolor": "#005588",
    "alpha": 0.5
}
# matplotlib.collections.PolyCollection
https: // matplotlib.org/api/collections_api.html

cmeans: {
    "edgecolor",
    "linestyle",
    "linewidth",
    "alpha"
}
# matplotlib.collections.LineCollection
https: // matplotlib.org/api/collections_api.html
"""


@gen_action(["data", "y"], violin_option)
def violin(
    data: DataSource, y, *arg,
    bodies=None,
    cmeans=None,
    widths=0.5,
    scale="width",
    **kwargs
)->PlotAction:

    _factor = y if type(y) in [list, tuple] else [y]

    _data_without_nan = [data[fname].dropna() for fname in _factor]
    _subset_hasLegalLength = pip(
        it.filtering(lambda iv: len(iv[1]) > 0),
        list
    )(enumerate(_data_without_nan))

    dataset = [iv[1].values for iv in _subset_hasLegalLength]
    positions = [iv[0] for iv in _subset_hasLegalLength]

    if scale is "count":
        count = [len(d) for d in dataset]
        variance = [np.var(d) for d in dataset]
        max_count = np.max(count)
        _widths = [c/(max_count) for c, v in zip(count, variance)]
    else:
        _widths = widths

    def plot(ax):

        if len(dataset) is 0:
            print("No data for violin plot")
            return ax

        parts = ax.violinplot(
            dataset=dataset,
            positions=positions,
            widths=_widths,
            **kwargs
        )

        # Customize style for each part of violine
        if bodies is not None:
            for p in parts["bodies"]:
                p.set_facecolor(bodies.get("facecolor", "#2196f3"))
                p.set_edgecolor(bodies.get("edgecolor", "#005588"))
                p.set_alpha(bodies.get("alpha", 0.5))

        if cmeans is not None:
            p = parts["cmeans"]
            p.set_edgecolor(cmeans.get("edgecolor", "#005588"))
            p.set_linestyle(cmeans.get("linestyle", "-"))
            p.set_linewidth(cmeans.get("linewidth", 1))
            p.set_alpha(cmeans.get("alpha", 0.5))

        if kwargs.get("vert", True):
            ax.set_xticks(list(range(0, len(_factor))))
            ax.set_xticklabels(_factor)
            ax.set_xlim([-1, len(_factor)])
        else:
            ax.set_yticks(list(range(0, len(_factor))))
            ax.set_yticklabels(_factor)
            ax.set_ylim([-1, len(_factor)])

        return ax

    return plot


@gen_action(["data", "x", "y"],
            {**violin_option, "xfactor": None})
def factor_violin(
        data: DataSource, x, y, *arg,
        bodies=None,
        cmeans=None,
        widths=0.5,
        scale="width",
        xfactor=None,
        positions=None,
        **kwargs)->PlotAction:
    """
    factor_violine
    --------------
    Plot violin plots for pandas.Series.
    The serieses are subset filtered by a factor.

    Usage
    -----
    plot.factor_violin(**preset_kwargs)(
        df,{
            "y":"column name for violin plot",
            "x":"column name for factor"
        }
    )(matplotlib.pyplot.subplot())

    Default preset_kwargs are:
        {
            "vert": True,
            "widths" :0.5,
            "showmeans":False,
            "showextrema":True,
            "showmedians":False,
            "points":100,
            "bw_method":None,
            "scale" : "width",
            "bodies": None,
            "cmeans": None
        }

    If scale is "width", each violin has the same width.
    Else of scale is "count", each violin has the width proportional
        to its data size.

    "bodies" is used for styling parts of violin.
    Default is:
        {
            "facecolor": "#2196f3",
            "edgecolor": "#005588",
            "alpha": 0.5
        }

    factorが与えられたときはfactorでgroupbyする.
    与えられなかったときはdf[f]でgroupbyする.
    """

    _factor_series, _factor, position = Iget_factor(data, x, xfactor)
    _factor_detector = pd.Categorical(
        _factor_series, ordered=True, categories=_factor)

    _group = data.groupby(_factor_detector)
    _data_without_nan = [data.loc[_group.groups[fname]][y].dropna()
                         for fname in _factor]

    loc_and_violin = enumerate(_data_without_nan) if positions is None \
        else zip(positions, _data_without_nan)

    _subset_hasLegalLength = pip(
        it.filtering(lambda iv: len(iv[1]) > 0),
        list
    )(enumerate(_data_without_nan))

    dataset = [iv[1].values for iv in _subset_hasLegalLength]
    _positions = [position[iv[0]] for iv in _subset_hasLegalLength]

    if scale is "count":
        count = [len(d) for d in dataset]
        variance = [np.var(d) for d in dataset]
        max_count = np.max(count)
        _widths = [c/(max_count) for c, v in zip(count, variance)]
    else:
        _widths = widths

    def plot(ax):
        if len(dataset) is 0:
            print("No data for violin plot")
            return ax

        parts = ax.violinplot(
            dataset=dataset,
            positions=_positions,
            widths=_widths,
            **kwargs
        )

        # Customize style for each part of violine
        if bodies is not None:
            for p in parts["bodies"]:
                p.set_facecolor(bodies.get("facecolor", "#2196f3"))
                p.set_edgecolor(bodies.get("edgecolor", "#005588"))
                p.set_alpha(bodies.get("alpha", 0.5))

        if cmeans is not None:
            p = parts["cmeans"]
            p.set_edgecolor(cmeans.get("edgecolor", "#005588"))
            p.set_linestyle(cmeans.get("linestyle", "-"))
            p.set_linewidth(cmeans.get("linewidth", 1))
            p.set_alpha(cmeans.get("alpha", 0.5))

        if kwargs.get("vert", True):
            ax.set_xticks(list(range(0, len(_factor))))
            ax.set_xticklabels(_factor)
            #ax.set_xlim([-1, len(_factor)])
        else:
            ax.set_yticks(list(range(0, len(_factor))))
            ax.set_yticklabels(_factor)
            #ax.set_ylim([-1, len(_factor)])

        return ax
    return plot
