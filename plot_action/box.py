from .action import default_kwargs, gen_action, generate_arg_and_kwags, get_value, get_subset, Iget_factor
from ..type_set import DataSource, PlotAction
from typing import Union, List
import pandas as pd


@gen_action(["y"],
            default_kwargs.get("box"))
def box(df: DataSource, ys: Union[str, List[str]], *arg, **kwargs)->PlotAction:
    """
    Generate box plots for indicated columns.
    """
    _ys = ys if type(ys) is list else [ys]

    def plot(ax):
        ax.boxplot(
            [df[y].dropna() for y in _ys],
            labels=_ys,
            positions=range(0, len(_ys)),
            **kwargs
        )
        return ax
    return plot


@gen_action(["data", "x", "y"],
            {**default_kwargs.get("box"), "xfactor": None})
def factor_box(data: DataSource, x, y, xfactor=None, **kwargs)->PlotAction:
    """
    Generate box plots grouped by a factor column in DataFrame.

    """
    _factor_series, _factor, position = Iget_factor(data, x, xfactor)
    _factor_detector = pd.Categorical(
        _factor_series, ordered=True, categories=_factor)

    _group = data.groupby(_factor_detector)
    _data_without_nan = [data.loc[_group.groups[fname]][y].dropna()
                         for fname in _factor]

    def plot(ax):
        if len(_data_without_nan) is 0:
            print("No data for box plot")
            return ax
        ax.boxplot(
            _data_without_nan,
            labels=_factor,
            positions=position,
            **kwargs
        )

        if kwargs.get("vert", True):
            ax.set_xticks(position)
            ax.set_xticklabels(_factor)
            #ax.set_xlim([-1, len(_factor)])
        else:
            ax.set_yticks(position)
            ax.set_yticklabels(_factor)
            #ax.set_ylim([-1, len(_factor)])
        return ax
    return plot
