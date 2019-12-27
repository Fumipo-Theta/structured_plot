from ..kit import gen_action, gen_plotter, get_subset
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

    @gen_plotter
    def plot(ax):
        return ax.imshow(img)
    return plot
