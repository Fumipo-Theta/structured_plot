from ..kit import gen_action, gen_plotter, get_subset, get_literal_or_series
from ..type_set import DataSource, PlotAction
from .artist_options import line2d_option


@gen_action(["data", "x", "y", "z"], {
    "fmt": None,
    "scalex": True,
    "scaley": True,
    **line2d_option
}
)
def plot(
        data: DataSource,
        *arg,
        fmt=None,
        **kwargs) -> PlotAction:
    f"""
    Plot line and/or marker.

    gen_action.line(x, y, [z], fmt=None, **kwargs)
    """
    plot_data = [get_subset()(data, selector)
                 for selector in filter(lambda e: e is not None, arg)]

    plot_data = [*arg]
    if fmt is not None:
        plot_data += [fmt]

    new_kwargs = {k: get_literal_or_series(v, data) for k, v in kwargs.items()}

    @gen_plotter
    def plot(ax):
        return ax.plot(*plot_data, **new_kwargs)
    return plot
