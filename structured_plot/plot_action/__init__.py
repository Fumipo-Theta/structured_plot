"""
This module provides wrapper functions for plot with matplotlib.

By using with other modules in structured_plot, you can separate actions of plot
    from data and layouting.

Functions
---------
set_tick_params
set_labels
set_grid
set_xlim
set_ylim
line
scatter
vlines
hlines
box
factor_box
factor_violin
velocity
band
text
"""
from matplotlib.pyplot import cm as colormap


from .artist_options import line2d_option

from .axes_style import set_cycler
from .axes_style import set_xlim, set_ylim, set_zlim
from .axes_style import set_grid
from .axes_style import set_tick_parameters
from .axes_style import axis_scale
from .axes_style import set_label, set_xlabel, set_ylabel, set_zlabel
from .axes_style import twinx
from .band import hband, vband, xband, yband
from .bar import bar, factor_bar, group_bar, rose
from .box import box, factor_box
from .contour import contour, contourf
# from .cycler import *
from .errorbar import errorbar
from .fill import fill, fill_between
from .hist import hist
from .imshow import imshow
from .line import line
# from .mapping import *
from .multiple import multiple, m
from .plot import plot
from .scatter import scatter
from .text import text
from .velocity import velocity
from .vhlines import vlines, hlines
from .violin import violin, factor_violin
