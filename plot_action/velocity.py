from .action import default_kwargs, gen_action, generate_arg_and_kwags, get_value, get_subset
from ..type_set import DataSource, PlotAction


@gen_action(["data", "x", "ex", "ey"],
            {**default_kwargs.get("quiver"),
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
