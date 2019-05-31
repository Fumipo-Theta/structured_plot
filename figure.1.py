# %%
from func_helper import pip, identity
from i_subplot import ISubplot
from concatable import Concatable
from layout import Matpos

# %%


class Figure:
    def __init__(self):
        self._subplots = []
        self._subplot_names = []

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
        return list(map(
            lambda iv: iv[0] if iv[1] is None else iv[1],
            enumerate(self.subplot_names)
        ))

    def add_subplot(self, *subplots, names=[]):
        """
        if any(map(lambda s: not isinstance(s, ISubplot), subplots)):
            raise TypeError("subplot must inherit ISubplot.")
        """

        _names = names if type(names) in [list, tuple] else [names]

        for i, s in enumerate(subplots):
            self.subplots.append(s)
            self.subplot_names.append(
                _names[i]
                if len(_names) > i
                else None
            )
        return self

    def show(self,
             *arg,
             size=None,
             **kwargs
             ):
        if len(arg) > 0:
            if type(arg[0]) is Matpos:
                matpos = arg[0]
                subgrids = arg[1]
                return self._show_on_layout(matpos, subgrids, **kwargs)
            elif type(arg[0]) is FigureSizing:
                figure_sizing = arg[0]
                return self._show_on_grid(
                    [figure_sizing.get_figsize()
                     for i in range(len(self))],
                    margin=figure_sizing.get_margin(),
                    padding=figure_sizing.get_padding(),
                    **kwargs
                )
            elif type(arg[0]) is dict:
                return self.show(**arg[0], **kwargs)
            else:
                raise SystemError(
                    "Type of positional arguments must be Matpos or dict. Or use keyword arguments.")

        else:
            if type(size) is tuple:
                return self._show_on_grid(
                    [size for i in range(len(self))],
                    **kwargs
                )
            elif type(size) is list:
                return self._show_on_grid(size, **kwargs)
            else:
                raise TypeError(
                    "The first arguments must be MatPos, Tuple, or List")

    def _show_on_grid(self,
                      sizes,
                      column=1,
                      margin=(1, 0.5),
                      padding={},
                      test=False,
                      unit="inches",
                      dpi=72,
                      **kwargs):

        matpos = Matpos(unit=unit, dpi=dpi)
        sgs = matpos.add_grid(sizes, column, margin)

        return self._show_on_layout(matpos, sgs, padding, test, dpi=dpi, **kwargs)

    def _show_on_layout(self,
                        matpos,
                        subgrids,
                        padding={},
                        test=False,
                        **kwargs):
        for sg, subplot in zip(subgrids, self.subplots):
            sg.set_axes_option(**subplot.get_axes_spec())

        fig, empty_axes = matpos.figure_and_axes(
            subgrids, padding=padding, **kwargs
        )

        while len(self.subplots) < len(empty_axes):
            self.add_subplot(Subplot.create_empty_space())

        axes = pip(
            Figure.__applyForEach(test),
            # list
        )(zip(empty_axes, self.subplots))

        return (fig, dict(zip(self.get_subplot_names(), axes)))

    @staticmethod
    def __applyForEach(test=False):
        """
        [(pyplot.axsubplot, Subplot)] -> [pyplot.axsubplot]
        """
        def helper(t):
            ax = t[0]
            subplot = t[1]
            return subplot.plot(ax, test)

        def f(axesAndSubplots):
            return map(
                helper,
                axesAndSubplots
            )
        return f
