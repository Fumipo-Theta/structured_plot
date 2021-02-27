# -*- coding: utf-8 -*-
from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
from func_helper import pip
from iter_helper import mapping, reducing
from .subgrid import Subgrid
from typing import List, Tuple, TypeVar, Callable, Union, Optional
from .type_set import Ax, Fig, Number, Padding, Size, Coordinate

T = TypeVar("T")
S = TypeVar("S")
U = TypeVar("U")


def vectorize(f: Callable[[S], U]) -> Callable[[T], T]:
    def apply(arg: T) -> T:
        if type(arg) is list:
            return [f(x) for x in arg]
        elif type(arg) is tuple:
            return tuple(f(x) for x in arg)
        elif type(arg) is dict:
            return {k: f(v) for k, v in arg.items()}
        else:
            return f(arg)
    return apply


def enum_iter(l):
    return reducing(lambda acc, e: f"{acc}\n{e}")("")(l)


class Layout:
    """
    Store information of:
        1. Store and update size of staging area of subplots
        2. Compute relative position of the new subplot to
            the former subplot
    """

    def __new__(cls, *arg, **kwargs):
        return super().__new__(cls)

    def __repr__(self):
        return f"""
        Layout
        ------
        size: {self.get_width()} x {self.get_height()} inches
        dpi: {self.dpi}
        subgrids: {len(self)} {self._subgrids.keys()} {enum_iter(map(
            pip(
                self.axes_position,
                lambda pos: f"left-bottom at ({pos[0]},{pos[1]}) & size of ({pos[2]} * {pos[3]})"
            ),
            self.get_all_subgrids()
            ))}
        """

    def __init__(self, padding: dict | list = {}, unit: str = "inches", dpi: str = 72):
        """
        Generate instance.
        With setup unit of length and dpi optionally.

        Parameters
        ----------
        unit: str, optional
            Unit of length for subplot sizes, margins of among them.
            "inches", "mm", "cm", or "px".
            Default value is "inches".
        dpi: int, optional
            Value of dot par inches.
            Necessary in translate inches to px.
            Default value is 72.

        """
        self.dpi = dpi
        self.origin = (0, 0)
        self.left_top = (0, 0)
        self.right_bottom = (0, 0)
        self.default_figure_style = {
            "facecolor": "white"
        }
        self.unit = unit
        unit_translator = Layout.IToDefaultUnit(unit, dpi)
        self.to_default_unit = unit_translator
        self.default_padding = Padding.parse(unit_translator(padding))
        self._subgrids = {}

    def __len__(self):
        return len(self._subgrids)

    def set_subgrid(self, subgrid, name=None):
        key = len(self) if name is None else name
        if key in self._subgrids:
            raise Exception(f"key {key} has already been resisterd !")
        self._subgrids[name] = subgrid

    def get_subgrids_order(self):
        return self._subgrids.keys()

    def get_a_subgrid(self, name=None) -> Optional[Subgrid]:
        """
        Retruns subgrid with a given name.

        Parameters
        ----------
        name: Optional[str]

        Return
        ------
        Optional[Subgrid]
        """
        return self._subgrids.get(name, None)

    def get_subgrids(self, names) -> List[Optional[Subgrid]]:
        """
        Returns list of subgrids matching their name.

        Parameters
        ----------
        names: List[Union[str,int]]

        Return
        ------
        List[Optional[Subgrid]]
        """
        if len(self) == 0:
            raise Exception("There is no subgrids.")

        return [self._subgrids[name] for name in names]

    def get_all_subgrids(self) -> List[Optional[Subgrid]]:

        return list(self._subgrids.values())

    @staticmethod
    def IToDefaultUnit(unit: str, dpi: int) -> Callable[[T], T]:
        if unit == "mm":
            return vectorize(lambda x: x / 25.4 if x else x)
        elif unit == "cm":
            return vectorize(lambda x: x / 2.54 if x else x)
        elif unit == "px":
            return vectorize(lambda x: x / dpi if x else x)
        else:
            return vectorize(lambda x: x)

    def get_padding(self, padding: dict | list) -> Padding:
        """
        Reset padding.

        Parameters
        ----------
        padding: dict, optional
            Defining size of padding around all subplots.
            The unit of size is inches.
            Padding of top, left, bottom, and right can be set.
            Default is {
                "top" : 0.1,
                "left" : 0.5,
                "bottom" : 0.5,
                "right" : 0.2
            }
        """
        new_pad = Padding.parse(self.to_default_unit(padding))
        return self.default_padding | new_pad

    def get_width(self) -> Number:
        """
        Width of rectangle containing all plot areas of subplots.
        Not containing axis and ticks area of subplots
            and padding area of the figure.
        """
        return (self.right_bottom[0] - self.left_top[0])

    def get_height(self) -> Number:
        """
        Hight of rectangle containing all plot areas of subplots.
        Not containing axis and ticks area of subplots
            and padding area of the figure.
        """
        return (self.right_bottom[1] - self.left_top[1])

    def get_size(self) -> Size:
        """
        Tuple of (Width, Hight) of rectangle containing
            all plot areas of subplots.
        Not containing axis and ticks area of subplots
            and padding area of the figure.
        """
        return (self.get_width(), self.get_height())

    def __expand(self, sg_origin: Coordinate, sg_size: Size):
        """
        Expanding rectangle of plot areas
            if the new subplot over the rectangle.
        """
        self.left_top = (
            np.min([self.left_top[0], sg_origin[0]]),
            np.min([self.left_top[1], sg_origin[1]])
        )

        self.right_bottom = (
            np.max([self.right_bottom[0], sg_origin[0] + sg_size[0]]),
            np.max([self.right_bottom[1], sg_origin[1] + sg_size[1]])
        )

    def add_origin(self, new_name, size: Size, offset: Size = (0, 0), **kwd):
        sg = self

        _offset = self.to_default_unit(offset)
        _size = self.to_default_unit(size)

        next_origin = (
            sg.origin[0] + _offset[0],
            sg.origin[1] + _offset[1]
        )

        next_size = (
            _size[0] if _size[0] is not None else sg.get_width() - _offset[0],
            _size[1] if _size[1] is not None else sg.get_height() - _offset[1]
        )

        self.__expand(next_origin, next_size)
        self.set_subgrid(Subgrid(next_size, next_origin, **kwd), new_name)
        return self

    def from_left_top(self, origin_name, new_name, size: Size, offset: Size = (0, 0), sharex=None, sharey=None, **kwd):
        """
        Layout a new subplot based on the position of
            left-top corner of the former subplot.
        """
        sg = self.get_subgrids([origin_name])[0]

        _offset = self.to_default_unit(offset)
        _size = self.to_default_unit(size)

        next_origin = (
            sg.origin[0] + _offset[0],
            sg.origin[1] + _offset[1]
        )

        next_size = (
            _size[0] if _size[0] is not None else sg.get_width() - _offset[0],
            _size[1] if _size[1] is not None else sg.get_height() - _offset[1]
        )

        self.__expand(next_origin, next_size)
        self.set_subgrid(Subgrid(next_size, next_origin, sharex=self.get_a_subgrid(
            sharex), sharey=self.get_a_subgrid(sharey), **kwd), new_name)
        return self

    def from_left_bottom(self, origin_name, new_name, size: Size, offset: Size = (0, 0), sharex=None, sharey=None, **kwd) -> Subgrid:
        _offset = self.to_default_unit(offset)
        _size = self.to_default_unit(size)

        sg = self.get_subgrids([origin_name])[0]

        next_size = (
            _size[0] if _size[0] is not None else sg.get_width() - _offset[0],
            _size[1] if _size[1] is not None else sg.get_height() - _offset[1]
        )

        next_origin = (
            sg.origin[0] + _offset[0],
            sg.origin[1] + sg.size[1] - _offset[1] - next_size[1]
        )

        self.__expand(next_origin, next_size)
        self.set_subgrid(Subgrid(next_size, next_origin, sharex=self.get_a_subgrid(
            sharex), sharey=self.get_a_subgrid(sharey), **kwd), new_name)
        return self

    def from_right_top(self, origin_name, new_name, size: Size, offset: Size = (0, 0), sharex=None, sharey=None, **kwd) -> Subgrid:
        _offset = self.to_default_unit(offset)
        _size = self.to_default_unit(size)

        sg = self.get_subgrids([origin_name])[0]

        next_size = (
            _size[0] if _size[0] is not None else sg.get_width() - _offset[0],
            _size[1] if _size[1] is not None else sg.get_height() - _offset[1]
        )

        next_origin = (
            sg.origin[0] + sg.size[0] - _offset[0] - next_size[0],
            sg.origin[1] + _offset[1]
        )

        self.__expand(next_origin, next_size)
        self.set_subgrid(Subgrid(next_size, next_origin, sharex=self.get_a_subgrid(
            sharex), sharey=self.get_a_subgrid(sharey), **kwd), new_name)
        return self

    def from_right_bottom(self, origin_name, new_name, size: Size, offset: Size = (0, 0), sharex=None, sharey=None, **kwd) -> Subgrid:
        _offset = self.to_default_unit(offset)
        _size = self.to_default_unit(size)

        sg = self.get_subgrids([origin_name])[0]

        next_size = (
            _size[0] if _size[0] is not None else sg.get_width() - _offset[0],
            _size[1] if _size[1] is not None else sg.get_height() - _offset[1]
        )

        next_origin = (
            sg.origin[0] + sg.get_width() - _offset[0] - next_size[0],
            sg.origin[1] + sg.get_height() - _offset[1] - next_size[1]
        )

        self.__expand(next_origin, next_size)
        self.set_subgrid(Subgrid(next_size, next_origin, sharex=self.get_a_subgrid(
            sharex), sharey=self.get_a_subgrid(sharey), **kwd), new_name)
        return self

    def add_right(self, origin_name, new_name, size: Size, margin: Union[Number, Size] = 0, offset: Size = (0, 0), sharex=None, sharey=None, **kwd) -> Subgrid:
        """
        Layout a new subplot on the right side of the
            former subplot.

        Parameters
        ----------
        sg: Subgrid
            An instance of Subgrid.
            The position of the new subplot is calculated
                form the subgrid.
        size: tuple(float)
            (width, height) of plot area of the new subplot.
        margin: float, optional
            Distance between the former subplot and the new
                one.
            Default value is 0.
        offset: tuple(float), optional
            (horizontal, vertical) offset from the relative
                origin of the new subplot.
            If you want to adjust margin between 2 subplots,
                please use margin parameter.
            Default velue is (0,0)
        """
        _offset = self.to_default_unit(offset)
        _size = self.to_default_unit(size)
        _margin = self.to_default_unit(margin)

        sg = self.get_subgrids([origin_name])[0]

        d = _margin[0] if type(_margin) is tuple else _margin

        next_origin = (
            sg.origin[0] + sg.get_width() + d + _offset[0],
            sg.origin[1] + _offset[1]
        )

        next_size = (
            _size[0],
            _size[1] if _size[1] is not None else self.get_height() -
            next_origin[1]
        )

        self.__expand(next_origin, next_size)
        self.set_subgrid(Subgrid(next_size, next_origin, sharex=self.get_a_subgrid(
            sharex), sharey=self.get_a_subgrid(sharey), **kwd), new_name)
        return self

    def add_bottom(self, origin_name, new_name, size: Size, margin: Union[Number, Size] = 0, offset: Size = (0, 0), sharex=None, sharey=None, **kwd) -> Subgrid:
        _offset = self.to_default_unit(offset)
        _size = self.to_default_unit(size)
        _margin = self.to_default_unit(margin)

        sg = self.get_subgrids([origin_name])[0]

        d = _margin[1] if type(_margin) is tuple else _margin

        next_origin = (
            sg.origin[0] + _offset[0],
            sg.origin[1] + sg.get_height() + d + _offset[1]
        )

        next_size = (
            _size[0] if _size[0] is not None else self.get_width() -
            next_origin[0],
            _size[1]
        )

        self.__expand(next_origin, next_size)
        self.set_subgrid(Subgrid(next_size, next_origin, sharex=self.get_a_subgrid(
            sharex), sharey=self.get_a_subgrid(sharey), **kwd), new_name)
        return self

    def add_top(self, origin_name, new_name, size: Size, margin: Union[Number, Size] = 0, offset: Size = (0, 0), sharex=None, sharey=None, **kwd) -> Subgrid:
        _offset = self.to_default_unit(offset)
        _size = self.to_default_unit(size)
        _margin = self.to_default_unit(margin)

        sg = self.get_subgrids([origin_name])[0]

        d = _margin[1] if type(_margin) is tuple else _margin
        next_origin = (
            sg.origin[0] + _offset[0],
            sg.origin[1] - _size[1] - d - _offset[1]
        )

        next_size = (
            _size[0] if _size[0] is not None else self.get_width() -
            next_origin[0],
            _size[1]
        )

        self.__expand(next_origin, next_size)
        self.set_subgrid(Subgrid(next_size, next_origin, sharex=self.get_a_subgrid(
            sharex), sharey=self.get_a_subgrid(sharey), **kwd), new_name)
        return self

    def add_left(self, origin_name, new_name, size: Size, margin: Union[Number, Size] = 0, offset: Size = (0, 0), sharex=None, sharey=None, **kwd) -> Subgrid:
        _offset = self.to_default_unit(offset)
        _size = self.to_default_unit(size)
        _margin = self.to_default_unit(margin)

        sg = self.get_subgrids([origin_name])[0]

        d = _margin[0] if type(_margin) is tuple else _margin
        next_origin = (
            sg.origin[0] - _offset[0] - d - _size[0],
            sg.origin[1] + _offset[1]
        )

        next_size = (
            _size[0],
            _size[1] if _size[1] is not None else self.get_height() -
            next_origin[1]
        )

        self.__expand(next_origin, next_size)
        self.set_subgrid(Subgrid(next_size, next_origin, sharex=self.get_a_subgrid(
            sharex), sharey=self.get_a_subgrid(sharey), **kwd), new_name)
        return self

    def add_grid(self, sizes: List[Size], column: int = 1, margin: Union[Number, Size] = (0, 0), names=None, **kwd) -> List[Subgrid]:
        """
        Generates subgrids aligning as grid layout.
        Order of subgrid is column prefered.

        Parameters
        ----------
        sizes: List[Tuple[float]]
            List of tuples which have 2 float numbers.
            The tuple defines width and height (w, h) of
                a subplot by unit of inches.

        column: int, optional
            Number of columns in grid.
            Default value is 1.

        offset: Tuple[float], optional
            Offsets between subgrids.
            It has 2 float numbers indicating horizontal and vertical
                distances (h, v) between subgrids.
            Default value is (0, 0).

        Return
        ------
        subgrids: List[Subgrid]
            List of instances of Subgrid class.
            The length is equal to that of sizes parameter.

        Example
        -------
        # Generate 3 x 3 grid from 9 subplots whose plot area sizes are 3 x 3.

        gridder = Gridder()

        subgrids = gridder.add_grid(
            [(3,3) for i in range(9)],
            3,
            offset=(0.5, 0.5)
        )

        """

        d = margin if type(margin) is tuple else (margin, margin)

        def safe_get(l, i, default):
            return l[i] if l is not None and len(l) > i else default

        size, *rest_sizes = sizes
        self.add_origin(safe_get(names, 0, 0), size)

        for i, size in enumerate(rest_sizes):
            l = len(self)

            if len(self) % column == 0:
                self.add_bottom(
                    safe_get(names, l - column, l - column),
                    safe_get(names, i + 1, i + 1),
                    size, d, **kwd
                )
            else:
                self.add_right(
                    safe_get(names, l - 1, l - 1),
                    safe_get(names, i + 1, i + 1),
                    size, d, **kwd
                )

        return self

    def __scale(self, v: Union[Coordinate, Size], padding: dict | list) -> Union[Coordinate, Size]:
        """
        Scaling position in figure by figure size.
        Padding is took into considered.
        """
        pad: Padding = self.get_padding(padding)

        size = np.add(self.get_size(), (pad.left + pad.right, pad.top + pad.bottom)
                      )

        if 0 in size:
            raise SystemError("Size cannot be zero")

        origin = np.add(
            self.left_top, (-pad.left, -pad.top))
        # r = (v - o)/s
        return tuple(
            np.divide(np.add(v, np.multiply(origin, -1)), size)
        )

    def __relative(self, subgrid, padding: dict | list) -> Tuple[Coordinate, Coordinate]:
        """
        Return scaled position of left-top and right-bottom
            corners of a subgrid.
        """

        rel_left_top = self.__scale(subgrid.get_left_top(), padding)
        rel_right_bottom = self.__scale(subgrid.get_right_bottom(), padding)
        return (rel_left_top, rel_right_bottom)

    def axes_position(self, subgrid, padding: dict | list = {}) -> List[Number]:
        """
        Return matplotlib style position of ax.
        """
        lt, rb = self.__relative(subgrid, padding)

        # [left,bottom,width,height]
        position = [lt[0], 1 - rb[1], rb[0] - lt[0], rb[1] - lt[1]]
        return position

    def generate_axes(self, figure: Fig, padding: dict | list = {}) -> Callable[[Subgrid], Ax]:
        """
        Generate matplotlib.pyplot.axsubplot.

        Parameter
        ---------
        figure: matplotlib.pyplot.figure

        Returns
        -------
        ax: matplotlib.pyplot.axsubplot
        """
        def f(subgrid: Subgrid) -> Ax:
            ax = figure.add_axes(
                self.axes_position(subgrid, padding),
                **subgrid.get_axes_option(),
                **subgrid.get_shared_axis()
            )
            subgrid.set_ax(ax)
            return ax
        return f

    def figure_and_axes(self,
                        subgrid_names: List[str] = None,
                        padding: dict | list = {},
                        figsize: Optional[Size] = None,
                        dpi: Optional[int] = None,
                        **figure_kwargs) -> Tuple[Fig, List[Ax]]:
        """
        Generate matplotlib.pyplot.figure and its subplots of
            matplotlib.pyplot.axsubplot.

        This method also takes key word arguments same with matplotlib.pyplot.figure.

        Paraeters
        ---------
        subgrids: list[Subgrid]
            List of Subgrids generated by this instance.
        padding: dict, optional
            Dictionary to overwrite default padding size around plot areas of subplots.
            It can have keys "top", "left", "bottom", and "right.
            If padding are too small, axises may be out of image.
            Default value is empty dictionaly.
        figsize: tuple(float), optional
            Tuple with 2 float number (width, height) to overwrite figure size.
            Default value is None.
        kwargs:
            Key word arguments compatible to matplotlib.pyplot.figure.

        Return
        ------
        fig: matplotlib.figure.Figure
        axs: list[matplotlib.axes._subplots.AxesSubplot]
        """
        subgrids = self.get_subgrids(
            subgrid_names) if subgrid_names is not None else self.get_all_subgrids()

        fig = plt.figure(
            figsize=self.get_size() if figsize is None else figsize,
            dpi=self.dpi,
            **dict(self.default_figure_style, **figure_kwargs)
        )
        axs = pip(
            mapping(self.generate_axes(fig, padding)),
            list
        )(subgrids)

        return(fig, axs)

    @staticmethod
    def fontsize_to_inch(fontsize: Number, n: int, dpi: int = 72) -> Number:
        """
        Assist determin padding size when font size
            and number of characters are given.

        Parameters
        ----------
        fontsize: float
            Unit is px.
        n: float
            Number of characters.

        Return
        ------
        padding: float
            Unit of inches

        Usage
        -----
        padding = MatPos.fontsize_to_point(12, 5)

        """
        return fontsize * n / dpi
