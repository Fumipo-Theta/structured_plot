import numpy as np


class Subgrid:
    def __init__(self, size, origin, sharex=None, sharey=None, **kwd):
        if size[0] < 0 or size[1] < 0:
            raise SystemError("size must be positive")
        self.size = size
        self.origin = origin
        self.set_shared_axis(sharex, sharey)
        self.axes_kwargs = kwd

    def get_left_top(self):
        return self.origin

    def get_right_bottom(self):
        return tuple(np.add(self.origin, self.size))

    def get_width(self):
        return self.size[0]

    def get_height(self):
        return self.size[1]

    def get_size(self):
        return self.size

    def set_ax(self, ax):
        self.ax = ax

    def get_ax(self):
        return self.ax

    def set_shared_axis(self, sharex=None, sharey=None):
        self.sharex = sharex
        self.sharey = sharey

    def get_shared_axis(self):
        return {
            "sharex": self.sharex.get_ax() if type(self.sharex) is Subgrid else None,
            "sharey": self.sharey.get_ax() if type(self.sharey) is Subgrid else None
        }

    def set_axes_kwargs(self, **kwd):
        self.axes_kwargs = kwd

    def get_axes_kwargs(self):
        return self.axes_kwargs


class EmptyGrid(Subgrid):
    def __init__(self, size, origin):
        super(size, origin)
