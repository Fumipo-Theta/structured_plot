
from ..kit import gen_action, gen_plotter, get_subset, get_literal_or_series
from ..type_set import DataSource, PlotAction
from .artist_options import line2d_option


def iterable(i):
    return hasattr(i, "__iter__")


@gen_action(["data", "x", "y", "z"], {
    "fmt": None,
    "scalex": True,
    "scaley": True,
    **line2d_option
}
)
def line(
        data: DataSource,
        *arg,
        fmt=None,
        **kwargs)->PlotAction:
    f"""
    Plot line and/or marker.

    gen_action.line(x, y, [z], fmt=None, **kwargs)
    """

    if len(data) is 0:
        return gen_plotter(lambda ax: None)

    plot_data = [get_subset()(data, selector)
                 for selector in filter(lambda e: e is not None, arg)]

    if fmt is not None:
        plot_data += [fmt]

    new_kwargs = {k: get_literal_or_series(v, data) for k, v in kwargs.items()}

    @gen_plotter
    def plot(ax):
        return ax.plot(*plot_data,  **new_kwargs)
    return plot


plot = line
