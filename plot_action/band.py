from .action import gen_action, get_subset, Icoordinate_transform
from ..type_set import DataSource, PlotAction
import numpy as np
import pandas as pd
from .artist_options import line2d_option


def iterable(i):
    return hasattr(i, "__iter__")


axline_option = {
    **line2d_option,
    "alpha": 0.5,
    "color": "green",
    "linewidth": None,
    "linestyle": "-"
}

fill_option = {
    "color": "green",
    "cmap": None,
    "alpha": 0.5,
    "facecolor": None,
    "hatch": None,
}


@gen_action(["data"],
            {**fill_option, "ypos": None})
def hband(data, *arg, ypos=None, **kwargs)->PlotAction:
    """
    Plot a horizontal band or line.

    ypos:
        If ypos is collection and length >= 2, plot as band.
        Else plot as line.

    ypos = 0             line at 0
    ypos = [0]           line at 0
    ypos = [0,1]         line at 0, 1
    ypos = [0,[0,1]]     line at 0 and band between 0,1
    ypos = [[0,1],[2,3]] band between 0,1 and 2,3
    ypos = zip([0,2],[1,3])   band between 0,1 and 2,3
    ypos = lambda df: df["y"] line at y in data source
    ypos = "y"                line at y in data source
    """

    def plot(ax):

        _ypos = get_subset()(data, ypos)

        if not iterable(_ypos):
            _kwargs = dict(
                filter(lambda kv: kv[0] in axline_option, kwargs.items())
            )
            ax.axhline(_ypos, **_kwargs)

        else:
            for item in _ypos:
                if iterable(item):
                    if len(item) >= 2:
                        ax.fill(
                            [0, 1, 1, 0],
                            [item[0], item[0], item[1], item[1]],
                            transform=Icoordinate_transform(
                                ax, "axes", "data"),
                            **kwargs
                        )
                    elif len(item) is 1:
                        _kwargs = dict(
                            filter(
                                lambda kv: kv[0] in axline_option, kwargs.items())
                        )
                        ax.axhline(item, **_kwargs)
                    else:
                        print(
                            "ypos must be list like object with having length >= 1.")

                else:
                    _kwargs = dict(
                        filter(
                            lambda kv: kv[0] in axline_option, kwargs.items())
                    )
                    ax.axhline(item, **_kwargs)

        return ax
    return plot


xband = hband


@gen_action(["data"],
            {**fill_option, "xpos": None})
def vband(data, *arg, xpos=None, **kwargs)->PlotAction:
    """
    Plot a vertical band or line.

    xpos:
        If xpos is collection and length >= 2, plot as band.
        Else plot as line.

    xpos = 0             line at 0
    xpos = [0]           line at 0
    xpos = [0,1]         line at 0, 1
    xpos = [0,[0,1]]     line at 0 and band between 0,1
    xpos = [[0,1],[2,3]] band between 0,1 and 2,3
    xpos = zip([0,2],[1,3])   band between 0,1 and 2,3
    xpos = lambda df: df["x"] line at x in data source
    """
    def plot(ax):

        _xpos = get_subset()(data, xpos)

        if not iterable(_xpos):
            _kwargs = dict(
                filter(lambda kv: kv[0] in axline_option, kwargs.items())
            )
            ax.axvline(_xpos, **_kwargs)

        else:
            for item in _xpos:
                if iterable(item):
                    if len(item) >= 2:
                        ax.fill(
                            [item[0], item[0], item[1], item[1]],
                            [0, 1, 1, 0],
                            transform=Icoordinate_transform(
                                ax, "data", "axes"),
                            **kwargs
                        )
                    elif len(item) is 1:
                        _kwargs = dict(
                            filter(
                                lambda kv: kv[0] in axline_option, kwargs.items())
                        )
                        ax.axvline(item, **_kwargs)
                    else:
                        print(
                            "xpos must be list like object with having length >= 1.")

                else:
                    _kwargs = dict(
                        filter(
                            lambda kv: kv[0] in axline_option, kwargs.items())
                    )
                    ax.axvline(item, **_kwargs)
        return ax
    return plot


yband = vband
