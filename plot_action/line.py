from .action import default_kwargs, plot_action, generate_arg_and_kwags, get_value, get_subset, get_literal_or_series
from .action import DataSource, AxPlot, Selector


def iterable(i):
    return hasattr(i, "__iter__")


@plot_action(["x", "y", "z"],
             default_kwargs.get("line"))
def line(
        df: DataSource,
        *arg,
        color=None,
        **kwargs)->AxPlot:

    if len(df) is 0:
        return lambda ax: ax

    plot_data = [get_subset()(df, selector)
                 for selector in filter(lambda e: e is not None, arg)]

    _color = get_literal_or_series(color, df)

    new_kwargs = {k: get_literal_or_series(v, df) for k, v in kwargs.items()}

    def plot(ax):
        ax.plot(*plot_data, color=_color, **new_kwargs)
        return ax
    return plot


@plot_action(["x", "y", "z"],
             default_kwargs.get("line"))
def line3d(
        df: DataSource,
        x: Selector,
        y: Selector,
        z: Selector,
        *arg,
        color=None,
        **kwargs)->AxPlot:

    if len(df) is 0:
        return lambda ax: ax

    _x = get_subset()(df, x)
    _y = get_subset()(df, y)
    _z = get_subset()(df, z)
    _color = get_literal_or_series(color, df)

    new_kwargs = {k: get_literal_or_series(v, df) for k, v in kwargs.items()}

    def plot(ax):
        ax.plot(_x, _y, _z, color=_color, **new_kwargs)
        return ax
    return plot
