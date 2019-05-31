from .action import default_kwargs, plot_action, generate_arg_and_kwags, get_value, get_subset
from .action import DataSource, AxPlot


@plot_action(["x", "y"],
             {**default_kwargs.get("vlines"), "lower": 0})
def vlines(df: DataSource, x, y, *arg, lower=0, **kwargs)->AxPlot:
    if len(df) is 0:
        return lambda ax: ax

    _x = get_subset()(df, x)
    _y = get_subset()(df, y)

    def plot(ax):
        ax.vlines(
            _x, [lower for i in _x], _y, **kwargs
        )
        return ax
    return plot
