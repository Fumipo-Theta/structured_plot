"""
This module provides wrapper functions for plot with matplotlib.

By using with other modules in "matdat" and "matpos", you can separate actions of plot
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

from .action import *
from .axes_style import *
from .band import hband, vband, xband, yband
from .bar import bar, factor_bar, rose
from .box import box, factor_box
from .contour import contour, contourf
from .cycler import *
from .dummy_data import DummyData, DummyLoader
from .errorbar import errorbar
from .fill import fill, fill_between
from .hist import hist
from .imshow import *
from .line import line, line3d
from .mapping import *
from .multiple import multiple, m
from .scatter import scatter, scatter3d
from .text import text
from .velocity import velocity
from .vhlines import vlines, hlines
from .violin import violin, factor_violin
