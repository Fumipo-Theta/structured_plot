import pandas as pd
import functools
from typing import List, Tuple, Callable, NewType, Optional
from func_helper import pip
import iter_helper as it
from iter_helper import DuplicateLast
from ..dummy_data import DummyData

from ..type_set import DataSource, PlotAction, Plotter, ActionGenerator, ActionModifier, Scalar, Selector, LiteralOrSequence, LiteralOrSequencer



def iterable(i):
    return hasattr(i, "__iter__")

def stringify_dict(d):
    return it.reducing(lambda acc, kv: f"{acc}\n{kv[0]}: {kv[1]}")("")(d.items())


def diff_of_list(current, reference):
    return list(filter(lambda e: e not in reference, current))

def notify_unsued_options(l):
    if len(l) > 0:
        print(f"Option not used: {l}")

def gen_action(required_args: List[str], default_parameters: dict = {})->Callable[[Plotter], ActionModifier]:
    """
    Decorater function to generate ActionModifier function from Plotter function.

    Parameters
    ----------
    required_args: List[str]
    default_parameters: dict

    Return
    ------
    Callable[[Plotter], ActionModifier]
        Function taking a Plotter and returns binary function taking a dict and keyword args.

    Detail
    ------
    gen_action takes two types of parameters.
    1. List of required args of ActionModifier.
    2. Dict of default parameters of AcionModifier.

    ActionModifier enables you to make customizable PlotAction easily, which has a signature:

    ActionModifier: (provisional_parameters: dict, **prior_parameters: Any)
                    -> (DataSource, broadcasted_parametes: dict)
                    -> PlotAction

    PlotAction has a simple signature: Axes -> Axes.
    Then it is not flexible in reuse.
    ActionModifier takes three types of parameters used in PlotAction.

    The priority of the parameters with the same name is:
    1. prior_parameters
    2. broadcasted_parameters
    3. provisional_parameters
    4. default_parameters


    Example
    -------
    The decorated function should take some parameter to use in PlotAction and
        return function of PlotAction.

    @gen_action(["data","x","y"], {"c":"C0","s":20,"alpha":1})
    def scatter_modifier(data, x, y, **parameters)->PlotAction:
        def plot_action(ax: Axes)->Axes:
            # Something special to make plot
            ax.scatter(data[x], data[y], **parameters)
            return ax
        return plot_action

    The decorated function recieves the only args and parameters which are included
        in the required_args or default_parameters. The other parameters are ignored.
    In the case above, only parameters of "data", "x", "y", "c", "s", and "alpha" are accepted.

    From the scatter_modifier, you can make function which generate cutomized PlotAction.

    plot_half_visible_circle = scatter_modifier({"alpha":0.5})
    plot_red_dot = scatter_modifier({"s":1}, c="red")

    The first function defines PlotAction drawing partially transparent scatter plot.
        The parameter "alpha" is set as 0.5 if it is not override by broadcasted parameters.
    The second one defines PlotAction drawing scatter plot with red dot.
        The parameter "s" may be override, otherwise the parameter "c" is fixed as red.

    """
    arg_filter = get_values_by_keys(required_args, None)
    kwarg_filter = filter_dict(default_parameters.keys())

    def wrapper(plotter: Plotter)->ActionModifier:

        @functools.wraps(plotter)
        def action_modifier(
            provisional_settings: dict = {},
            verbose:bool=False,
            **priority_parameters
            )->ActionGenerator:
            """
            plot_action.line(provisional_setting, **priority_parameters)
            """

            def action_generator(data_source: DataSource, bloadcasted_settings: dict = {})->PlotAction:

                """
                Usage of decorated plotter

                @gen_action(required_args=[], default_parameters={})
                def plotter(*arg, **kwargs):
                    ...

                plotter(
                    provisional_setting={},
                    **priority_parameters
                )(data_source, broadcasted_settings={})


                **Priority of plot parameters**

                1. priority_parameters
                    Parameters passed to ActionModifier
                2. bloadcasted_settings
                    Dictionary passed to ActionGenerator
                3. provisional_settings
                    Dictionary passed to ActionModifier
                4. default_parameters
                    Dictionary passed to gen_action decorator

                """
                list_of_entry = to_flatlist({
                        "data": data_source,
                        **default_parameters,
                        **provisional_settings,
                        **bloadcasted_settings,
                        **priority_parameters,
                        })

                valid_args = list(map(arg_filter, list_of_entry))
                valid_kwargs = list(map(kwarg_filter, list_of_entry))


                arg_and_kwarg = generate_arg_and_kwags()(
                    valid_args,
                    valid_kwargs
                )

                if verbose:
                    print(plotter.__name__)
                    print(it.reducing(lambda acc,e: acc+f"args: {e[0]}\nkwargs: {e[1]}\n\n")("")(arg_and_kwarg))

                # return plot action
                return lambda ax: it.reducing(
                    lambda acc_ax, e: plotter(*e[0], **e[1])(acc_ax))(ax)(arg_and_kwarg)

            action_generator.__doc__ = f"""
                Prepere plot operation by Ax instance.

                Default Parameters
                ----------
                data_source: DataSource

                Reruired: {required_args}
                Default: {default_parameters}
                """

            return action_generator


        # Enable refer the original docstrings
        action_modifier.__doc__ = (plotter.__doc__ if plotter.__doc__ is not None else "") \
            + f"""
                Prepere plot operation by Ax instance.

                Default Parameters
                ----------
                data_source: DataSource

                Reruired: {required_args}
                Default: {default_parameters}
                """

        action_modifier.default_parameters=default_parameters

        return action_modifier
    return wrapper

"""
def as_DataFrame(d: DataSource) -> pd.DataFrame:
    if type(d) in [pd.DataFrame, pd.Series]:
        return d
    elif type(d) in [list, dict]:
        return pd.DataFrame(d)
    else:
        raise TypeError(f"{type(d)} is not available for data source.")
"""

def generate_arg_and_kwags():
    """
    Setup positional arguments and keyword arguments for plotter.
    """
    def gen_func(
        option: List[list],
        style: List[dict]
    )->List[Tuple[list, dict]]:

        if len(option) != len(style):
            raise SystemError("option and style must be same size list.")

        arg_and_kwarg = []
        for o, s in zip(option, style):
            arg = [*o]
            kwargs = s
            arg_and_kwarg.append((arg, kwargs))
        return arg_and_kwarg
    return gen_func


def get_subset(use_index=True)\
        ->Callable[[DataSource, Selector], DataSource]:
    """

    """
    def f(df: DataSource, k: Selector)->DataSource:
        """
        Select value in hashable (pandas.DataFrame, dict, etc.)
        """
        if type(df) is pd.DataFrame:
            if k in ["index", None]:
                return df.index
            elif type(k) is str:
                return df[k]
            elif type(k) in [int, float]:
                return k
            elif callable(k):
                return k(df)
            elif iterable(k):
                return k
            else:
                return df[k]

        elif type(df) is pd.Series:
            if k in ["index", None]:
                return df.index
            elif callable(k):
                return k(df)
            elif type(k) in [int, float]:
                return k
            elif iterable(k):
                return k
            else:
                return df

        elif type(df) is dict:
            if type(k) is str:
                return df.get(k, [])
            elif callable(k):
                return k(df)
            elif type(k) in [int, float]:
                return k
            elif iterable(k):
                return k
            else:
                return df

        elif type(df) is DummyData:
            return k

        else:
            # print(df)
            raise TypeError("df must be pandas.DataFrame or pandas.Series.")
    return f



def to_flatlist(d: dict) -> List[dict]:
    """
    Usage
    -----
    d = {
        "x" : (0,1,2),
        "y" : [1,2],
        "z" : 0
    }

    to_flatlist(d) is...
    [
        {"x" : 0, "y" : [1,2], "z" : 0},
        {"x" : 1, "y" : [1,2], "z" : 0},
        {"x" : 2, "y" : [1,2], "z" : 0}
    ]

    """
    def to_duplicate(d: dict) -> dict:
        return dict(it.mapping(
            lambda kv: (kv[0], kv[1]) if type(
                kv[1]) is DuplicateLast else (kv[0], DuplicateLast(kv[1]))
        )(d.items()))

    list_dict = to_duplicate(d)

    max_length = it.reducing(
        lambda acc, e: acc if acc >= len(e) else len(e)
    )(0)(list_dict.values())

    flatlist = []
    for i in range(max_length):
        new_dict = {}

        for k in list_dict.keys():
            new_dict.update({(k): list_dict[k][i]})

        flatlist.append(new_dict)
    return flatlist


def filter_dict(k: list) -> Callable[[dict], dict]:
    return lambda d: dict(
        filter(lambda kv: (kv[0] in k) and kv[1] is not None, d.items())
    )


def translate_table(table_dict: dict):
    return lambda d: {table_dict.get(k, k): v for k, v in d.items()}


def get_values_by_keys(k: list, default=None)->Callable[[dict], list]:
    """
    Filter dictionary by list of keys.

    Parameters
    ----------
    k: list
    default: any, optional
        Set as default value for key not in dict.
        Default value is None
    """
    return lambda d: list(map(lambda key: d.get(key, default), k))







def _annotate_plotter(df, from_pos, to_pos, text, *arg, textdict={}, **kwargs) -> PlotAction:
    def plot(ax):

        return ax
    return plot


def annotate(**action_modifier):
    return gen_action(
        _annotate_plotter,
        ["from_pos", "to_pos", "text"],
        {**_quiver_kwargs, "textdict": _text_kwargs}
    )(**action_modifier)
