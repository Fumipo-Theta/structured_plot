from ..kit import gen_action, get_subset, get_literal_or_series
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

    def plot(ax):

        ax.contourf(_x, _y, _z, **kwargs)
        return ax

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

    def plot(ax):
        print(kwargs)
        ax.contour(_x, _y, _z, **kwargs)
        return ax

    return plot
