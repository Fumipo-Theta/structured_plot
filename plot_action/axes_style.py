from ..kit import gen_action, get_subset
from ..type_set import DataSource, PlotAction
from typing import Optional
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def set_cycler(cycler=None):
    def setter(ax):
        if cycler is 'default':
            return ax
        elif cycler is None:
            return ax
        else:
            ax.set_prop_cycle(cycler)
        return ax
    return setter


def _get_lim(data: DataSource, lim_list: Optional[list]):
    try:
        if lim_list is not None and len(lim_list) >= 2:
            lim = [*lim_list]
            if lim[0] is None:
                lim[0] = np.min(data.min())
            if lim[1] is None:
                lim[1] = np.max(data.max())
            return lim
        else:
            return [
                np.min(data.min()),
                np.max(data.max())
            ]
    except:
        print(f"Failed: Set limit {lim_list}.")
        return None


def _get_lim_parameter(data: DataSource, lim_list: Optional[list]):
    if lim_list is None:
        return None
    elif len(lim_list) >= 2:
        return lim_list
    elif len(lim_list) is 1:
        return [lim_list[0], None]
    else:
        return None


_invalid_range = [None, pd.NaT, np.nan]


@gen_action(["data", "x"],
            {"xlim": None})
def set_xlim(data: DataSource, x, *arg, xlim=None, **kwargs)->PlotAction:
    """
    Parameters
    ----------
    x
    """
    lim = _get_lim_parameter(get_subset()(data, x), xlim)

    def plot(ax):
        if lim is not None:
            now_lim = ax.get_xlim()
            next_lim = [None, None]
            next_lim[0] = lim[0] if lim[0] not in _invalid_range else now_lim[0]
            next_lim[1] = lim[1] if lim[1] not in _invalid_range else now_lim[1]
            ax.set_xlim(next_lim)
        return ax
    return plot


@gen_action(["data", "y"],
            {"ylim": None})
def set_ylim(data: DataSource, y, *arg, ylim=None, **kwargs)->PlotAction:
    """
    Parameters
    ----------
    y
    """
    lim = _get_lim_parameter(get_subset()(data, y), ylim)

    def plot(ax):
        if lim is not None:
            now_lim = ax.get_ylim()
            next_lim = [None, None]
            next_lim[0] = lim[0] if lim[0] not in _invalid_range else now_lim[0]
            next_lim[1] = lim[1] if lim[1] not in _invalid_range else now_lim[1]
            ax.set_ylim(next_lim)
        return ax
    return plot


@gen_action(["data", "z"],
            {"zlim": None})
def set_zlim(data: DataSource, z, *arg, zlim=None, **kwargs)->PlotAction:
    """
    Parameters
    ----------
    z
    """
    lim = _get_lim_parameter(get_subset()(data, z), zlim)

    def plot(ax):
        if not hasattr(ax, "get_zlim"):
            return ax

        if lim is not None:
            now_lim = ax.get_zlim()
            next_lim = [None, None]
            next_lim[0] = lim[0] if lim[0] not in _invalid_range else now_lim[0]
            next_lim[1] = lim[1] if lim[1] not in _invalid_range else now_lim[1]
            ax.set_zlim(next_lim)
        return ax
    return plot


from .artist_options import line2d_option

grid_option = {
    **line2d_option,
    "axis": None,
    "color": 'gray',
    "linestyle": ':',
    "linewidth": 1,
}


@gen_action([],
            grid_option)
def set_grid(*arg, axis=None, **kwargs)->PlotAction:
    """
    Show grid line.

    axis: "x" | "y" | "z" | "both"
    """
    def plot(ax):
        if axis is None:
            return ax
        ax.grid(axis=axis, **kwargs)
        return ax
    return plot


tick_option = {
    "labelsize": 12,
    "rotation": 0,
    "which": "both",
    "direction": "in",
    "color": "black",
    "labelcolor": "black",
    "labelbottom": None,
    "labelleft": None,
    "labeltop": None,
    "labelright": None,
    "bottom": None,
    "left": None,
    "top": None,
    "right": None
}

tick_params_each = {
    "labelsize": 12,
    "rotation": 0,
    "which": "both",
    "direction": "in",
    "color": "black",
    "labelcolor": "black"
}


@gen_action(["axis"], {
    **tick_option,
    "locations": None,
    "labels": None
})
def set_tick_parameters(axis, *arg, locations=None, labels=None, **kwargs)->PlotAction:
    """
    Show/hide ticks and tick labels.
    Set tick locations and labels.
    """
    def plot(ax):
        if axis is "x":
            if type(locations) in [list, np.ndarray]:
                ax.set_xticks(locations)
                #plt.setp(ax.get_xticklabels(), visible=True)
            if type(labels) in [list, np.ndarray]:
                ax.set_xticklabels(labels)
                plt.setp(ax.get_xticklabels(), visible=True)
        if axis is "y":
            if type(locations) in [list, np.ndarray]:
                ax.set_yticks(locations)
                #plt.setp(ax.get_yticklabels(), visible=True)
            if type(labels) in [list, np.ndarray]:
                ax.set_yticklabels(labels)
                plt.setp(ax.get_yticklabels(), visible=True)

        if axis is "z":
            if type(locations) in [list, np.ndarray]:
                ax.set_zticks(locations)
                #plt.setp(ax.get_yticklabels(), visible=True)
            if type(labels) in [list, np.ndarray]:
                ax.set_zticklabels(labels)
                plt.setp(ax.get_zticklabels(), visible=True)

        if axis is "both":
            ax.tick_params(axis=axis, **kwargs)
        else:
            ax.tick_params(
                axis=axis, **dict(filter(lambda kv: kv[0] in tick_params_each, kwargs.items())))

        return ax
    return plot


@gen_action([],
            {"xscale": None, "yscale": None, "zscale": None})
def axis_scale(*arg, xscale=None, yscale=None, zscale=None):
    """
    Set axis scale types.

    xscale: None | "log"
    yscale: None | "log"
    """
    def plot(ax):
        if xscale is not None:
            ax.set_xscale(xscale)
        if yscale is not None:
            ax.set_yscale(yscale)
        if zscale is not None:
            ax.set_zscale(zscale)
        return ax
    return plot


label_option = {
    "alpha": 1,
    "color": "black",
    "family": ["Noto Sans CJK JP", "sans-serif"],
    # "fontname" : "sans-serif",
    "fontsize": 16,
    "fontstyle": "normal",
    "fontweight": "normal",
    "rotation": None,
}


@gen_action(["xlabel", "ylabel", "zlabel"],
            {
    **label_option,
})
def set_label(
    xlabel: str,
    ylabel: str,
    zlabel: str,
    *arg,
    xlabelposition=None,
    ylabelposition=None,
    zlabelposition=None,
    **kwargs
)->PlotAction:

    def plot(ax):
        if xlabel is not None:
            ax.set_xlabel(
                xlabel,
                **kwargs
            )

        if xlabelposition is not None:
            ax.xaxis.set_label_position(xlabelposition)
            plt.setp(ax.get_xticklabels(), visible=True)

        if ylabel is not None:
            ax.set_ylabel(
                ylabel,
                **kwargs
            )
        if ylabelposition is not None:
            ax.yaxis.set_label_position(ylabelposition)
            plt.setp(ax.get_yticklabels(), visible=True)

        if zlabel is not None:
            ax.set_zlabel(
                zlabel,
                **kwargs
            )

        if zlabelposition is not None:
            ax.zaxis.set_label_position(zlabelposition)
            plt.setp(ax.get_zticklabels(), visible=True)
        return ax
    return plot


@gen_action(["xlabel"], {**label_option, "xlabelposition": None, })
def set_xlabel(xlabel: str, *arg, xlabelposition=None, **kwargs)->PlotAction:
    def plot(ax):
        if xlabel is not None:
            ax.set_xlabel(
                xlabel,
                **kwargs
            )

        if xlabelposition is not None:
            ax.xaxis.set_label_position(xlabelposition)
            #plt.setp(ax.get_xticklabels(), visible=True)
        return ax
    return plot


@gen_action(["ylabel"], {**label_option, "ylabelposition": None, })
def set_ylabel(ylabel: str, *arg, ylabelposition=None, **kwargs)->PlotAction:
    def plot(ax):
        if ylabel is not None:
            ax.set_ylabel(
                ylabel,
                **kwargs
            )
        if ylabelposition is not None:
            ax.yaxis.set_label_position(ylabelposition)
            #plt.setp(ax.get_yticklabels(), visible=True)
        return ax
    return plot


@gen_action(["zlabel"], {**label_option, "zlabelposition": None, })
def set_zlabel(zlabel: str, *arg, zlabelposition=None, **kwargs)->PlotAction:
    def plot(ax):
        if zlabel is not None:
            ax.set_zlabel(
                zlabel,
                **kwargs
            )
        if zlabelposition is not None:
            ax.zaxis.set_label_position(zlabelposition)
            #plt.setp(ax.get_yticklabels(), visible=True)
        return ax
    return plot


def twinx():
    def set_data(*arg):
        def plot(ax):
            return ax.twinx()
        return plot
    return set_data
