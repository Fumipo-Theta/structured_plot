from .action import default_kwargs, plot_action, generate_arg_and_kwags, get_value, get_subset, Iget_factor
from .action import DataSource, AxPlot
import pandas as pd
import numpy as np
from func_helper import pip
import func_helper.func_helper.iterator as it


@plot_action(["x", "y", "yagg"],
             {
    **default_kwargs.get("bar"),
    "xfactor": None,
    "yfactor": None,
    "legend_labels": None,
    "legend": {}
})
def factor_bar(
    df: DataSource,
    x,  # factor1 selector
    y: str,  # stack factor selector
    yagg,  # aggregate
    *arg,
    xfactor=None,  # explicit factor list
    yfactor=None,  # explicit factor list
    norm=False,
    vert=True,
    legend_labels=None,
    legend={},
        **kwargs):
    """
    plot.bar(**presetting)(df, option, **kwargs)(ax)

    df: dict, pandas.DataFrame, numpy.ndarray

    option: dict
        x:
        y:
        agg:
        **other_option

    presetting, other_option,kwargs:
        xfactor:
        yfactor:
        norm: bool
        vert: bool
        legend: dict
        align: str
        width:
    """

    if len(df) is 0:
        return lambda ax: ax

    if type(y) is list:
        return bar(x=x, y=y,
                   yagg=yagg, xfactor=xfactor,
                   norm=norm, vert=vert,
                   legend_labels=legend_labels, legend=legend,
                   **kwargs)(df)

    """
    1. stacking bar plotのstackしていくgroupingをつくる
    """
    stack_series, stack_factor = Iget_factor(df, y, yfactor)
    stack_group = df.groupby(
        pd.Categorical(
            stack_series,
            ordered=True,
            categories=stack_factor
        )
    )

    """
    2. stack groupごとにそれぞれfactorごとにgroupingする.
        * すべてのstack groupごとにx_factorの長さが同じである必要があるので,
          全データに基づくcommon_x_factorを記録しておく.
    3.

    ax.bar(ind, bar_lengths_for_each_x_factor)
    """

    stack_bars = []
    for stack_name in stack_factor:
        subset = df.loc[stack_group.groups[stack_name]]

        x_factor_series, x_factor = Iget_factor(subset, x, xfactor)

        x_group = subset.groupby(
            pd.Categorical(
                x_factor_series,
                ordered=True,
                categories=x_factor
            )
        )

        subset_for_x_factor = [
            subset.loc[x_group.groups[xfname]]
            for xfname in x_factor
        ]

        stack_heights = pip(
            it.mapping(lambda df: df.agg(yagg).values),
            it.mapping(lambda arr: arr[0] if len(arr) > 0 else 0),
            list
        )(subset_for_x_factor)

        stack_bars.append(stack_heights)

    if norm:
        sum = pip(
            it.mapping(np.sum),
            list
        )(zip(*stack_bars))

        stack_bars = pip(
            it.mapping(lambda bars: pip(
                it.mapping(lambda t: 0 if t[1] in [
                           0, None, np.nan] else t[0]/t[1]),
                list
            )(zip(bars, sum))),
            list
        )(stack_bars)

    ind = list(range(len(x_factor)))
    plot_arg = {
        **kwargs,
        "tick_label": kwargs.get("tick_label", x_factor)
    }

    def plot(ax):
        prev_top = stack_bars[0]
        for i, bar in enumerate(stack_bars):
            if vert:
                if i is 0:
                    ax.bar(ind, bar, **plot_arg)
                else:
                    ax.bar(
                        ind, bar, bottom=prev_top, **plot_arg)
                    prev_top = [a+b for a, b in zip(prev_top, bar)]
            else:
                if i is 0:
                    ax.barh(ind, bar, **plot_arg)
                else:
                    ax.barh(
                        ind, bar, left=prev_top, **plot_arg)
                    prev_top = [a+b for a, b in zip(prev_top, bar)]

        if (legend is not None) and (legend is not False):
            ax.legend(
                stack_factor if legend_labels is None else legend_labels, **legend)

        if vert:
            # ax.set_xticks(ind)
            # ax.set_xticklabels(x_factor)
            ax.set_xlim([-1, len(x_factor)])
        else:
            # ax.set_yticks(ind)
            # ax.set_yticklabels(x_factor)
            ax.set_ylim([-1, len(x_factor)])

        return ax
    return plot


@plot_action(["x", "y", "yagg"],
             {
    **default_kwargs.get("bar"),
    "xfactor": None,
    "legend_labels": None,
    "legend": {}
})
def bar(
    df: DataSource,
    x,  # factor1 selector
    y: str,  # stack factor selector
    yagg,  # aggregate
    *arg,
    xfactor=None,  # explicit factor list
    norm=False,
    vert=True,
    legend_labels=None,
    legend={},
        **kwargs):
    """
    plot.bar(**presetting)(df, option, **kwargs)(ax)

    df: dict, pandas.DataFrame, numpy.ndarray

    option: dict
        x:
        y:
        agg:
        **other_option

    presetting, other_option,kwargs:
        xfactor:
        norm: bool
        vert: bool
        legend: dict
        align: str
        width:
    """

    stack_factor = y if type(y) is list else [y]
    stack_bars = []
    for stack_name in stack_factor:
        subset = df

        x_factor_series, x_factor = Iget_factor(subset, x, xfactor)

        x_group = subset.groupby(
            pd.Categorical(
                x_factor_series,
                ordered=True,
                categories=x_factor
            )
        )

        subset_for_x_factor = [
            subset.loc[x_group.groups[xfname]]
            for xfname in x_factor
        ]

        # aggrigation時にnanがあると, normalize時にsumがnanになる.
        # それを回避するためにfillna(0)してある.
        stack_heights = pip(
            it.mapping(lambda df: yagg(df[stack_name].fillna(0))),
            #it.mapping(lambda arr: arr[0] if len(arr) > 0 else 0),
            list
        )(subset_for_x_factor)

        stack_bars.append(stack_heights)

    if norm:
        sum = pip(
            it.mapping(np.sum),
            list
        )(zip(*stack_bars))

        stack_bars = pip(
            it.mapping(lambda bars: pip(
                it.mapping(lambda t: 0 if t[1] in [
                           0, None, np.nan] else t[0]/t[1]),
                list
            )(zip(bars, sum))),
            list
        )(stack_bars)

    ind = list(range(len(x_factor)))
    plot_arg = {
        **kwargs,
        "tick_label": kwargs.get("tick_label", x_factor)
    }

    def plot(ax):
        prev_top = stack_bars[0]
        for i, bar in enumerate(stack_bars):
            if vert:
                if i is 0:
                    ax.bar(ind, bar, **plot_arg)
                else:
                    ax.bar(
                        ind, bar, bottom=prev_top, **plot_arg)
                    prev_top = [a+b for a, b in zip(prev_top, bar)]
            else:
                if i is 0:
                    ax.barh(ind, bar, **plot_arg)
                else:
                    ax.barh(
                        ind, bar, left=prev_top, **plot_arg)
                    prev_top = [a+b for a, b in zip(prev_top, bar)]

        if (legend is not None) and (legend is not False):
            ax.legend(
                stack_factor if legend_labels is None else legend_labels, **legend)

        if vert:
            # ax.set_xticks(ind)
            # ax.set_xticklabels(x_factor)
            ax.set_xlim([-1, len(x_factor)])
        else:
            # ax.set_yticks(ind)
            # ax.set_yticklabels(x_factor)
            ax.set_ylim([-1, len(x_factor)])

        return ax
    return plot
