from typing import TypeVar
from iter_helper import DuplicateLast as Duplicated

T = TypeVar("T")


def wrap_by_duplicate(a) -> Duplicated:
    """
    Wrap not tuple parameter by tuple.
    """
    return a if type(a) is Duplicated else Duplicated(a)


def get_from_duplicated(it: Duplicated[T], i: int, default=None) -> T:
    """
    Take ith item in Duplicated.
    If length of Duplicated is 0, default value is used.
    """
    if len(it) == 0:
        return default
    return it[i]
