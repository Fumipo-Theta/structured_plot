from .action import default_kwargs, plot_action, generate_arg_and_kwags, get_value, get_subset, get_literal_or_series
from .action import DataSource, AxPlot, SetData, Selector, LiteralOrSequencer


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


@plot_action(["x", "y", "z"], contour_option)
def contourf(
        data: DataSource,
        x: Selector,
        y: Selector,
        z: Selector,
        **kwargs
)->AxPlot:
    _x = get_subset()(data, x)
    _y = get_subset()(data, y)
    _z = get_subset()(data, z)

    def plot(ax):

        ax.contourf(_x, _y, _z, **kwargs)
        return ax

    return plot


@plot_action(["x", "y", "z"], contour_option)
def contour(
        data: DataSource,
        x: Selector,
        y: Selector,
        z: Selector,
        **kwargs
)->AxPlot:
    _x = get_subset()(data, x)
    _y = get_subset()(data, y)
    _z = get_subset()(data, z)

    def plot(ax):
        print(kwargs)
        ax.contourf(_x, _y, _z, **kwargs)
        return ax

    return plot
