from ..kit import gen_action, gen_plotter, get_subset
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
        return gen_plotter(lambda ax: None)

    _x = get_subset()(data, x)
    _y = get_subset()(data, y)

    @gen_plotter
    def plot(ax):
        return ax.vlines(
            _x, [lower for i in _x], _y, **kwargs
        )
    return plot


@gen_action(["data", "x", "y"], {**vhlines_option, "lower": 0})
def hlines(data, x, y, *arg, lower=0, **kwargs):
    if len(data) is 0:
        return gen_plotter(lambda ax: None)

    _x = get_subset()(data, x)
    _y = get_subset()(data, y)

    @gen_plotter
    def plot(ax):
        return ax.hlines(
            _x, [lower for i in _x], _y, **kwargs
        )
    return plot
