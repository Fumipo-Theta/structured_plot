from .action import default_kwargs, gen_action, generate_arg_and_kwags, get_value, get_subset
from ..type_set import DataSource, PlotAction


@gen_action(["data", "y"],
            default_kwargs.get("hist"))
def hist(data: DataSource, y, *arg, **kwargs):
    _y = get_subset()(data, y)

    def plot(ax):
        ax.hist(_y, **kwargs)
        return ax
    return plot
