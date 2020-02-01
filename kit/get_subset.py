import pandas as pd
import numpy as np
from typing import Callable
from ..dummy_data import DummyData
from ..type_set import DataSource, Selector


def iterable(i):
    return hasattr(i, "__iter__")


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
            elif callable(k):
                return k(df)
            elif iterable(k):
                return k
            else:
                # int, float, np.int, np.float
                return k

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
                return k

        elif type(df) is DummyData:
            return k

        else:
            # print(df)
            raise TypeError("df must be pandas.DataFrame or pandas.Series.")
    return f
