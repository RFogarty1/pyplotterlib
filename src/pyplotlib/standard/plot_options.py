
import numpy as np

from ..core import plot_options as plotOptCore
from ..core.serialization import register as serializationReg


@serializationReg.registerForSerialization()
class DataLabels(plotOptCore.StringIterPlotOption):
	""" Set the data labels for the plot. Values should be a list of string, with None for any data you want left with the default label. e.g. ["seriesA", None, "seriesC"] should mean only 1st and 3rd appear in the legend

	"""
	def __init__(self, name=None, value=None):
		self.name = "dataLabels" if name is None else name
		self.value = value


@serializationReg.registerForSerialization()
class LegendOn(plotOptCore.BooleanPlotOption):
	""" Option for whether to show a legend or not. Values are True (create legend) or False (dont create)

	"""
	def __init__(self, name=None, value=None):
		self.name = "showLegend" if name is None else name
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
class XLabelStr(plotOptCore.StringPlotOption):
	""" Option for the value for the x-axis label; Any string should be fine

	"""
	def __init__(self, name=None, value=None):
		self.name = "xLabelStr" if name is None else name
		self.value = value

@serializationReg.registerForSerialization()
class YLabelStr(plotOptCore.StringPlotOption):
	""" Option for the value of the y-axis label; Any string should be fine

	"""
	def __init__(self, name=None, value=None):
		self.name = "yLabelStr" if name is None else name
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

