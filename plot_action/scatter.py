from .action import plot_action,  get_subset, get_literal_or_series
from .action import DataSource, AxPlot, SetData, Selector, LiteralOrSequencer

scatter_option = {
    "c": None,
    "s": 20,
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


@plot_action(["x", "y", "z"],
             {**scatter_option})
def scatter(
    data: DataSource,
    *arg,
    c: LiteralOrSequencer=None,
    s: LiteralOrSequencer=20,
    **kwargs
)->AxPlot:
    """
    scatter(x, y, [z], **kwargs)

    Scatter plot in 2D or 3D coordinate.

    In 2D plot:
        x
        y

    In 3D plot:
        x
        y
        z
    """

    if len(data) is 0:
        return lambda ax: ax

    plot_data = [get_subset()(data, selector)
                 for selector in filter(lambda e: e is not None, arg)]

    colors = get_literal_or_series(c, data)
    sizes = get_literal_or_series(s, data)

    new_kwargs = {
        **kwargs,
        "s": sizes,
        "c": colors,
    }

    def plot(ax):
        ax.scatter(*plot_data, **new_kwargs)
        return ax
    return plot
