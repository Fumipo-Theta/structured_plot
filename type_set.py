from typing import Callable, Dict, List, Optional, Tuple, TypeVar, Union, Any

import matplotlib
import pandas as pd

from .dummy_data import DummyData

Ax = matplotlib.axes._subplots.Axes
Fig = matplotlib.figure.Figure
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
