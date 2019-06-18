import numpy as np
import pandas as pd


def normalize(lower, upper):
    return lambda v: (v-lower)/(upper-lower)


class IGetSeriesOrLiteral:
    def __new__(cls, *arg, **kwargs):
        return super().__new__(cls)

    def __init__(self, series_selector):
        self.series_generator = series_selector

    def apply(self, df):
        pass


class ColorLiteral(IGetSeriesOrLiteral):
    def __init__(self, color_literal):
        self.series_generator = color_literal

    def apply(self, _):
        return self.series_generator


class ColorMap(IGetSeriesOrLiteral):
    def __init__(self, series_selector, extent=[None, None], cmap=None):
        self.series_generator = series_selector
        self.extent = extent
        self.cmap = cmap

    def get_extent(self, data):
        lower, upper = self.extent
        return [
            np.min(data) if lower is None else lower,
            np.max(data) if upper is None else upper
        ]

    def apply(self, df):
        target = self.series_generator(df)
        lower, upper = self.get_extent(target)
        normalizer = normalize(lower, upper)
        if type(target) in [pd.DataFrame, pd.Series]:
            return self.cmap(target.apply(normalizer))
        else:
            return self.cmap(normalizer(target))
