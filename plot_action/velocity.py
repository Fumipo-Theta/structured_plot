from ..kit import gen_action, get_subset
from ..type_set import DataSource, PlotAction


quiver_option = {
    "scale": 1,
    "scale_units": "dots",
    "alpha": 1,
    "color": "black",
    "width": 1,
    "headwidth": 0.1,
    "headlength": 0.2
}


@gen_action(["data", "x", "ex", "ey"],
            {**quiver_option,
             "scale": 1,
             "scale_units": "y",
             "alpha": 0.3,
             "color": "gray",
             "width": 0.001,
             "headwidth": 5,
             "headlength": 10
             })
def velocity(data: DataSource, x, ex, ey, *arg, **kwargs)->PlotAction:
    _x = get_subset()(data, x)
    _y = [0. for i in _x],
    _ex = get_subset()(data, ex)
    _ey = get_subset()(data, ey)

    def plot(ax):
        ax.quiver(_x, _y, _ex, _ey, **kwargs)
        return ax
    return plot
