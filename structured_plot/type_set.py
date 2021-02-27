from __future__ import annotations
from typing import Callable, Dict, List, Optional, Tuple, TypeVar, Union, Any
import inspect
import matplotlib
import pandas as pd
import dataclasses
from .dummy_data import DummyData

Ax = matplotlib.axes._subplots.Axes
Fig = matplotlib.figure.Figure
Artists = List[matplotlib.artist.Artist]


Number = Union[int, float]
#Padding = Dict[str, Number]
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


@dataclasses.dataclass()
class Padding:
    """
    Padding sizes of a plot.

    `Padding.parse` is useful to create this instance.

    """
    top: float = 0.1
    left: float = 0.5
    bottom: float = 0.5
    right: float = 0.2

    @staticmethod
    def parse(pad: dict[str, float] | list[float]):
        if isinstance(pad, dict):
            return Padding(**pad)
        elif isinstance(pad, list):
            if len(pad) == 0:
                return Padding()
            elif len(pad) == 1:
                vert = lat = pad[0]
                return Padding(vert, lat, vert, lat)
            elif len(pad) == 2:
                vert, lat = pad
                return Padding(vert, lat, vert, lat)
            elif len(pad) == 3:
                vert, left, right = pad
                return Padding(vert, left, vert, right)
            elif len(pad) == 4:
                return Padding(*pad)
            else:
                raise ValueError("Length of padding must be <= 4.")
        else:
            raise ValueError("padding must be dict or list.")

    def __or__(self, pad: Padding):
        return Padding(**(dataclasses.asdict(self) | dataclasses.asdict(pad)))


def is_PlotAction(func) -> bool:
    sig = inspect.signature(func)
    is_unary = len(sig.parameters) == 1
    param_is_Ax = next(iter(sig.parameters.values())).annotation is Ax
    return_is_Ax = sig.return_annotation is Ax
    return is_unary and param_is_Ax and return_is_Ax


def is_unary(func) -> bool:
    sig = inspect.signature(func)
    return len(sig.parameters) == 1


def is_binary(func) -> bool:
    sig = inspect.signature(func)
    return len(sig.parameters) == 2


def iterable(v):
    return hasattr(v, "__iter__")
