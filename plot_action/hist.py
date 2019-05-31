from .action import default_kwargs, plot_action, generate_arg_and_kwags, get_value, get_subset
from .action import DataSource, AxPlot


@plot_action(["y"],
             default_kwargs.get("hist"))
def hist(df: DataSource, y, *arg, **kwargs):
    _y = get_subset()(df, y)

    def plot(ax):
        ax.hist(_y, **kwargs)
        return ax
    return plot
