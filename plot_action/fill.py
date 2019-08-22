from .action import default_kwargs, plot_action, generate_arg_and_kwags, get_value, get_subset, Iget_factor
from .action import DataSource, AxPlot


fill_option = {
    "color": "green",
    "cmap": None,
    "alpha": 0.5,
    "facecolor": None,
    "hatch": None,
}


@plot_action(["x", "y"],
             {
    "y2": 0,
    **fill_option,
    "color": "blue"
})
def fill_between(data, x, y, y2=0, cmap=None, **kwargs)->AxPlot:
    if len(data) is 0:
        return lambda ax: ax

    _x = get_subset()(data, x)
    _y = get_subset()(data, y)
    _y2 = get_subset()(data, y2)

    print(kwargs)

    def plot(ax):
        ax.fill_between(_x, _y, _y2, **kwargs)
        return ax

    return plot


@plot_action(["x", "y"],
             {
    "y2": 0,
    **fill_option,
    "color": "blue"
})
def fill(data, x, y, y2=0, cmap=None, **kwargs)->AxPlot:
    if len(data) is 0:
        return lambda ax: ax

    _x = get_subset()(data, x)
    _y = get_subset()(data, y)
    _y2 = get_subset()(data, y2)

    def plot(ax):
        ax.fill(_x, _y, _y2, **kwargs)
        return ax

    return plot
