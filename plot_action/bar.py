from .action import default_kwargs, plot_action, generate_arg_and_kwags, get_value, get_subset, Iget_factor, get_literal_or_series
from .action import DataSource, AxPlot
import pandas as pd
import numpy as np
from func_helper import pip
import iter_helper as it


@plot_action(["x", "y", "yagg"],
             {
    "norm": False,
    "width": None,
    "color": "blue",
    "alpha": 1,
    "align": "center",
    "xfactor": None,
    "yfactor": None,
    "legend_labels": None,
    "legend": {},
    "vert": True,
    "show_factor_ticks": True,
})
def factor_bar(
    df: DataSource,
    x,  # factor1 selector
    y: str,  # stack factor selector
    yagg,  # aggregate
    *arg,
    xfactor=None,  # explicit factor list
    yfactor=None,  # explicit factor list
    width=None,
    color=None,
    norm=False,
    vert=True,
    legend_labels=None,
    legend={},
    show_factor_ticks=True,
        **kwargs):
    """
    Stacking bar plot.

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
    stack_series, stack_factor, _ = Iget_factor(df, y, yfactor)
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

        x_factor_series, x_factor, position = Iget_factor(subset, x, xfactor)

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

    plot_arg = {
        **kwargs,
        # "tick_label": kwargs.get("tick_label", x_factor)
    }

    def plot(ax):
        prev_top = stack_bars[0]
        for i, bar in enumerate(stack_bars):
            if vert:
                if i is 0:
                    ax.bar(position, bar, **plot_arg)
                else:
                    ax.bar(
                        position, bar, bottom=prev_top, **plot_arg)
                    prev_top = [a+b for a, b in zip(prev_top, bar)]
            else:
                if i is 0:
                    ax.barh(position, bar, **plot_arg)
                else:
                    ax.barh(
                        position, bar, left=prev_top, **plot_arg)
                    prev_top = [a+b for a, b in zip(prev_top, bar)]

        if (legend is not None) and (legend is not False):
            ax.legend(
                stack_factor if legend_labels is None else legend_labels, **legend)

        if not show_factor_ticks:
            return ax

        if vert:
            ax.set_xticks(position)
            ax.set_xticklabels(x_factor)
            ax.set_xlim([-1, len(x_factor)])
            pass
        else:
            ax.set_yticks(position)
            ax.set_yticklabels(x_factor)
            ax.set_ylim([-1, len(x_factor)])
            pass

        return ax
    return plot


@plot_action(["x", "y", "yagg"],
             {
    **default_kwargs.get("bar"),
    "xfactor": None,
    "legend_labels": None,
    "legend": {},
    "vert": True,
    "show_factor_ticks": True,
})
def bar(
    df: DataSource,
    x,  # factor1 selector
    y: str,  # stack factor selector
    yagg,  # aggregate
    *arg,
    color=None,
    xfactor=None,  # explicit factor list
    norm=False,
    vert=True,
    legend_labels=None,
    legend={},
    show_factor_ticks=True,
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

        x_factor_series, x_factor, position = Iget_factor(subset, x, xfactor)

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
            # it.mapping(lambda arr: arr[0] if len(arr) > 0 else 0),
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

    plot_arg = {
        **kwargs,
        # "tick_label": kwargs.get("tick_label", x_factor)
    }

    def plot(ax):
        prev_top = stack_bars[0]
        for i, bar in enumerate(stack_bars):
            if vert:
                if i is 0:
                    ax.bar(position, bar, **plot_arg)
                else:
                    ax.bar(
                        position, bar, bottom=prev_top, **plot_arg)
                    prev_top = [a+b for a, b in zip(prev_top, bar)]
            else:
                if i is 0:
                    ax.barh(position, bar, **plot_arg)
                else:
                    ax.barh(
                        position, bar, left=prev_top, **plot_arg)
                    prev_top = [a+b for a, b in zip(prev_top, bar)]

        if (legend is not None) and (legend is not False):
            ax.legend(
                stack_factor if legend_labels is None else legend_labels, **legend)

        if not show_factor_ticks:
            return ax

        if vert:
            ax.set_xticks(position)
            ax.set_xticklabels(x_factor)
            ax.set_xlim([-1, len(x_factor)])
            pass
        else:
            ax.set_yticks(position)
            ax.set_yticklabels(x_factor)
            ax.set_ylim([-1, len(x_factor)])
            pass
        return ax
    return plot


@plot_action(
    ["x", "y", "yagg"],
    {
        **default_kwargs.get("bar"),
        "xfactor": None,
        "cmap": None,
    }
)
def rose(
    df: DataSource,
    x,  # factor1 selector
    y: str,  # stack factor selector
    yagg,  # aggregate
    *arg,
    width=None,
    color=None,
    cmap=None,
    xfactor=None,  # explicit factor list
    norm=False,
    **kwargs
):
    x_factor_series, x_factor, position = Iget_factor(df, x, xfactor)

    x_group = df.groupby(
        pd.Categorical(
            x_factor_series,
            ordered=True,
            categories=x_factor
        )
    )

    subset_for_x_factor = [
        df.loc[x_group.groups[xfname]]
        for xfname in x_factor
    ]

    # aggrigation時にnanがあると, normalize時にsumがnanになる.
    # それを回避するためにfillna(0)してある.
    heights = pip(
        it.mapping(lambda df: yagg(df[y].fillna(0))),
        pd.Series
    )(subset_for_x_factor)

    colors = pip(
        it.mapping(lambda df: get_literal_or_series(color, df)),
        pd.Series
    )(subset_for_x_factor)

    if norm:
        sum = np.sum(heights)

        heights = heights.apply(
            lambda height: 0 if sum == 0 else height/sum)

    plot_arg = {
        "width": width,
        "color": colors,
        **kwargs
    }

    def plot(ax):
        ax.bar(position, heights, **plot_arg)

        return ax
    return plot
