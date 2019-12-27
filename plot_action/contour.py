from ..kit import gen_action, gen_plotter, get_subset, get_literal_or_series
from ..type_set import DataSource, PlotAction, ActionGenerator, Selector, LiteralOrSequencer


contour_option = {
    "levels": None,
    "extend": "neither",  # | "both" | "min" | "max"
    "cmap": None,
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
)->PlotAction:
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
)->PlotAction:
    _x = get_subset()(data, x)
    _y = get_subset()(data, y)
    _z = get_subset()(data, z)

    @gen_plotter
    def plot(ax):
        print(kwargs)
        return ax.contour(_x, _y, _z, **kwargs)

    return plot
