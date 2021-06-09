from __future__ import annotations
import re
from .artist_options import line2d_option
from ..kit import gen_action, gen_plotter, get_subset
from ..type_set import DataSource, PlotAction
from typing import Callable, Optional
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def set_cycler(cycler=None):
    @gen_plotter
    def setter(ax):
        if cycler == 'default':
            return None
        elif cycler is None:
            return None
        else:
            ax.set_prop_cycle(cycler)
        return None
    return setter


def _lim_parser(orig_new: tuple[float, str | float | int | Callable[[float], float] | None]) -> float:
    orig, new = orig_new
    if new is None:
        return orig
    if callable(new):
        return new(orig)
    if isinstance(new, pd.Timestamp):
        return new

    try:
        return float(new)
    except Exception as _e:
        if (match := re.search(r"([-+])([0-9\.]+)%", new)) is not None:
            d_sign = 1 if match[1] == "+" else -1
            d_ratio = float(match[2]) / 100
            d = d_sign * abs(orig) * d_ratio
            return orig + d
        else:
            raise ValueError("Invalid range format.")


def _get_lim_parameter(original_lim, lim_list: list[str | float | int | Callable[[float], float] | None] | None) -> list[float]:
    """
    lim_list
        If autoscaled limit is [-5, 90],
        [0, None] => [0, 90.0]
        [None, 100.0] => [-5, 100.0]
        ["-10%", "+10%"] => [-5.5, 99.0]

    """
    if lim_list is None:
        return original_lim
    elif len(lim_list) >= 2:
        return list(map(_lim_parser, zip(original_lim, lim_list[0:2])))
    else:
        return original_lim


_invalid_range = [None, pd.NaT, np.nan]


@gen_action(["data", "x"],
            {"xlim": None})
def set_xlim(data: DataSource, x, *arg, xlim=None, **kwargs) -> PlotAction:
    """
    Parameters
    ----------
    x
    """

    @gen_plotter
    def plot(ax):
        now_lim = ax.get_xlim()
        next_lim = _get_lim_parameter(now_lim, xlim)
        ax.set_xlim(next_lim)
        return None
    return plot


@gen_action(["data", "y"],
            {"ylim": None})
def set_ylim(data: DataSource, y, *arg, ylim=None, **kwargs) -> PlotAction:
    """
    Parameters
    ----------
    y
    """

    @gen_plotter
    def plot(ax):
        now_lim = ax.get_ylim()
        next_lim = _get_lim_parameter(now_lim, ylim)
        ax.set_ylim(next_lim)
        return None
    return plot


@gen_action(["data", "z"],
            {"zlim": None})
def set_zlim(data: DataSource, z, *arg, zlim=None, **kwargs) -> PlotAction:
    """
    Parameters
    ----------
    z
    """

    @gen_plotter
    def plot(ax):
        if not hasattr(ax, "get_zlim"):
            return None

        now_lim = ax.get_zlim()
        next_lim = _get_lim_parameter(now_lim, zlim)
        ax.set_zlim(next_lim)
        return None
    return plot


grid_option = {
    **line2d_option,
    "axis": None,
    "color": 'gray',
    "linestyle": ':',
    "linewidth": 1,
}


@gen_action([],
            grid_option)
def set_grid(*arg, axis=None, **kwargs) -> PlotAction:
    """
    Show grid line.

    axis: "x" | "y" | "z" | "both"
    """

    @gen_plotter
    def plot(ax):
        if axis is None:
            return None
        ax.grid(axis=axis, **kwargs)
        return None
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
def set_tick_parameters(axis, *arg, locations=None, labels=None, **kwargs) -> PlotAction:
    """
    Show/hide ticks and tick labels.
    Set tick locations and labels.
    """
    @gen_plotter
    def plot(ax):
        if hasattr(ax, f"set_{axis}ticks"):
            if axis == "x":
                if type(locations) in [list, np.ndarray]:
                    ax.set_xticks(locations)

                if type(labels) in [list, np.ndarray]:
                    ax.set_xticklabels(labels)
                    plt.setp(ax.get_xticklabels(), visible=True)
            if axis == "y":
                if type(locations) in [list, np.ndarray]:
                    ax.set_yticks(locations)

                if type(labels) in [list, np.ndarray]:
                    ax.set_yticklabels(labels)
                    plt.setp(ax.get_yticklabels(), visible=True)

            if axis == "z":
                if type(locations) in [list, np.ndarray]:
                    ax.set_zticks(locations)

                if type(labels) in [list, np.ndarray]:
                    ax.set_zticklabels(labels)
                    plt.setp(ax.get_zticklabels(), visible=True)

        if axis == "both":
            ax.tick_params(axis=axis, **kwargs)
        else:
            if hasattr(ax, f"set_{axis}ticklabels"):
                ax.tick_params(
                    axis=axis, **dict(filter(lambda kv: kv[0] in tick_params_each, kwargs.items())))

        return None
    return plot


@gen_action([],
            {"xscale": None, "yscale": None, "zscale": None})
def axis_scale(*arg, xscale=None, yscale=None, zscale=None):
    """
    Set axis scale types.

    xscale: None | "log"
    yscale: None | "log"
    """
    @gen_plotter
    def plot(ax):
        if xscale is not None:
            ax.set_xscale(xscale)
        if yscale is not None:
            ax.set_yscale(yscale)
        if zscale is not None:
            ax.set_zscale(zscale)
        return None
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
) -> PlotAction:

    @gen_plotter
    def plot(ax):
        if xlabel and xlabel != False:
            ax.set_xlabel(
                xlabel,
                **kwargs
            )

        if xlabelposition is not None:
            ax.xaxis.set_label_position(xlabelposition)
            plt.setp(ax.get_xticklabels(), visible=True)

        if ylabel and ylabel != False:
            ax.set_ylabel(
                ylabel,
                **kwargs
            )
        if ylabelposition is not None:
            ax.yaxis.set_label_position(ylabelposition)
            plt.setp(ax.get_yticklabels(), visible=True)

        if zlabel and zlabel != False:
            ax.set_zlabel(
                zlabel,
                **kwargs
            )

        if zlabelposition is not None:
            ax.zaxis.set_label_position(zlabelposition)
            plt.setp(ax.get_zticklabels(), visible=True)
        return None
    return plot


@gen_action(["xlabel"], {**label_option, "xlabelposition": None, })
def set_xlabel(xlabel: str, *arg, xlabelposition=None, **kwargs) -> PlotAction:

    @gen_plotter
    def plot(ax):
        if xlabel and xlabel != False:
            ax.set_xlabel(
                xlabel,
                **kwargs
            )

        if xlabelposition is not None:
            ax.xaxis.set_label_position(xlabelposition)
            #plt.setp(ax.get_xticklabels(), visible=True)
        return None
    return plot


@gen_action(["ylabel"], {**label_option, "ylabelposition": None, })
def set_ylabel(ylabel: str, *arg, ylabelposition=None, **kwargs) -> PlotAction:

    @gen_plotter
    def plot(ax):
        if ylabel and ylabel != False:
            ax.set_ylabel(
                ylabel,
                **kwargs
            )
        if ylabelposition is not None:
            ax.yaxis.set_label_position(ylabelposition)
            #plt.setp(ax.get_yticklabels(), visible=True)
        return None
    return plot


@gen_action(["zlabel"], {**label_option, "zlabelposition": None, })
def set_zlabel(zlabel: str, *arg, zlabelposition=None, **kwargs) -> PlotAction:

    @gen_plotter
    def plot(ax):
        if zlabel and zlabel != False:
            ax.set_zlabel(
                zlabel,
                **kwargs
            )
        if zlabelposition is not None:
            ax.zaxis.set_label_position(zlabelposition)
            #plt.setp(ax.get_yticklabels(), visible=True)
        return None
    return plot


def twinx():
    def set_data(*arg):
        @gen_plotter
        def plot(ax):
            ax.twinx()
            return None
        return plot
    return set_data


def twiny():
    def set_data(*arg):
        @gen_plotter
        def plot(ax):
            ax.twiny()
            return None
        return plot
    return set_data
