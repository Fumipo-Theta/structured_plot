from typing import Callable, Dict, List, Optional, Tuple, TypeVar, Union, Any
import inspect
import matplotlib
import pandas as pd

from .dummy_data import DummyData

Ax = matplotlib.axes._subplots.Axes
Fig = matplotlib.figure.Figure
Artists = List[matplotlib.artist.Artist]


Number = Union[int, float]
Padding = Dict[str, Number]
Size = Tuple[Number, Number]
Coordinate = Tuple[Number, Number]
BloadCastedSetting = Dict[str, Any]

DataSource = Union[dict, pd.DataFrame, pd.Series, DummyData]
DataTransformer = Callable[[pd.DataFrame], pd.DataFrame]
PlotAction = Callable[[Ax], Ax]
Plotter = Callable[[Any], PlotAction]
ActionGenerator = Callable[[DataSource, BloadCastedSetting], PlotAction]
Plot = Union[PlotAction, ActionGenerator,
             Callable[[Any, Any], Callable[[Ax], Ax]]]
ActionModifier = Callable[[dict], ActionGenerator]
Scalar = Union[int, float]
Selector = Optional[Union[Scalar, str, Callable[[DataSource], DataSource]]]
LiteralOrSequence = Optional[Union[int, float, str, list, tuple, DataSource]]
LiteralOrSequencer = Optional[Union[LiteralOrSequence,
                                    Callable[[DataSource], DataSource]]]


def is_PlotAction(func)->bool:
    sig = inspect.signature(func)
    is_unary = len(sig.parameters) is 1
    param_is_Ax = next(iter(sig.parameters.values())).annotation is Ax
    return_is_Ax = sig.return_annotation is Ax
    return is_unary and param_is_Ax and return_is_Ax


def is_unary(func)->bool:
    sig = inspect.signature(func)
    return len(sig.parameters) is 1


def is_binary(func)->bool:
    sig = inspect.signature(func)
    return len(sig.parameters) is 2


def iterable(v):
    return hasattr(v, "__iter__")
