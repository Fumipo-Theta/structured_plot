from .action import plot_action,  get_subset, selector_or_literal, Icoordinate_transform
from .action import DataSource, AxPlot

default_option = {
    "text": None,
    "ha": 'left',
    "va": 'bottom',
    "color": "black",
    "family": None,
    "fontsize": 10,
    "rotation": None,
    "style": None,
    "xcoordinate": None,  # "data" = None | "axes"
    "ycoordinate": None,  # "data" = None | "axes"
    "wrap": False
}


@plot_action(["x", "y", "z"],
             default_option)
def text(df: DataSource, *arg,
         xcoordinate=None,
         ycoordinate=None,
         **kwargs):
    """
    Plot text on the graph.

    Parameters
    ----------
    x, y, [z]: Selector
        Text position.
    text: Selector
        Text content.

    xcoordinate: "data" | "axes"
    ycoordinate: "data" | "axes"
        Use coordinate based on data ar axes.
        Default value is "data"
    """

    t = kwargs.pop("text", None)
    if t is None:
        raise Exception("text parameter is required !")

    positions = [get_subset()(df, selector) for selector in arg]
    _text = get_subset()(df, t)

    def plot(ax):
        zipped = zip(*positions, _text) \
            if hasattr(ax, "set_zlim") else zip(*positions[0:-1], _text)

        for _arg in zipped:
            transform = Icoordinate_transform(ax, xcoordinate, ycoordinate)
            ax.text(*_arg, transform=transform, **kwargs)
        return ax
    return plot
