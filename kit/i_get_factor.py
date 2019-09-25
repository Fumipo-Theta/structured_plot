import pandas as pd
from typing import Callable, Optional, Tuple, Union


def Iget_factor(
    df: pd.DataFrame,
    f: Union[str, Callable[[pd.DataFrame], pd.Series]],
    factor: Optional[Union[list, Callable[[
        pd.DataFrame], Tuple[pd.Series, list, list]]]]
)->Tuple[pd.Series, list, list]:
    d = f(df) if callable(f) else df[f]
    if type(factor) is list:
        return (d, factor, list(range(len(factor))))
    elif callable(factor):
        return factor(d)
    else:
        cat = d.astype('category').cat.categories
        return (d, cat, list(range(len(cat))))
