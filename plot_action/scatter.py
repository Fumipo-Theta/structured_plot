from .action import default_kwargs, plot_action, generate_arg_and_kwags, get_value, get_subset, get_literal_or_series
from .action import DataSource, AxPlot, SetData, Selector, LiteralOrSequencer

scatter_option = {
    "c": None,
    "s": None,
    "cmap": None,
    "norm": None,
    "vmin": None,
    "vmax": None,
    "alpha": 1,
    "marker": "o",
    "facecolor": None,
    "edgecolors": "face",
    "linewidth": None,
    "linestyle": "-"
}


@plot_action(["x", "y"],
             {**scatter_option})
def scatter(
    data: DataSource,
    x: Selector,
    y: Selector,
    *arg,
    c: LiteralOrSequencer=None,
    s: LiteralOrSequencer=None,
    cmap=None,
    vmin=None,
    vmax=None,
    norm=None,
    **kwargs
)->AxPlot:

    if len(data) is 0:
        return lambda ax: ax

    _x = get_subset()(data, x)
    _y = get_subset()(data, y)

    colors = get_literal_or_series(c, data)
    sizes = get_literal_or_series(s, data)
    new_kwargs = {
        **{k: get_literal_or_series(v, data) for k, v in kwargs.items()},
        "s": sizes,
        "c": colors,
        "cmap": cmap,
        "vmin": vmin,
        "vmax": vmax,
        "norm": norm,
    }

    def plot(ax):
        ax.scatter(_x, _y, **new_kwargs)
        return ax
    return plot


@plot_action(["x", "y", "z"],
             {**scatter_option})
def scatter3d(
    data: DataSource,
    x: Selector,
    y: Selector,
    z: Selector,
    *arg,
    c: LiteralOrSequencer=None,
    s: LiteralOrSequencer=20,
    cmap=None,
    vmin=None,
    vmax=None,
    norm=None,
    **kwargs
)->AxPlot:

    if len(data) is 0:
        return lambda ax: ax

    _x = get_subset()(data, x)
    _y = get_subset()(data, y)
    _z = get_subset()(data, z)

    colors = get_literal_or_series(c, data)
    sizes = get_literal_or_series(s, data)
    new_kwargs = {
        **{k: get_literal_or_series(v, data) for k, v in kwargs.items()},
        "s": sizes,
        "c": colors,
        "cmap": cmap,
        "vmin": vmin,
        "vmax": vmax,
        "norm": norm,
    }

    def plot(ax):

        ax.scatter(_x, _y, _z, **new_kwargs)
        return ax
    return plot
