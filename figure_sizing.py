import func_helper.func_helper.dictionary as d

_default_style = {
    "figure_style": {
        "figsize": None,
        "padding": {
            "top": 0.5,
            "left": 1,
            "bottom": 1,
            "right": 0.5
        }
    },
    "axes_style": {
        "margin": (1, 0.5)
    }
}


class FigureSizing:
    @staticmethod
    def create():
        style_generator = FigureSizing()
        return style_generator

    def __init__(self):
        self.figure_size = d.get(
            _default_style, "figure_style.figsize")
        self.figure_padding = d.get(
            _default_style, "figure_style.padding")

        self.axes_margin = d.get(_default_style, "axes_style.margin")
        None

    def set_figure_style(self, **kwargs):
        self.figure_size = kwargs.get("figsize", self.figure_size)
        self.figure_padding = kwargs.get("padding", self.figure_padding)
        return self

    def get_figsize(self):
        return self.figure_size

    def get_padding(self):
        return self.figure_padding

    def set_axes_style(self, **kwargs):
        self.axes_margin = kwargs.get("margin", self.axes_margin)
        return self

    def get_margin(self):
        return self.axes_margin
