from func_helper import identity, pip
import iter_helper as it
import dataframe_helper as dataframe
import dict_helper as dictionary
from data_loader import PathList
from .i_subplot import ISubplot
import pandas as pd
from typing import List, Tuple, Callable, Union, Optional, TypeVar
from iter_helper import DuplicateLast as Duplicated
from . import plot_action

DataSource = Union[dict, pd.DataFrame, pd.Series, PathList]
Ax = plot_action.Ax
AxPlot = plot_action.AxPlot
PlotAction = Callable[..., AxPlot]
DataTransformer = Callable[[pd.DataFrame], pd.DataFrame]
T = TypeVar("T")


def filter_dict(ref_keys):
    """
    Filter items in a dict by reference list of keys.
    """
    return lambda dictionary: dict(filter(lambda kv: kv[0] in ref_keys, dictionary.items()))


def mix_dict(target: dict, mixing: dict, consume: bool=False)->dict:
    """
    Overwrite items by only the key in the old dict.

    """
    d = {}
    for key in target.keys():
        if type(target[key]) is dict:
            d[key] = {
                **target[key], **(mixing.pop(key, {}) if consume else mixing.get(key, {}))}
        else:
            d[key] = mixing.pop(
                key, target[key]) if consume else mixing.get(key, target[key])
    return d, mixing


assert(mix_dict(
    {
        "xlabel": {"fontsize": 12}
    },
    {
        "xlim": [0, 1],
        "xlabel": {}
    }
) == ({'xlabel': {'fontsize': 12}}, {'xlim': [0, 1], 'xlabel': {}}))


def wrap_by_duplicate(a: Union[T, Duplicated])->Union[Duplicated]:
    """
    Wrap not tuple parameter by tuple.
    """
    return a if type(a) is Duplicated else Duplicated(a)


def get_from_duplicated(it: Duplicated, i: int, default=None):
    """
    Take ith item in Duplicated.
    If length of Duplicated is 0, default value is used.
    """
    if len(it) is 0:
        return default
    return it[i]


class Subplot(ISubplot):
    """
    dict, pandas.DataFrame, ファイルを指定し, プロット方法とプロット設定を指定する.
    Figureオブジェクトに登録することで最終的にプロットが作成される.

    Example
    -------
    fig=Figure():

    line_and_scatter_plot = Subplot(axStyle)\
            .add(
                data=PathList.match(pattern1,pattern2,...)(directory),
                dataInfo={
                    "header": 3
                },
                plot=[plot_action.scatter(),plot_action.line()],
                x="x_column_name_in_data",
                y="y_column_name_in_data",
                ylim=[25,35],
                xlabel=r"$x$",
                ylabel="Y axis label"
            )

    fig.add_subplot(
        line_and_scatter_plot
    ).show(size=(6,6))
    """

    @staticmethod
    def create_empty_space():
        """
        Create empty space.
        Any plot and axis are not drawn.
        """
        return Subplot().add(
            plot=[lambda df, opt: Subplot.__noDataAx]
        )

    def __new__(cls, *arg, **kwargs):
        return super().__new__(cls)

    def __add__(self, subplot):
        new_subplot = self.forked()
        for i in range(len(subplot)):
            new_subplot.add(
                **dictionary.mix(
                    {
                        "data": subplot.data[i],
                        "dataInfo": subplot.dataInfo[i],
                        "index": subplot.index_name[i],
                        "plot": subplot.plotMethods[i],
                        "second_axis": subplot.is_second_axes[i],
                        "transformer": subplot.dataTransformer[i],
                    },
                    subplot.option[i]
                )
            )
        return new_subplot

    def __len__(self):
        return self.length

    def __repr__(self):
        return f"""Subplot with length {len(self)}
        Axes spec: {self.axes_spec}
        First axis style: {self.get_first_axis_style()}
        Second axis style: {self.get_second_axis_style()}
        """

    def __init__(self, *style_dict, axes_spec={}, **style):
        self.axes_spec = axes_spec
        self.data = []
        self.dataInfo = []
        self.index_name = []
        self.dataTransformer = []
        self.plotMethods = []
        self.option = []
        self.is_second_axes = []
        self.filter_x = False
        self._isTest = False

        default_axes_style = {
            "title": {
                "fontsize": 16
            },
            "title_text": None,
            "cycler": None,
            "xlim": [],
            "ylim": [],
            "zlim": [],
            "label": {
                "fontsize": 16,
            },
            "xlabel": {},
            "ylabel": {},
            "zlabel": {},
            "scale": {
                "xscale": None,
                "yscale": None,
                "zscale": None,
            },
            "tick": {
                "labelsize": 14,
            },
            "xtick": {},
            "ytick": {},
            "ztick": {},
            "grid": {},
            "style": {}
        }

        _style = {**style_dict[0], **style} if len(
            style_dict) > 0 else style
        self.axes_style, rest_style = mix_dict(
            default_axes_style, _style, True)
        self.axes_style["style"].update({
            "xTickRotation": 0,
            **rest_style
        })

        self.diff_second_axes_style = {
            "title": {},
            "cycler": None,
            "xlim": [],
            "ylim": [],
            "zlim": [],
            "label": {},
            "xlabel": {},
            "ylabel": {},
            "zlabel": {},
            "scale": {},
            "tick": {},
            "xtick": {},
            "ytick": {},
            "ztick": {},
            "grid": {},
            "style": {}
        }

        _style = style_dict[1] if len(style_dict) > 1 else {}
        self.diff_second_axes_style, rest_style = mix_dict(
            self.diff_second_axes_style, _style)

        # print(self.axes_style)

        self.length = 0
        self.plotter = Subplot.Iplotter(plot_action)

    def get_axes_spec(self):
        return self.axes_spec

    def set_title(self, title=""):
        print("set_title() is deprecated. Use title option in add() method.")
        self.axes_style["title_text"] = title
        return self

    def get_first_axis_style(self)->dict:
        return self.axes_style

    def get_second_axis_style(self)->dict:
        return mix_dict(
            self.axes_style,
            self.diff_second_axes_style
        )[0]

    def show_title(self, ax):
        if self.axes_style["title_text"] is not None:
            ax.set_title(self.axes_style["title_text"],
                         **self.axes_style.get("title", {}))
        return ax

    def plot(self, ax, test=False):
        """
        pyplot.axsubplot -> pyplot.axsubplot

        Apply plot action functions to ax.

        Parameters
        ----------
        ax: pyplot.axsubplot

        test: bool, optional
            Flag for test plot mode.
            Default value is False.

        Return
        ------
        plotted_ax: pyplot.axsubplot
            Ax applied the plot actions.
        """

        self.set_test_mode(test)

        first_plot_actions = map(
            self.__getPlotAction,
            filter(lambda i: not self.is_second_axes[i], range(len(self)))
        )

        first_axis_style = self.get_first_axis_style()

        ax1 = pip(
            self.plotter(first_plot_actions, first_axis_style),
            self.show_title,
            self.setXaxisFormat()
        )(ax)

        if any(self.is_second_axes):
            second_axis_actions = map(
                self.__getPlotAction,
                filter(
                    lambda i: self.is_second_axes[i], range(len(self)))
            )

            second_xaxis_style = {**self.get_second_axis_style()}
            second_yaxis_style = {**self.get_second_axis_style()}

            # A hack for changing the first and the second axis limits independently.
            ax2 = pip(
                lambda ax: ax.twiny(),
                self.plotter([], second_xaxis_style),
                lambda ax: ax.twinx(),
                self.plotter(second_axis_actions, second_yaxis_style)
            )(ax1)

            return (ax1, ax2)
        else:
            return ax1

    @staticmethod
    def Iplotter(plot_action):
        def plotter(actions, style):
            """
            Plot actions for setting axes style

            * cycler
            * axis scale
            * axis range
            * axis ticks
            * axis labels
            * axis grids
            """
            return pip(
                plot_action.set_cycler(style["cycler"]),
                *actions,
                plot_action.axis_scale()({}, style["scale"]),
                plot_action.set_xlim()({}, {"xlim": style["xlim"]}),
                plot_action.set_ylim()({}, {"ylim": style["ylim"]}),
                plot_action.set_zlim()({}, {"zlim": style["zlim"]}),
                plot_action.set_tick_parameters(axis="both")(
                    {}, style["tick"]),
                plot_action.set_tick_parameters(axis="x")(
                    {}, {**style["tick"], **style["xtick"]}),
                plot_action.set_tick_parameters(axis="y")(
                    {}, {**style["tick"], **style["ytick"]}),
                plot_action.set_tick_parameters(axis="z")(
                    {}, {**style["tick"], **style["ytick"]}),

                plot_action.set_xlabel()(
                    {}, {**style["label"], **style["xlabel"]}),
                plot_action.set_ylabel()(
                    {}, {**style["label"], **style["ylabel"]}),
                plot_action.set_zlabel()(
                    {}, {**style["label"], **style["zlabel"]}),
                plot_action.set_grid()({}, style["grid"])
            )
        return plotter

    def __getPlotAction(self, i):
        dfs: Duplicated = self.read(i)
        opt = self.get_option(i)

        if len(dfs) == 0:
            return Subplot.__noDataAx
        if all(map(lambda df: len(df) is 0, dfs.args)):
            return Subplot.__noDataAx

        return lambda ax: pip(
            *[f(dfs, opt) for f in self.plotMethods[i]],
        )(ax)

    def read(self, i)->Tuple[pd.DataFrame]:
        """
        Indipendent from type of data source.
        """
        data: Duplicated = wrap_by_duplicate(self.data[i])
        meta: Duplicated = wrap_by_duplicate(self.dataInfo[i])
        default_transformers: Duplicated = self.default_transformers(i)
        data_transformers: Duplicated = wrap_by_duplicate(
            self.dataTransformer[i])

        max_len = pip(
            it.mapping(len),
            it.reducing(lambda acc, e: acc if acc > e else e)(0)
        )([data, meta, default_transformers, data_transformers])

        dfs = []
        for j in range(max_len):
            d = get_from_duplicated(data, j, {})
            m = get_from_duplicated(meta, j, {})
            def_trans = get_from_duplicated(default_transformers, j, [])
            trans = get_from_duplicated(data_transformers, j, [])

            loader = ISubplot.IDataLoader(d, self.isTest())

            if self.isTest():
                transformers = None
            else:
                transformers = def_trans + trans

            dfs.append(loader.read(d, meta=m,
                                   transformers=transformers))
        return Duplicated(*dfs)

    def default_transformers(self, i)->tuple:
        def filterX(df):
            x = self.option[i].get("x", None)
            lim = self.axes_style.get("xlim")
            if len(lim) is 0 or lim is None:
                return df
            elif len(lim) is 1:
                lower = lim[0]
                upper = None
            else:
                lower, upper, *_ = lim

            return dataframe.filter_between(
                lower, upper, False, False
            )(df, x) if self.filter_x else df

        data_len = len(self.data[i]) if type(self.data[i]) is Duplicated else 1

        return Duplicated(*[[filterX] for i in range(data_len)])

    def get_option(self, i):
        if self.isTest():
            return {**self.option[i], "y": "y"}
        else:
            return self.option[i]

    def add(self,
            data: Union[DataSource, Tuple[DataSource]]=None,
            dataInfo: dict={},
            index: Optional[Union[List[str], Tuple[List[str]]]]=None,
            transformer: Union[DataTransformer, List[DataTransformer], Tuple[DataTransformer], Tuple[List[DataTransformer]]]=identity,
            plot: List[PlotAction]=[],
            option: dict={},
            xlim: Optional[list]=None,
            ylim: Optional[list]=None,
            zlim: Optional[list]=None,
            xscale: Optional[str]=None,
            yscale: Optional[str]=None,
            zscale: Optional[str]=None,
            tick: dict={},
            xtick: dict={},
            ytick: dict={},
            ztick: dict={},
            xlabel: Optional[str]=None,
            ylabel: Optional[str]=None,
            zlabel: Optional[str]=None,
            title: Optional[str]= None,
            cycler=None,
            within_xlim: bool=False,
            second_axis: bool=False,
            **_kwargs):
        """
        Set parameters for plotting.

        Parameters
        ----------
        data, optional: DataSource, Tuple[DataSource]
            Data source as pandas.DataFrame, dict, and PathLike objects or tuple of them.
            Default value is {}.
        dataInfo, optional: dict
            Dict of parameters in reading data source files.
            Keys and values must be compatible to data loader
            such as pandas.read_csv and pandas.read_excel.
            Default value is {}.
        index, optional: List[str], Tuple[List[str]]
            List of str or tuple of it for column names used as
            index of dataframe.
            When list of column names is passed, values of index is made by concatenating the columns.
            Default value is None.
        transformer, optional: DataTransformer, List[DataTransformer], Tuple[DataTransformer], Tuple[List[DataTransformer]]
            Functions for transforming dataframe object prior to plot.
        plot, optional: List[PLotAction]
            List of plot actions.
        xlim, ylim, zlim, optional: List[int,float]
            List of numbers for defining limit of xy axis.
        title, optional: str
            String of subplot title.
        xscale, yscale, zscale, optional: str
            Str of type of axis scale.
            "linear", "log" can be used.
        tick, xtick, ytick, ztick, optional: dict
            Dict defining style of ticks.
        xlabel, ylabel, zlabel, optional: str
            Str label of axis.
        within_xlim, optional: bool
            Flag whether plot only data in xlim.
        second_axis, optinal: bool
            Flag for plot on second axis.

        **kwargs:
            Parameters passed to PlotActions.
            They are broad casted on all PlotActions.
        """

        kwargs = {**_kwargs}
        self.data.append(data)

        # index name of data source
        self.index_name.append(index)
        self.dataInfo.append(dataInfo)

        update_axes_style = dictionary.mix(
            {
                "label": dictionary.mix(
                    {"xlabel": xlabel} if xlabel is not None else {},
                    {"ylabel": ylabel} if ylabel is not None else {},
                    {"zlabel": zlabel} if zlabel is not None else {}
                ),
                "scale": dictionary.mix(
                    {"xscale": xscale} if xscale is not None else {},
                    {"yscale": yscale} if yscale is not None else {},
                    {"zscale": zscale} if zscale is not None else {}
                ),
                "tick": dictionary.mix(
                    tick,
                    filter_dict([
                        "labelbottom",
                        "labeltop",
                        "labelleft",
                        "labelright",
                        "bottom",
                        "top",
                        "left",
                        "right"
                    ])(kwargs)
                ),
                "xtick": xtick,
                "ytick": ytick,
                "ztick": ztick,
            },
            kwargs.get("limit", {}),
            {"xlim": xlim} if xlim is not None else {},
            {"ylim": ylim} if ylim is not None else {},
            {"zlim": zlim} if zlim is not None else {},
            {"title_text": title} if title is not None else {},
        )

        if not second_axis:
            self.axes_style, _ = mix_dict(
                self.axes_style,
                update_axes_style
            )
        else:
            self.diff_second_axes_style, _ = mix_dict(
                self.diff_second_axes_style,
                update_axes_style
            )

        # plot
        self.plotMethods.append(plot if type(plot) is list else [plot])

        # plot option
        _option = dictionary.mix(option, kwargs)
        self.option.append(_option)

        # transformer
        self.dataTransformer.append(
            transformer if type(transformer) in [list, tuple] else [transformer])

        self.filter_x = within_xlim
        self.is_second_axes.append(second_axis)

        self.length = self.length+1
        return self

    def forked(self,
               *option,
               **style_kwargs
               ):
        """
        Method for extends a subplot to the another subplot.
        Without any option, a subplot instance is copied to
        the new one.
        On the other hand, with option, part of properties of
        the old subplot can be over written.

        Parameters
        ----------
        *option: *dict
            Keys and values must be compatible to parameters
                for register() or add() method.
        title: str
        **style_kwargs:
            Overwrite style of axes
            ----------------------
            title: dict
            cycler: cycler
            xlim: list
            ylim: list
            label: dict
            scale: dict
            tick: dict
            xtick: dict
            ytick: dict

            xTickRotation
            xFmt
        """

        new_subplot = type(self)(
            **mix_dict(self.axes_style,
                       style_kwargs)[0],
            axes_spec=self.axes_spec
        )

        new_subplot.diff_second_axes_style = {**self.diff_second_axes_style}

        for i in range(len(self)):
            new_subplot.add(
                **dictionary.mix(
                    {
                        "data": self.data[i],
                        "dataInfo": self.dataInfo[i],
                        "index": self.index_name[i],
                        "plot": self.plotMethods[i],
                        "second_axis": self.is_second_axes[i],
                        "transformer": self.dataTransformer[i],
                    },
                    self.option[i],
                    option[i] if len(option) > i and type(
                        option[i]) is dict else {},
                )
            )

        return new_subplot

    @staticmethod
    def __noDataAx(ax):
        ax.axis("off")
        return ax

    def setXaxisFormat(self):
        def f(ax):
            return ax
        return f

    def set_test_mode(self, test):
        self._isTest = test
        return self

    def isTest(self):
        return self._isTest
