from .action import default_kwargs, plot_action, generate_arg_and_kwags, get_value, get_subset, selector_or_literal, Icoordinate_transform
from .action import DataSource, AxPlot

default_option = {
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


@plot_action(["x", "y", "text"],
             default_option)
def text(df: DataSource, x, y, text, *arg,
         xcoordinate=None,
         ycoordinate=None,
         **kwargs):
    _x = selector_or_literal(df, x)
    _y = selector_or_literal(df, y)
    _text = selector_or_literal(df, text)

    def plot(ax):
        for x, y, t in zip(_x, _y, _text):
            transform = Icoordinate_transform(ax, xcoordinate, ycoordinate)
            ax.text(x, y, t, transform=transform, **kwargs)
        return ax
    return plot
