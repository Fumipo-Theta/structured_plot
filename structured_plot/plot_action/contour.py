import numpy as np
import scipy.optimize as so
from ..kit import gen_action, gen_plotter, get_subset, get_literal_or_series
from ..type_set import DataSource, PlotAction, ActionGenerator, Selector, LiteralOrSequencer


contour_option = {
    "levels": None,
    "extend": "neither",  # | "both" | "min" | "max"
    "cmap": "viridis",
    "corner_mask": True,
    "colors": None,
    "alpha": 1,
    "vmin": None,
    "vmax": None,
    "extent": None,
    "linestyles": None,
    "linewidths": None,
    "hatches": None
}


@gen_action(["data", "x", "y", "z"], contour_option)
def contourf(
        data: DataSource,
        x: Selector,
        y: Selector,
        z: Selector,
        **kwargs
) -> PlotAction:
    _x = get_subset()(data, x)
    _y = get_subset()(data, y)
    _z = get_subset()(data, z)

    @gen_plotter
    def plot(ax):

        return ax.contourf(_x, _y, _z, **kwargs)

    return plot


@gen_action(["data", "x", "y", "z"], contour_option)
def contour(
        data: DataSource,
        x: Selector,
        y: Selector,
        z: Selector,
        **kwargs
) -> PlotAction:
    _x = get_subset()(data, x)
    _y = get_subset()(data, y)
    _z = get_subset()(data, z)

    @gen_plotter
    def plot(ax):
        print(kwargs)
        return ax.contour(_x, _y, _z, **kwargs)

    return plot


def find_confidence_interval(x, pdf, confidence_level):
    return pdf[pdf > x].sum() - confidence_level


@gen_action(["data", "x", "y", "xbins", "ybins"], contour_option | {"fill": False})
def density_contour(
    data: DataSource,
    x: Selector,
    y: Selector,
    xbins: int,
    ybins: int,
    fill: bool = False,
    **contour_kwargs
):
    _x = np.array(get_subset()(data, x))
    _y = np.array(get_subset()(data, y))

    _contour_kwargs = {**contour_kwargs}

    levels = _contour_kwargs.pop("levels", None) or [0.67, 0.95, 0.99]

    H, xedges, yedges = np.histogram2d(
        _x, _y, bins=(xbins, ybins), normed=True)
    x_bin_sizes = (xedges[1:] - xedges[:-1]).reshape((1, xbins))
    y_bin_sizes = (yedges[1:] - yedges[:-1]).reshape((ybins, 1))
    pdf = (H * (x_bin_sizes * y_bin_sizes))

    sigmas = list(map(lambda pval: so.brentq(find_confidence_interval, 0., 1., args=(pdf, pval)),
                      levels))
    _levels = np.sort(sigmas)

    X, Y = 0.5 * (xedges[1:] + xedges[:-1]), 0.5 * (yedges[1:] + yedges[:-1])
    Z = pdf.T

    @gen_plotter
    def plot(ax):
        ax_action = ax.contourf if fill else ax.contour
        print(ax_action)
        return ax_action(X, Y, Z, levels=_levels, origin="lower", **_contour_kwargs)

    return plot
