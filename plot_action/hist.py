from ..kit import gen_action, get_subset
from ..type_set import DataSource, PlotAction


hist_option = {
    "bins": None,
    "range": None,
    "density": None,
    "weights": None,
    "cumulative": False,
    "bottom": None,
    "histtype": 'bar',
    "align": 'mid',
    "orientation": 'vertical',
    "rwidth": None,
    "log": False,
    "color": "#2196f3",
    "label": None,
    "stacked": False,
    "normed": None,
}


@gen_action(["data", "y"],
            hist_option)
def hist(data: DataSource, y, *arg, **kwargs):
    _y = get_subset()(data, y)

    def plot(ax):
        ax.hist(_y, **kwargs)
        return ax
    return plot
