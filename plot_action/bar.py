from ..kit import gen_action, gen_plotter, get_subset, Iget_factor, get_literal_or_series
from ..type_set import DataSource, PlotAction
import pandas as pd
import numpy as np
from func_helper import pip
import iter_helper as it

bar_option = {
    "norm": False,
    "width": None,
    "color": "blue",
    "alpha": 1,
    "align": "center",
}


@gen_action(["data", "x", "y", "yagg"],
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
    data: DataSource,
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

    xfactor, yfactor:
        List of factor values or function generate it from dataframe.
        xfactor is used for grouping x axis variable.
        yfactor is used for grouping stacking variable.
    yagg:
        Function of aggrigating operation.

    factor_bar(
        x="group_column",
        xfactor=xfactors,
        y="stack_column",
        yfactor=yfactors,
        yagg=lambda group: group.count()
    )

    """

    if len(data) is 0:
        return lambda ax: ax

    if type(y) is list:
        return bar(
            x=x, y=y,
            yagg=yagg, xfactor=xfactor,
            norm=norm, vert=vert,
            legend_labels=legend_labels, legend=legend,
            **kwargs)(data)

    """
    1. stacking bar plotのstackしていくgroupingをつくる
    """
    stack_series, stack_factor, _ = Iget_factor(data, y, yfactor)
    stack_group = data.groupby(
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
        subset = data.loc[stack_group.groups[stack_name]]

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
                it.mapping(lambda t: 0 if (t[1] == 0) or np.isnan(t[1])
                           else t[0]/t[1]),
                it.mapping(lambda v: 0 if np.isnan(v) else v),
                list
            )(zip(bars, sum))),
            list
        )(stack_bars)

    plot_arg = {
        **kwargs,
        # "tick_label": kwargs.get("tick_label", x_factor)
    }

    @gen_plotter
    def plot(ax):
        prev_top = stack_bars[0]

        artists = []
        for i, bar in enumerate(stack_bars):
            # print(prev_top)
            if vert:
                if i is 0:
                    art = ax.bar(position, bar, **plot_arg)
                else:
                    art = ax.bar(
                        position, bar, bottom=prev_top, **plot_arg)
                    prev_top = [a+b for a, b in zip(prev_top, bar)]
                artists.append(art)
            else:
                if i is 0:
                    art = ax.barh(position, bar, **plot_arg)
                else:
                    art = ax.barh(
                        position, bar, left=prev_top, **plot_arg)
                    prev_top = [a+b for a, b in zip(prev_top, bar)]

                artists.append(art)

        if (legend is not None) and (legend is not False):
            ax.legend(
                stack_factor if legend_labels is None else legend_labels, **legend)

        if not show_factor_ticks:
            return artists

        if vert:
            ax.set_xticks(position)
            ax.set_xticklabels(x_factor)
            ax.set_xlim([-1, len(x_factor)])

        else:
            ax.set_yticks(position)
            ax.set_yticklabels(x_factor)
            ax.set_ylim([-1, len(x_factor)])

        return artists
    return plot


@gen_action(["data", "x", "y", "yagg"],
            {
    **bar_option,
    "xfactor": None,
    "legend_labels": None,
    "legend": {},
    "vert": True,
    "show_factor_ticks": True,
})
def bar(
    data: DataSource,
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
    Plot bars.

    xfactor:
        List of factor values or function generate it from dataframe.
    yagg:
        Function for aggligating y factor.
    """

    stack_factor = y if type(y) is list else [y]
    stack_bars = []
    for stack_name in stack_factor:
        subset = data

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

        # print(sum)

        stack_bars = pip(
            it.mapping(lambda bars: pip(
                it.mapping(lambda t: 0 if (t[1] == 0) or np.isnan(t[1])
                           else t[0]/t[1]),
                it.mapping(lambda v: 0 if np.isnan(v) else v),
                list
            )(zip(bars, sum))),
            list
        )(stack_bars)

    plot_arg = {
        **kwargs,
        # "tick_label": kwargs.get("tick_label", x_factor)
    }

    @gen_plotter
    def plot(ax):
        prev_top = stack_bars[0]
        artists = []

        for i, bar in enumerate(stack_bars):
            # print(prev_top)
            if vert:
                if i is 0:
                    art = ax.bar(position, bar, **plot_arg)
                else:
                    art = ax.bar(
                        position, bar, bottom=prev_top, **plot_arg)
                    prev_top = [a+b for a, b in zip(prev_top, bar)]
                artists.append(art)
            else:
                if i is 0:
                    art = ax.barh(position, bar, **plot_arg)
                else:
                    art = ax.barh(
                        position, bar, left=prev_top, **plot_arg)
                    prev_top = [a+b for a, b in zip(prev_top, bar)]
                artists.append(art)

        if (legend is not None) and (legend is not False):
            ax.legend(
                stack_factor if legend_labels is None else legend_labels, **legend)

        if not show_factor_ticks:
            return artists

        if vert:
            ax.set_xticks(position)
            ax.set_xticklabels(x_factor)
            ax.set_xlim([-1, len(x_factor)])

        else:
            ax.set_yticks(position)
            ax.set_yticklabels(x_factor)
            ax.set_ylim([-1, len(x_factor)])

        return artists
    return plot


@gen_action(
    ["data", "x", "y", "group"],
    {
        **bar_option,
        "xfactor": None,
        "gfactor": None,
        "cmap": None,
        "legend_labels": None,
        "legend": {},
        "color": None,
        "yerr": None,
    }
)
def group_bar(
    data: DataSource,
    x,
    y,
    group,
    *arg,
    xfactor=None,
    gfactor=None,
    yerr=None,
    legend_labels=None,
    legend={},
    width=0.9,
    norm: None,
    **kwargs
):
    """
    pre: Number and combination of x factors for each groups must be same.

    group_bar(
        x="x",
        y="y",
        xfactor=["A", "B"]
        group = "g",
        gfactor = ["group1", "group2"]
    )

    x    y     g
    A    1     group1
    B    1     group1
    A    2     group2
    B    NA    group2  <- required if y is NA

    """

    x_factor_series, x_factor, positions = Iget_factor(data, x, xfactor)
    g_factor_series, g_factor, _ = Iget_factor(data, group, gfactor)

    g_group = data.groupby(
        pd.Categorical(
            g_factor_series,
            ordered=True,
            categories=g_factor
        )
    )

    subsets = [
        data.loc[g_group.groups[gname]]
        for gname in g_factor
    ]

    each_width = width/len(g_factor)

    def shift(i, l, w): return - w*(l-1)/2 + w*i

    @gen_plotter
    def plot(ax):
        for i, subset in enumerate(subsets):
            _x = [p + shift(i, len(g_factor), each_width) for p in positions]
            _y = (get_subset()(subset, y))

            _yerr = get_subset()(subset, yerr) if yerr is not None else None

            try:
                ax.bar(_x, _y, width=each_width, yerr=_yerr, **kwargs)
            except Exception as e:
                print(_x)
                print(_y)
                raise e

        if (legend is not None) and (legend is not False):
            ax.legend(
                g_factor if legend_labels is None else legend_labels, **legend)

        ax.set_xticks(positions)
        ax.set_xticklabels(x_factor)
        ax.set_xlim([-1, len(x_factor)])

    return plot


@gen_action(
    ["data", "x", "y", "yagg"],
    {
        **bar_option,
        "xfactor": None,
        "cmap": None,
    }
)
def rose(
    data: DataSource,
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
    x_factor_series, x_factor, position = Iget_factor(data, x, xfactor)

    x_group = data.groupby(
        pd.Categorical(
            x_factor_series,
            ordered=True,
            categories=x_factor
        )
    )

    subset_for_x_factor = [
        data.loc[x_group.groups[xfname]]
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

    @gen_plotter
    def plot(ax):

        return ax.bar(position, heights, **plot_arg)

    return plot
