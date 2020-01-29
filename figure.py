# %%
from typing import Callable, Iterable, List, Dict, Tuple, Union

from func_helper import pip, identity
from .i_subplot import ISubplot
from .layout import Layout
from .figure_sizing import FigureSizing
from .subgrid import Subgrid
from .subplot import Subplot
from functools import reduce
from .type_set import Ax, Artists, Fig
# %%


def is_unique(it):
    return len(it) is len(set(it))


def iterable(i):
    return hasattr(i, "__iter__")


class Figure:
    def __init__(self):
        self._subplots = []
        self._subplot_names = []
        self.create_empty_subplot = Subplot.create_empty_space

    def __new__(cls, *arg, **kwargs):
        return super().__new__(cls)

    def __len__(self):
        return len(self.subplots)

    def __add__(self, figure):
        return Figure().add_subplot(
            *self.subplots, *figure.subplots,
            names=[*self.subplot_names, *figure.subplot_names]
        )

    @property
    def subplots(self):
        return self._subplots

    @subplots.getter
    def subplots(self):
        return self._subplots

    @property
    def subplot_names(self):
        return self._subplot_names

    @subplot_names.getter
    def subplot_names(self):
        return self._subplot_names

    def get_subplot_names(self):
        """
        Return computed names of subplots.

        If a subplot has name (not None):
            it name is the defined string
        else:
            it name is the index number

        Example
        -------
        Fgure().add_subplot(
            subplot_0
        ) \
        + Figure().add_subplot(
            subplot_1, subplot_2,
            names=["a","b"]
        )\
        + Figure().add_subplot(
            subplot_3
        )

        in the case, subplot_names is [None, "a", "b", None].
        In this time, this method returns [0, "a", "b", 3] as names of subplots.

        """
        return list(map(
            lambda iv: iv[0] if iv[1] is None else iv[1],
            enumerate(self.subplot_names)
        ))

    def get_subplots(self, names):
        subplots = []
        for name in names:
            if name in self.get_subplot_names():
                index = self.get_subplot_names().index(name)
                subplots.append(
                    self.subplots[index]
                )
            else:
                subplots.append(self.create_empty_subplot())
        return subplots

    def get_all_subplots(self):
        return self.subplots

    def add_named_subplot(self, *named_subplots):
        """
        Parameter
        ---------
        named_subplots: Tuple[any, ISubplot]
        """
        for name, subplot in named_subplots:
            self.subplots.append(subplot)
            self.subplot_names.append(name)

        if not is_unique(self.get_subplot_names()):
            raise Exception("name of subplots is duplicated !")
        return self

    def add_subplot(self, *subplots, names=None):
        """
        Register Isubplot instances.
        """
        if any(map(lambda s: not isinstance(s, ISubplot), subplots)):
            raise TypeError("subplot must inherit ISubplot.")

        if names is None:
            self.add_named_subplot(*zip(
                [None for _ in subplots],
                subplots
            ))
            return self

        if iterable(names):
            if len(subplots) is not len(names):
                raise Exception("number of subplots and names must be same.")
            self.add_named_subplot(*zip(names, subplots))
            return self
        else:
            raise TypeError("names must be iterable.")

    def show(self,
             *arg,
             size=None,
             order=None,
             **kwargs
             ):
        if len(arg) > 0:
            if type(arg[0]) is Layout:
                layout = arg[0]
                return self._show_on_layout(layout, order, **kwargs)
            elif type(arg[0]) is FigureSizing:
                figure_sizing = arg[0]
                return self._show_on_grid(
                    [figure_sizing.get_figsize()
                     for i in range(len(self))],
                    margin=figure_sizing.get_margin(),
                    padding=figure_sizing.get_padding(),
                    order=order,
                    **kwargs
                )
            elif type(arg[0]) is dict:
                return self.show(**arg[0], **kwargs)
            else:
                raise SystemError(
                    "Type of positional arguments must be Layout or dict. Or use keyword arguments.")

        else:
            if type(size) is tuple:
                return self._show_on_grid(
                    [size for i in range(len(self))],
                    order=order,
                    **kwargs
                )
            elif type(size) is list:
                return self._show_on_grid(size, order=order, **kwargs)
            else:
                raise TypeError(
                    "The first arguments must be Layout, Tuple, or List")

    def _show_on_grid(self,
                      sizes,
                      column=1,
                      margin=(1, 0.5),
                      padding={},
                      order=None,
                      unit="inches",
                      dpi=72,
                      **kwargs):

        layout = Layout(unit=unit, dpi=dpi)\
            .add_grid(sizes, column, margin, names=order)

        return self._show_on_layout(layout, order, padding, **kwargs)

    def _show_on_layout(self,
                        layout,
                        order=None,
                        padding={},
                        test=False,
                        verbose=False,
                        **kwargs):
        """

        """
        if verbose:
            print(layout)
            print(self.get_subplot_names())
        # Transfer axes generating option from ISubplot to Subgrid

        for sg, subplot in zip(
            layout.get_subgrids(
                order) if order is not None else layout.get_all_subgrids(),
            self.get_subplots(
                order if order is not None else layout.get_subgrids_order())
        ):
            sg.set_axes_option(**subplot.get_axes_spec())

        # Generate axes in order by order option
        fig, empty_axes = layout.figure_and_axes(
            order, padding=padding, **kwargs
        )

        # Padding empty axes by empty space
        # while len(self.subplots) < len(empty_axes):
        #    self.add_subplot(self.create_empty_subplot())

        axes_and_artists: List[Union[Tuple[Ax, Artists], Tuple[Tuple[Ax, Ax], Tuple[Artists, Artists]]]] = pip(
            Figure.__applyForEach(test),
            list
        )(zip(
            empty_axes,
            self.get_subplots(
                order if order is not None else layout.get_subgrids_order())
        ))

        return (fig, dict(zip(
                order if order is not None else layout.get_subgrids_order(),
                [axes_artists[0] for axes_artists in axes_and_artists]
                )))

    @staticmethod
    def __applyForEach(test=False) -> Callable[[Iterable[Tuple[Ax, ISubplot]]], Iterable[Union[Tuple[Ax, Artists], Tuple[Tuple[Ax, Ax], Tuple[Artists, Artists]]]]]:
        """
        [(pyplot.axsubplot, Subplot)] -> [pyplot.axsubplot]
        """
        def helper(t: Tuple[Ax, ISubplot]) -> Union[Tuple[Ax, Artists], Tuple[Tuple[Ax, Ax], Tuple[Artists, Artists]]]:
            ax = t[0]
            subplot = t[1]
            return subplot.plot(ax, test)

        def f(axesAndSubplots):
            return map(
                helper,
                axesAndSubplots
            )
        return f
