from ..kit import gen_action,  get_subset, Iget_factor
from ..type_set import DataSource, PlotAction


fill_option = {
    "color": "green",
    "cmap": None,
    "alpha": 0.5,
    "facecolor": None,
    "hatch": None,
}


@gen_action(["data", "x", "y"],
            {
    "y2": 0,
    **fill_option,
    "color": "blue"
})
def fill_between(data, x, y, y2=0, cmap=None, **kwargs)->PlotAction:
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


@gen_action(["data", "x", "y"],
            {
    "y2": 0,
    **fill_option,
    "color": "blue"
})
def fill(data, x, y, y2=0, cmap=None, **kwargs)->PlotAction:
    if len(data) is 0:
        return lambda ax: ax

    _x = get_subset()(data, x)
    _y = get_subset()(data, y)
    _y2 = get_subset()(data, y2)

    def plot(ax):
        ax.fill(_x, _y, _y2, **kwargs)
        return ax

    return plot
