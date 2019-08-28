from .action import plot_action, get_subset, get_literal_or_series
from .action import DataSource, AxPlot, Selector
from .artist_options import line2d_option


def iterable(i):
    return hasattr(i, "__iter__")


@plot_action(["x", "y", "z"], {
    "fmt": None,
    "scalex": True,
    "scaley": True,
    **line2d_option
}
)
def line(
        df: DataSource,
        *arg,
        fmt=None,
        color=None,
        **kwargs)->AxPlot:
    f"""
    Plot line and/or marker.

    plot_action.line(x, y, [z], fmt=None, **kwargs)
    """

    if len(df) is 0:
        return lambda ax: ax

    plot_data = [get_subset()(df, selector)
                 for selector in filter(lambda e: e is not None, arg)]

    if fmt is not None:
        plot_data += [fmt]

    _color = get_literal_or_series(color, df)

    def plot(ax):
        ax.plot(*plot_data, color=_color, **kwargs)
        return ax
    return plot
