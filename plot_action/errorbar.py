from ..kit import gen_action, gen_plotter, get_subset, get_literal_or_series
from ..type_set import DataSource, PlotAction, ActionGenerator, Selector, LiteralOrSequencer

default_option = {
    "xerr": None,
    "yerr": None,
    "fmt": "none",
    "markersize": None,
    "color": None,
    "markeredgecolor": None,
    "ecolor": "black",
    "elinewidth": None,
    "capsize": None,
    "alpha": 0.75,
}


@gen_action(["data", "x", "y"],
            default_option)
def errorbar(
    data: DataSource,
    x: Selector,
    y: Selector,
    *arg,
    xerr: Selector=None,
    yerr: Selector=None,
    **kwargs
)->PlotAction:

    if len(data) is 0:
        return gen_plotter(lambda ax: None)

    _x = get_subset()(data, x)
    _y = get_subset()(data, y)
    _xerr = get_subset()(data, xerr)
    _yerr = get_subset()(data, yerr)

    @gen_plotter
    def plot(ax):
        return ax.errorbar(_x, _y, xerr=_xerr, yerr=_yerr, **kwargs)

    return plot
