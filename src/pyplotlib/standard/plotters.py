
from .private.line_plotter import LinePlotter as LinePlotter
from .private.rect_multi_plotter import RectMultiPlotter as RectMultiPlotter

from .private import shared_axis_plotter

#Define them like this to keep the file easier to read + plotters easy as possible to access
#LinePlotter = line_plotter.LinePlotter
DoubleAxisPlotter = shared_axis_plotter.DoubleAxisPlotter

