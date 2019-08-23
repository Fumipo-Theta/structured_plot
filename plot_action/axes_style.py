from .action import default_kwargs, plot_action, generate_arg_and_kwags, get_value, get_subset
from .action import DataSource, AxPlot
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


def _get_lim(df: DataSource, lim_list: Optional[list]):
    try:
        if lim_list is not None and len(lim_list) >= 2:
            lim = [*lim_list]
            if lim[0] is None:
                lim[0] = np.min(df.min())
            if lim[1] is None:
                lim[1] = np.max(df.max())
            return lim
        else:
            return [
                np.min(df.min()),
                np.max(df.max())
            ]
    except:
        print(f"Failed: Set limit {lim_list}.")
        return None


def _get_lim_parameter(df: DataSource, lim_list: Optional[list]):
    if lim_list is None:
        return None
    elif len(lim_list) >= 2:
        return lim_list
    elif len(lim_list) is 1:
        return [lim_list[0], None]
    else:
        return None


_invalid_range = [None, pd.NaT, np.nan]


@plot_action(["x"],
             {"xlim": None})
def set_xlim(df: DataSource, x, *arg, xlim=None, **kwargs)->AxPlot:
    """
    Parameters
    ----------
    x
    """
    lim = _get_lim_parameter(get_subset()(df, x), xlim)

    def plot(ax):
        if lim is not None:
            now_lim = ax.get_xlim()
            next_lim = [None, None]
            next_lim[0] = lim[0] if lim[0] not in _invalid_range else now_lim[0]
            next_lim[1] = lim[1] if lim[1] not in _invalid_range else now_lim[1]
            ax.set_xlim(next_lim)
        return ax
    return plot


@plot_action(["y"],
             {"ylim": None})
def set_ylim(df: DataSource, y, *arg, ylim=None, **kwargs)->AxPlot:
    """
    Parameters
    ----------
    y
    """
    lim = _get_lim_parameter(get_subset()(df, y), ylim)

    def plot(ax):
        if lim is not None:
            now_lim = ax.get_ylim()
            next_lim = [None, None]
            next_lim[0] = lim[0] if lim[0] not in _invalid_range else now_lim[0]
            next_lim[1] = lim[1] if lim[1] not in _invalid_range else now_lim[1]
            ax.set_ylim(next_lim)
        return ax
    return plot


@plot_action(["z"],
             {"zlim": None})
def set_zlim(df: DataSource, z, *arg, zlim=None, **kwargs)->AxPlot:
    """
    Parameters
    ----------
    z
    """
    lim = _get_lim_parameter(get_subset()(df, z), zlim)

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


@plot_action([],
             default_kwargs.get("grid"))
def set_grid(*arg, axis=None, **kwargs)->AxPlot:
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


@plot_action(["axis"], {
    **tick_option,
    "locations": None,
    "labels": None
})
def set_tick_parameters(df, axis, *arg, locations=None, labels=None, **kwargs)->AxPlot:
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
                axis=axis, **dict(filter(lambda kv: kv[0] in default_kwargs.get("tick_params_each"), kwargs.items())))

        return ax
    return plot


@plot_action([],
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


@plot_action(["xlabel", "ylabel", "zlabel"],
             {
                 **label_option,
})
def set_label(
    df: DataSource,
    xlabel: str,
    ylabel: str,
    zlabel: str,
    *arg,
    xlabelposition=None,
    ylabelposition=None,
    zlabelposition=None,
    **kwargs
)->AxPlot:

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


@plot_action(["xlabel"], {**label_option, "xlabelposition": None, })
def set_xlabel(df, xlabel: str, *arg, xlabelposition=None, **kwargs)->AxPlot:
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


@plot_action(["ylabel"], {**label_option, "ylabelposition": None, })
def set_ylabel(df, ylabel: str, *arg, ylabelposition=None, **kwargs)->AxPlot:
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


@plot_action(["zlabel"], {**label_option, "zlabelposition": None, })
def set_zlabel(df, zlabel: str, *arg, zlabelposition=None, **kwargs)->AxPlot:
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
