import matplotlib
from typing import Optional


def Icoordinate_transform(ax, xcoordinate: Optional[str], ycoordinate: Optional[str]):
    """
    Select coordinate transform method for x and y axis.

    """
    return matplotlib.transforms.blended_transform_factory(
        ax.transAxes if xcoordinate is "axes" else ax.transData,
        ax.transAxes if ycoordinate is "axes" else ax.transData
    )
