from .action import default_kwargs, gen_action, generate_arg_and_kwags, get_value, get_subset
from ..type_set import DataSource, PlotAction


@gen_action(["data", "x", "y"],
            {**default_kwargs.get("vlines"), "lower": 0})
def vlines(data: DataSource, x, y, *arg, lower=0, **kwargs)->PlotAction:
    if len(data) is 0:
        return lambda ax: ax

    _x = get_subset()(data, x)
    _y = get_subset()(data, y)

    def plot(ax):
        ax.vlines(
            _x, [lower for i in _x], _y, **kwargs
        )
        return ax
    return plot


@gen_action(["data", "x", "y"], {**default_kwargs.get("vlines"), "lower": 0})
def hlines(data, x, y, *arg, lower=0, **kwargs):
    if len(data) is 0:
        return lambda ax: ax

    _x = get_subset()(data, x)
    _y = get_subset()(data, y)

    def plot(ax):
        ax.hlines(
            _x, [lower for i in _x], _y, **kwargs
        )
        return ax
    return plot
