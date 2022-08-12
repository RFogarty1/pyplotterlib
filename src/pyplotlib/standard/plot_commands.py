
import itertools as it
import matplotlib.pyplot as plt

import numpy as np

from ..core import plot_command as plotCommCoreHelp



#These are the multi-plotter class ones

#Below ALL refer to single-plotter cases
class CreateFigureIfNoAxHandle(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "create-figure"
		self._description = "If no ax-handle is present, create a figure"
		self._axHandleKey = "axHandle"

	def execute(self, plotterInstance):
		try:
			currAxHandle = plotterInstance._scratchSpace["axHandle"]
		except KeyError:
			self._createFigure(plotterInstance)

	def _createFigure(self, plotterInstance):
		try:
			figSize = getattr(plotterInstance.opts,"figSizeOnCreation").value
		except AttributeError:
			figSize = None

		currFigHandle = plt.figure(figsize=figSize)
		currFigHandle.add_subplot(111)
		plotterInstance._scratchSpace["axHandle"] = plt.gca()



#Will likely need to factor most out + inherit
class PlotDataAsLines(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "plot-line-data"
		self._description = "Plots available data using standard line-plot mode (matplotlibs plot)"
		self._optName = "plotData"

	def execute(self, plotterInstance):
		#Get the data; exit if none present
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None
		elif len(targVal)==0:
			return None

		#Plot the data; may want to return handles to scratch space later
		for currData in targVal:
			plt.plot( np.array(currData)[:,0], np.array(currData)[:,1] )

		return

class SetAxisBorderInvisible(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "SetAxisBorderVisibility"
		self._description = "Sets the border visibility for various axes (top/bottom/left/right)"
		self._optName = "axisBorderMakeInvisible"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		attrKeys = ["top", "bottom", "left", "right"]
		if targVal is None:
			return None

		attrVals = [getattr(targVal,attr) for attr in attrKeys]
		if all([x is False for x in attrVals]):
			return None

		for attrKey, attrVal in it.zip_longest(attrKeys, attrVals):
			if attrVal is True:
				plt.gca().spines[attrKey].set_visible(False)
				if attrKey == "left":
					plt.gca().get_yaxis().set_ticks([])
				if attrKey == "bottom":
					plt.gca().get_xaxis().set_ticks([])

		#NOTE: Possibly some better commands here
		# hide the spines between ax and ax2
#		ax1.spines.bottom.set_visible(False)
#		ax2.spines.top.set_visible(False)
#		ax1.xaxis.tick_top()
#		ax1.tick_params(labeltop=False)  # don't put tick labels at the top
#		ax2.xaxis.tick_bottom()


class SetAxisColorX(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "SetAxisColorX"
		self._description = "Sets the base color for the x-axis"
		self._optName = "axisColorX"
		self._inclSpinesOptName = "axisColorX_exclSpines"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None

		#Set options
		currAx = plt.gca()
		currAx.xaxis.label.set_color(targVal)
		currAx.tick_params(axis='x', colors=targVal)

		exclSpines = getattr(plotterInstance.opts, self._inclSpinesOptName).value
		if exclSpines is not True:
			currAx.spines["bottom"].set_color(targVal)
			currAx.spines["top"].set_color(targVal)


class SetAxisColorY(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "SetAxisColorY"
		self._description = "Sets the base color for the y-axis"
		self._optName = "axisColorY"
		self._inclSpinesOptName = "axisColorY_exclSpines"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None

		#Set options
		currAx = plt.gca()
		currAx.yaxis.label.set_color(targVal)
		currAx.tick_params(axis='y', colors=targVal)

		exclSpines = getattr(plotterInstance.opts, self._inclSpinesOptName).value
		if exclSpines is not True:
			currAx.spines["left"].set_color(targVal)
			currAx.spines["right"].set_color(targVal)




class SetDataLabels(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "SetDataLabels"
		self._description = "Sets the data labels for lines currently plotted; this is needed to show a legend"
		self._optName = "dataLabels"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None

		plottedLineHandles = plt.gca().get_lines()
		for lineHandle, dataLabel in zip(plottedLineHandles, targVal):
			if dataLabel is not None:
				lineHandle.set_label(dataLabel)


class SetLegendNumberColumns(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "setLegendNumbColumns"
		self._description = "Sets the number of columns to use in the legend"
		self._optName = "legendNumbCols"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None

		plotterInstance._scratchSpace["legendKwargDict"]["ncol"] = targVal


class SetLegendLocStr(plotCommCoreHelp.PlotCommand):
	
	def __init__(self):
		self._name = "setLegendLocStr"
		self._description = "Sets the 'loc' option for matplotlibs legend() function; as far as i understand, this either tells mpl where to draw the legend or where to START drawing from"
		self._optName = "legendLocStr"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None

		#We REALLY want to avoid setting to something that isnt a string (such as the loc tuple)
		#or things will get confusing when setting fractional position
		assert isinstance(targVal, str)
		plotterInstance._scratchSpace["legendKwargDict"]["loc"] = targVal


#Note: This should generally be called AFTER SetLegendLocStr
class SetLegendFractPosStart(plotCommCoreHelp.PlotCommand):
	
	def __init__(self):
		self._name = "setLegendFractPosStart"
		self._description = "Sets either the 'loc' or 'bbox_to_anchor' values in mpl. Regardless, this tells it where to start drawing the legend"
		self._optName = "legendFractPosStart"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None

		try:
			locStr = plotterInstance._scratchSpace["legendKwargDict"]["loc"] = targVal
		except KeyError:
			plotterInstance._scratchSpace["legendKwargDict"]["loc"] = targVal
		else:
			plotterInstance._scratchSpace["legendKwargDict"]["bbox_to_anchor"] = targVal


class SetLineColors(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "setLineColors"
		self._description = "Sets the line colors for lines currently plotted"
		self._optName = "lineColors"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None

		dataLines = plt.gca().get_lines()
		colors = it.cycle(targVal)
		for dataLine, color in zip(dataLines, colors):
			dataLine.set_color(color)

class SetLineMarkerStyles(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "setLineMarkerStyles"
		self._description = "Sets the line markers for lines currently plotted"
		self._optName = "lineMarkerStyles"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None

		dataLines = plt.gca().get_lines()
		markerStyles = it.cycle(targVal)
		for dataLine, markerStyle in zip(dataLines, markerStyles):
			dataLine.set_marker(markerStyle)

class SetLineStyles(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "setLineStyles"
		self._description = "Sets the line styles for lines currently plotted"
		self._optName = "lineStyles"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None

		dataLines = plt.gca().get_lines()
		lineStyles = it.cycle(targVal)
		for dataLine, lineStyle in zip(dataLines, lineStyles):
			dataLine.set_linestyle(lineStyle)

class SetXLabelStr(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "SetXLabelStr"
		self._description = "Set the string value for the x-label" 
		self._optName = "xLabelStr"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None
		plt.xlabel(targVal)

class SetXLabelFractPos(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "SetXLabelFractPos"
		self._description = "Set the fractional position for the x-label"
		self._optName = "xLabelFractPos"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None
		plt.gca().xaxis.set_label_coords(targVal[0], targVal[1])


class SetXLimit(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "SetXLimit"
		self._description = "Set the x-axis limits"
		self._optName = "xLimit"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None
		plt.xlim(targVal)

class SetYLimit(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "SetYLimit"
		self._description = "Set the y-axis limits"
		self._optName = "yLimit"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None
		plt.ylim(targVal)


class SetYLabelStr(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "SetYLabelStr"
		self._description = "Set the string value for the y-label"
		self._optName = "yLabelStr"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None
		plt.ylabel(targVal)

class SetYLabelFractPos(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "SetYLabelFractPos"
		self._description = "Set the fractional position for the y-label"
		self._optName = "yLabelFractPos"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None
		plt.gca().yaxis.set_label_coords(targVal[0], targVal[1])


class TurnLegendOnIfRequested(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "TurnLegendOnIfRequested"
		self._description = "Turn the legend on if requested"
		self._optName = "showLegend"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None

		legendKwargDict = plotterInstance._scratchSpace["legendKwargDict"]

		if targVal is True:
			plt.legend(**legendKwargDict)



