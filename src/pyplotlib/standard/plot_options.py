
import types

import numpy as np

from ..core import plot_options as plotOptCore
from ..core.serialization import register as serializationReg


@serializationReg.registerForSerialization()
class AxisBorderMakeInvisible(plotOptCore.BoolNamespaceOption):
	""" Namespace controlling visibility of axis borders. Access values with .value.top, .value.bottom, .value.left, .value.right.

	Setting to True should hide that border, including any tick markers. This is useful for split axis plotters.

	Note: We assume x-ticks are "bottom" and y-ticks are "left". If not, other visiblity options may be more appropriate
	Note: Setting values to False does NOTHING (i.e. it wont override any other settings that make borders invisible)

	"""
	def __init__(self, name=None, value=None):
		self.name = "axisBorderMakeInvisible" if name is None else name
		self.value = types.SimpleNamespace(top=False, bottom=False, left=False, right=False) if value is None else value

@serializationReg.registerForSerialization()
class AxisColorX(plotOptCore.StringPlotOption):
	""" String representing the base color for the x-axis. Valid values include keywords like 'red' or hex rgb codes if prepended with a # (e.g. #d010f0)

	Note: This value may be overwritten by more specific options

	"""
	def __init__(self, name=None, value=None):
		self.name = "axisColorX" if name is None else name
		self.value = value

@serializationReg.registerForSerialization()
class AxisColorX_exclSpines(plotOptCore.BooleanPlotOption):
	""" Option for whether to include the spines when setting color for x-axis. Can be useful to exclude them when making shared axis plots

	"""
	def __init__(self, name=None, value=None):
		self.name = "axisColorX_exclSpines"
		self.value = value

@serializationReg.registerForSerialization()
class AxisColorY(plotOptCore.StringPlotOption):
	""" String representing the base color of the y-axis. Valid values include keywords like 'red' or hex rgb codes if prepended with a #  (e.g. #d010f0)

	Note: This value may be overwritten by more specific options

	"""
	def __init__(self, name=None, value=None):
		self.name = "axisColorY" if name is None else name
		self.value = value

@serializationReg.registerForSerialization()
class AxisColorY_exclSpines(plotOptCore.BooleanPlotOption):
	""" Option for whether to include the spines when setting color for y-axis. Can be useful to exclude them when making shared axis plots
	"""
	def __init__(self, name=None, value=None):
		self.name = "axisColorY_exclSpines"
		self.value = value


@serializationReg.registerForSerialization()
class DataLabels(plotOptCore.StringIterPlotOption):
	""" Set the data labels for the plot. Values should be a list of string, with None for any data you want left with the default label. e.g. ["seriesA", None, "seriesC"] should mean only 1st and 3rd appear in the legend

	"""
	def __init__(self, name=None, value=None):
		self.name = "dataLabels" if name is None else name
		self.value = value

@serializationReg.registerForSerialization()
class FontSizeDefault(plotOptCore.IntPlotOption):
	""" The default font size to use for a figure. None will fall back on matplotlib value.

	Valid values are integers (e.g. 10-ish is standard)

	"""
	def __init__(self, name=None, value=None):
		self.name = "fontSizeDefault" if name is None else name
		self.value = value

@serializationReg.registerForSerialization()
class LegendLocStr(plotOptCore.StringPlotOption):
	""" String representing location of legend, e.g. 'upper right' or 'best'. Same as used in matplotlib.

	If legendFractPosStart is also set then this string determines which part of the legend matches that fractional position (i.e. where we start drawing from). 

	"""
	def __init__(self, name=None, value=None):
		self.name = "legendLocStr" if name is None else name
		self.value = value

@serializationReg.registerForSerialization()
class LegendFractPosStart(plotOptCore.FloatIterPlotOption):
	""" len-2 iter with the fractional x/y ([x,y]) position to start drawing the legend.[values should generally be between 0 and 1]

	 Should default to lower-left corner as being the point it draws from, though this can be overwritten by LegendLocStr and currently is relying on matplotlib defaults (meaning it may change in future versions)

	Also setting LegendLocStr is recommended in order to control which corner [x,y] positions refer to

	"""
	def __init__(self, name=None, value=None):
		self.name = "legendFractPosStart" if name is None else name
		self.value = value



@serializationReg.registerForSerialization()
class LegendOn(plotOptCore.BooleanPlotOption):
	""" Option for whether to show a legend or not. Values are True (create legend) or False (dont create)

	"""
	def __init__(self, name=None, value=None):
		self.name = "showLegend" if name is None else name
		self.value = value

@serializationReg.registerForSerialization()
class LegendNumbCols(plotOptCore.IntPlotOption):
	""" Number of columns the legend should have

	"""
	def __init__(self, name=None, value=None):
		self.name = "legendNumbCols"
		self.value = value

@serializationReg.registerForSerialization()
class LineColors(plotOptCore.StringIterPlotOption):
	""" The line colors to use. Allowed strings are the same as in matplotlib, meaning special color names or hex rgb codes are both fine. For Example ['red','green','orange'] is a valid value

	Note: The number of colors doesnt have to match the number of data series. If you provide too few colors, they will simply cycle. For example if you set ['red','green'] then plotted data would be [red, green, red, green,.... etc]

	"""
	def __init__(self, name=None, value=None):
		self.name = "lineColors"
		self.value = value

@serializationReg.registerForSerialization()
class LineMarkerSizes(plotOptCore.FloatIterOrSingleFloatOption):
	""" The sizes of line marker sizes. Valid values are either a single number or a list of numbers.

	e.g. 20 will set all markers to a size of 20; [10,15] will set the first data series size to 10, and the second to 15

	"""
	def __init__(self, name=None, value=None):
		self.name = "lineMarkerSizes"
		self.value = value


@serializationReg.registerForSerialization()
class LineMarkerStyles(plotOptCore.StringIterPlotOption):
	""" The line markers to use. Valid values are currently shown at "https://matplotlib.org/stable/api/markers_api.html". E.g. ['x', 'o', '^']

	Note: The number of markers doesnt have to match the number of data series. If you provide too few marker styles they will simply cycle

	"""
	def __init__(self, name=None, value=None):
		self.name = "lineMarkerStyles"
		self.value = value

@serializationReg.registerForSerialization()
class LineStyles(plotOptCore.StringIterPlotOption):
	""" The line styles to use. Valid values are the strings currently shown at "https://matplotlib.org/stable/api/_as_gen/matplotlib.lines.Line2D.html#matplotlib.lines.Line2D.set_linestyle"

	Note: The number of styles doesnt have to match the number of data series. If you provide too few, line styles they will simply cycle

	"""
	def __init__(self, name=None, value=None):
		self.name = "lineStyles"
		self.value = value

@serializationReg.registerForSerialization()
class PlotterIter(plotOptCore.ObjectIterPlotOption):
	""" Iter of individual plotter objects. Used in cases where a graph is made of multiple individual "plots" (e.g. when using axis-splitting or multiple-independent x/y axes")

	"""
	def __init__(self, name=None, value=None):
		self.name = "plotters" if name is None else name
		self.value = value


@serializationReg.registerForSerialization()
class PlotData2D(plotOptCore.NumpyIterPlotOption):
	""" Option for the plot data. Expected formats are:

	a) None, if no plotData is available
	b) An iterable of nx2 numpy arrays, with columns being [x,y]
	c) An iterable that transforms to b) when np.array() is called on each element

	"""
	def __init__(self, name=None, value=None):
		self.name = "plotData" if name is None else name
		self.value = value

@serializationReg.registerForSerialization()
class PlotData1D(plotOptCore.NumpyIterPlotOption):
	""" Option for 1-dimensional plot data. Expected formats are:

	a) None, if no plotData is available
	b) An iterable of 1-D numpy arrays
	c) An iterable that transforms to b) when np.array() is called on each element (e.g. an iter of float-lists)

	e.g. [ [0,1,2], [3,2,1] ] may be input for two data series, each with three data points

	"""
	def __init__(self, name=None, value=None):
		self.name = "plotData1D" if name is None else name
		self.value = value

@serializationReg.registerForSerialization()
class SetFigsizeOnCreation(plotOptCore.FloatIterPlotOption):
	""" Set the size of the figure upon figure creation. Format is [width,height] where values are likely in inches.

	Note:
		i) The size of the displayed figure in a jupyter notebook will depend on this size AND the dpi value
		ii) This option will have no effect if a figure is not created by a plotter object; this will be common when creating multi plots (where an axis is passed to each individual axis-plotter)

	"""
	def __init__(self, name=None, value=None):
		self.name = "figSizeOnCreation"
		self.value = value

@serializationReg.registerForSerialization()
class ShowTicksAndLabelsOnSides(plotOptCore.BoolNamespaceOption):
	""" Controls which sides of the plot relevant ticks and labels are displayed. The value is a namespace with "top", "bottom", "left", "right" as the keys and True/False as valid values.

	Setting a key to True will make the tick-markers and labels appear on that side, False will make neither appear.

	Note: More specific options SHOULD overwrite this one (e.g. ShowTicksOnSides)

	"""
	def __init__(self, name=None, value=None):
		self.name = "showTicksAndLabelsOnSides"
		self.value = value


@serializationReg.registerForSerialization()
class ShowTicksOnSides(plotOptCore.BoolNamespaceOption):
	""" Controls which sides of the plot relevant tick markers are displayed. The value is a namespace with "top", "bottom", "left", "right" as the keys and True/False as valid values.

	Setting a key to True will make the tick-markers appear on that side, False will make them not appear. Setting a key to None will fallback on matplotlibs default behavior

	"""
	def __init__(self, name=None, value=None):
		self.name = "showTicksOnSides"
		self.value = value

@serializationReg.registerForSerialization()
class ShowTickLabelsOnSides(plotOptCore.BoolNamespaceOption):
	""" Controls which sides of the plot relevant tick labels are displayed. The value is a namespace with "top", "bottom", "left", "right" as the keys and True/False as valid values.

	Setting a key to True will make the tick-labels appear on that side, False will make them not appear.

	"""
	def __init__(self, name=None, value=None):
		self.name = "showTickLabelsOnSides"
		self.value = value




@serializationReg.registerForSerialization()
class TitleStr(plotOptCore.StringPlotOption):
	""" The string to use for the plot title (None means dont have a title)

	"""
	def __init__(self, name=None, value=None):
		self.name = "titleStr"
		self.value = value


@serializationReg.registerForSerialization()
class XLabelStr(plotOptCore.StringPlotOption):
	""" Option for the value for the x-axis label; Any string should be fine

	"""
	def __init__(self, name=None, value=None):
		self.name = "xLabelStr" if name is None else name
		self.value = value

@serializationReg.registerForSerialization()
class XLabelFractPos(plotOptCore.FloatIterPlotOption):
	""" Option to set the x/y fraction positions of the x-label. Useful for split-axes plotters in particular. Needs to be a len-2 float iter [xPos, yPos], e.g. [0.5, -0.1] will put it in approximately the standard place

	"""
	def __init__(self, name=None, value=None):
		self.name = "xLabelFractPos" if name is None else name
		self.value = value

@serializationReg.registerForSerialization()
class YLabelStr(plotOptCore.StringPlotOption):
	""" Option for the value of the y-axis label; Any string should be fine

	"""
	def __init__(self, name=None, value=None):
		self.name = "yLabelStr" if name is None else name
		self.value = value

@serializationReg.registerForSerialization()
class YLabelFractPos(plotOptCore.FloatIterPlotOption):
	"""The summary line for a class docstring should fit on one line.


	"""
	def __init__(self, name=None, value=None):
		self.name = "yLabelFractPos" if name is None else name
		self.value = value

@serializationReg.registerForSerialization()
class XLimit(plotOptCore.FloatIterPlotOption):
	""" Option for the value of the x-limit (e.g. [0,5.5])

	"""
	def __init__(self, name=None, value=None):
		self.name = "xLimit" if name is None else name
		self.value = value

@serializationReg.registerForSerialization()
class YLimit(plotOptCore.FloatIterPlotOption):
	""" Option for the value of the y-limit (e.g. [0,7.5])

	"""
	def __init__(self, name=None, value=None):
		self.name = "yLimit" if name is None else name
		self.value = value

