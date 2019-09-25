from ..kit import gen_action, get_subset
from ..type_set import DataSource, PlotAction

vhlines_option = {
    "color": None,
    "linestyle": "-",
    "linewidth": 1,
    "alpha": 1
}


@gen_action(["data", "x", "y"],
            {**vhlines_option, "lower": 0})
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


@gen_action(["data", "x", "y"], {**vhlines_option, "lower": 0})
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
