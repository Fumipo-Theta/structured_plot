from ..kit import gen_action, get_subset
from ..type_set import DataSource, PlotAction, Selector
import matplotlib.image as mpimg


@gen_action(
    ["img_like"],
    {
        "cmap": None,
    }
)
def imshow(img_like, *arg, **kwargs)->PlotAction:
    """
    Parameters
    ----------
    df: image like data
        Such as numpy array.

    """
    img = mpimg.imread(img_like)

    def plot(ax):
        ax.imshow(img)
        return ax
    return plot
