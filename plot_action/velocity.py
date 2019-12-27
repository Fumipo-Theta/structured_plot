from ..kit import gen_action, gen_plotter, get_subset
from ..type_set import DataSource, PlotAction


quiver_option = {
    "scale": 1,
    "scale_units": "dots",
    "alpha": 1,
    "color": "black",
    "width": 1,
    "headwidth": 0.1,
    "headlength": 0.2,
    "collect_artists": False
}


@gen_action(["data", "x", "ex", "ey"],
            {**quiver_option,
             "scale": 1,
             "scale_units": "y",
             "alpha": 0.3,
             "color": "gray",
             "width": 0.001,
             "headwidth": 5,
             "headlength": 10,
             })
def velocity(data: DataSource, x, ex, ey, *arg, collect_artists=False, **kwargs)->PlotAction:
    _x = get_subset()(data, x)
    _y = [0. for i in _x],
    _ex = get_subset()(data, ex)
    _ey = get_subset()(data, ey)

    @gen_plotter
    def plot(ax):
        artists = ax.quiver(_x, _y, _ex, _ey, **kwargs)
        if collect_artists:
            return artists
        else:
            return None
    return plot
