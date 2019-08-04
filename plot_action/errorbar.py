from .action import default_kwargs, plot_action, generate_arg_and_kwags, get_value, get_subset, get_literal_or_series
from .action import DataSource, AxPlot, SetData, Selector, LiteralOrSequencer

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


@plot_action(["x", "y"],
             default_option)
def errorbar(
    data: DataSource,
    x: Selector,
    y: Selector,
    *arg,
    xerr: Selector=None,
    yerr: Selector=None,
    **kwargs
)->AxPlot:

    if len(data) is 0:
        return lambda ax: ax

    _x = get_subset()(data, x)
    _y = get_subset()(data, y)
    _xerr = get_subset()(data, xerr)
    _yerr = get_subset()(data, yerr)

    def plot(ax):
        ax.errorbar(_x, _y, xerr=_xerr, yerr=_yerr, **kwargs)
        return ax
    return plot
