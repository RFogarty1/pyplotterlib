
import itertools as it
import matplotlib.ticker
import matplotlib.pyplot as plt


import numpy as np

from ..core import plot_command as plotCommCoreHelp
from ..core.serialization import register as serializationReg


#Generic commands should work for all
@serializationReg.registerForSerialization()
class AddPlotterToOutput(plotCommCoreHelp.PlotCommand):
	""" Adds the plotter instance to the output of createPlot()

	"""
	def __init__(self):
		self._name = "add-plotter-instance-to-output"
		self._description = "Adds the plotter instance used to create a plot to the output generated"

	def execute(self, plotterInstance):
		plotterInstance._scratchSpace["outDict"]["plotter"] = plotterInstance

#These are the multi-plotter class ones

#Below ALL refer to single-plotter cases
@serializationReg.registerForSerialization()
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


@serializationReg.registerForSerialization()
class GridLinesCreate(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "create-grid-lines"
		self._description = "Creates grid lines if required" 
		self._settingsComms = [_GridLinesSetVisibilityOption(),
		                       _GridLinesSetLineStyles(),
		                       _GridLinesSetLineWidths()]

	def execute(self, plotterInstance):
		#Run all the commands to set kwarg dict
		for command in self._settingsComms:
			command.execute(plotterInstance)

		#Get kwarg dicts
		genDict = plotterInstance._scratchSpace.get("grid_line_opts", None)
		xDict = plotterInstance._scratchSpace.get("grid_line_opts_x", None)
		yDict = plotterInstance._scratchSpace.get("grid_line_opts_y", None)

		#Figure out if we need to do anything; return if not
		allDicts = [genDict, xDict, yDict]
		if all([x is None for x in allDicts]):
			return None

		#Figure out the visibility of the axis in general
		if genDict is None:
			genVis = False

		#We need to set x and y visibility to global if its not specifically set
		if xDict is not None:
			xVis = xDict.get("visible", None)
			if xVis is None:
				xDict["visible"] = genVis

		if yDict is not None:
			yVis = yDict.get("visible", None)
			if yVis is None:
				yDict["visible"] = genVis

		#Apply any options to grid lines (including turning on/off)
#		self._applyGeneralGridLineOpts(genDict)
		self._applyAxisGridLineOpts(genDict, axis="both")
		self._applyAxisGridLineOpts(xDict, axis="x")
		self._applyAxisGridLineOpts(yDict, axis="y")

#		raise ValueError("TODO: Want to set linewidth/color on GENERAL only")

	def _applyAxisGridLineOpts(self, genDict, axis="both"):
		if genDict is None:
			return None

		plt.gca().grid(**genDict, axis=axis)


@serializationReg.registerForSerialization()
class _GridLinesSetVisibilityOption(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "grid-lines-set-visibility"
		self._description = "Sets option for grid-lines visibility"
		self._optNameGen = "gridLinesShow"
		self._optNameX = "gridLinesShowX"
		self._optNameY = "gridLinesShowY"

		self._dictNameGen = "grid_line_opts"
		self._dictNameX = "grid_line_opts_x"
		self._dictNameY = "grid_line_opts_y"
		self._dictKey = "visible"

	def execute(self, plotterInstance):
		#General settings
		genVal = _getValueFromOptName(plotterInstance, self._optNameGen)
		if genVal is not None:
			_setScratchSpaceDictKey(plotterInstance, self._dictNameGen, self._dictKey, genVal)

		#x-specific settings
		xVal = _getValueFromOptName(plotterInstance, self._optNameX)
		if xVal is not None:
			_setScratchSpaceDictKey(plotterInstance, self._dictNameX, self._dictKey, xVal)

		#y-specific settings
		yVal = _getValueFromOptName(plotterInstance, self._optNameY)
		if yVal is not None:
			_setScratchSpaceDictKey(plotterInstance, self._dictNameY, self._dictKey, yVal)

@serializationReg.registerForSerialization()
class _GridLinesSetLineStyles(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "grid-lines-set-styles"
		self._description = "Sets option for grid line styles"

		self._dictNameGen = "grid_line_opts"
		self._genOptName = "gridLinesStyle"
		self._dictKey = "linestyle"

	def execute(self, plotterInstance):
		genVal = _getValueFromOptName(plotterInstance, self._genOptName)
		if genVal is not None:
			_setScratchSpaceDictKey(plotterInstance, self._dictNameGen, self._dictKey, genVal)

@serializationReg.registerForSerialization()
class _GridLinesSetLineWidths(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "grid-lines-set-widths"
		self._description = "Sets the width of grid lines"

		self._dictNameGen = "grid_line_opts"
		self._genOptName = "gridLinesWidth"
		self._dictKey = "linewidth"

	def execute(self, plotterInstance):
		genVal = _getValueFromOptName(plotterInstance, self._genOptName)
		if genVal is not None:
			_setScratchSpaceDictKey(plotterInstance, self._dictNameGen, self._dictKey, genVal)


#Will likely need to factor most out + inherit
@serializationReg.registerForSerialization()
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

@serializationReg.registerForSerialization()
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
#					plt.gca().get_yaxis().set_ticks([])
					plt.gca().tick_params(which="both", left=False, labelleft=False)
				if attrKey == "bottom":
#					plt.gca().get_xaxis().set_ticks([])
					plt.gca().tick_params(which="both", bottom=False, labelbottom=False)
				if attrKey == "right":
					plt.gca().tick_params(which="both", right=False, labelright=False)
				if attrKey == "top":
					plt.gca().tick_params(which="both", top=False, labeltop=False)

#				if attrKey == "right":

		#NOTE: Possibly some better commands here
		# hide the spines between ax and ax2
#		ax1.spines.bottom.set_visible(False)
#		ax2.spines.top.set_visible(False)
#		ax1.xaxis.tick_top()
#		ax1.tick_params(labeltop=False)  # don't put tick labels at the top
#		ax2.xaxis.tick_bottom()


@serializationReg.registerForSerialization()
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

@serializationReg.registerForSerialization()
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


@serializationReg.registerForSerialization()
class SetAxisTickAndLabelVisibilitiesEachSide(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "SetAxisTickAndLabelVisiblityEachSide"
		self._description = "Sets which sides of the plot to show/hide tick markers and labels"
		self._optName = "showTicksAndLabelsOnSides"

	def execute(self, plotterInstance):
		#
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None
		
		#
		useDict = {}
		attrs = ["bottom", "top", "left", "right"]
		for attr in attrs:
			currVal = getattr(targVal, attr)
			currLabelOpt, currTickOpt = "label" + attr, attr
			if currVal is True:
				useDict[currLabelOpt], useDict[currTickOpt] = True, True
			elif currVal is False:
				useDict[currLabelOpt], useDict[currTickOpt] = False, False
			else:
				pass #To catch None. Though will also catch other values

		plt.gca().tick_params(**useDict)
		plt.gca().tick_params(which="minor",**useDict)

@serializationReg.registerForSerialization()
class SetBarDataLabels(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "set-data-labels-for-bars"
		self._description = "Sets the data labels (to use in a legend) for a bar chart; this is different to the line plotter version since theres no safe equivalent to ax.get_lines()"
		self._optName = "dataLabels"

	def execute(self, plotterInstance):
		dataLabels = getattr(plotterInstance.opts, self._optName).value
		if dataLabels is None:
			return None

		plottedBars = plotterInstance._scratchSpace.get("barHandles", None)

		if plottedBars is None:
			return None

		if len(plottedBars) == 0:
			return None

		for barHandle, dataLabel in zip(plottedBars, dataLabels):
			if dataLabel is not None:
				barHandle.set_label(dataLabel)


@serializationReg.registerForSerialization()
class SetBarColors(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "set-colors-for-bars"
		self._description = "Sets the colors for series of bars"
		self._optName = "barColors"

	def execute(self, plotterInstance):
		colors = getattr(plotterInstance.opts, self._optName).value
		if colors is None:
			colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

		plottedBars = plotterInstance._scratchSpace.get("barHandles", None)
		if plottedBars is None:
			return None
		useColors = it.cycle(colors)

		for color,barSet in zip(useColors,plottedBars):
			_children = barSet.get_children()
			for child in _children:
				child.set_color(color)



@serializationReg.registerForSerialization()
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


@serializationReg.registerForSerialization()
class SetLegendFontSize(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "setLegendFontSize"
		self._description = "Sets the font size to use in the legend"

	def execute(self, plotterInstance):
		defFont = _getDefaultFontSizeFromPlotter(plotterInstance)
		useFont = defFont #No more specific way to overide yet
		if useFont is None:
			return None

		plotterInstance._scratchSpace["legendKwargDict"]["fontsize"] = useFont


@serializationReg.registerForSerialization()
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


@serializationReg.registerForSerialization()
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
@serializationReg.registerForSerialization()
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


@serializationReg.registerForSerialization()
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

@serializationReg.registerForSerialization()
class SetLineMarkerSizes(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "setLineMarkerSizes"
		self._description = "Sets the sizes for line markers"
		self._optName = "lineMarkerSizes"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None

		dataLines = plt.gca().get_lines()
		try:
			iter(targVal)
		except TypeError:
			useVal = it.cycle([targVal])
		else:
			useVal = it.cycle(targVal)

		for dataLine, markerSize in zip(dataLines, useVal):
			dataLine.set_markersize(markerSize)


@serializationReg.registerForSerialization()
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

@serializationReg.registerForSerialization()
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

@serializationReg.registerForSerialization()
class SetTitleStr(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "setTitleString"
		self._description = "Sets the axis title string"
		self._optName = "titleStr"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None

		defFontSize = _getDefaultFontSizeFromPlotter(plotterInstance)
		xPosVal = _getValueFromOptName(plotterInstance, "titleFractPosX")
		yPosVal = _getValueFromOptName(plotterInstance, "titleFractPosY")

		kwargDict = {"fontsize":defFontSize, "x":xPosVal, "y":yPosVal}
		kwargDict = {k:v for k,v in kwargDict.items() if v is not None}
		plt.title(targVal, **kwargDict)


@serializationReg.registerForSerialization()
class SetTickLabelFontSize(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "setTickLabelFontSize"
		self._description = "Sets the size of the font for axis tick labels"
		self._optName = "setTickLabelFontSize"

	def execute(self, plotterInstance):
		defVal = _getDefaultFontSizeFromPlotter(plotterInstance)
		if defVal is None:
			return None

		plt.gca().xaxis.set_tick_params(labelsize=defVal)
		plt.gca().yaxis.set_tick_params(labelsize=defVal)


@serializationReg.registerForSerialization()
class SetTickLabelValues(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "SetTickLabelValues"
		self._description = "Sets the values for the tick labels on x/y axes"
		self._optNameX = "tickMarkerLabelsX"
		self._optNameY = "tickMarkerLabelsY"

	def execute(self, plotterInstance):
		xLabelVals = _getValueFromOptName(plotterInstance, self._optNameX)
		yLabelVals = _getValueFromOptName(plotterInstance, self._optNameY)

		if xLabelVals is not None:
			plt.gca().set_xticklabels(xLabelVals)
			
		if yLabelVals is not None:
			plt.gca().set_yticklabels(yLabelVals)

@serializationReg.registerForSerialization()
class SetTickMarkerValues(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "setTickMarkerValues"
		self._description = "Sets the values for the (major) tick marker positions on x/y axes"
		self._optNameX = "tickMarkerValsX"
		self._optNameY = "tickMarkerValsY"

	def execute(self, plotterInstance):
		xTickVals = _getValueFromOptName(plotterInstance, self._optNameX)
		yTickVals = _getValueFromOptName(plotterInstance, self._optNameY)

		if xTickVals is not None:
			plt.gca().set_xticks(xTickVals)

		if yTickVals is not None:
			plt.gca().set_yticks(yTickVals)

@serializationReg.registerForSerialization()
class SetTickMinorMarkersOn(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "setTickMinorMarkersOn"
		self._description = "Optionally turns the minor tick markers on/off"
		self._optNameX = "showMinorTickMarkersX"
		self._optNameY = "showMinorTickMarkersY"

	def execute(self, plotterInstance):
		showMinorTicksX = _getValueFromOptName(plotterInstance, self._optNameX)
		showMinorTicksY = _getValueFromOptName(plotterInstance, self._optNameY)

		if showMinorTicksX is not None:
			if showMinorTicksX is False:
				plt.gca().xaxis.set_minor_locator( matplotlib.ticker.AutoMinorLocator(n=1) )
			elif showMinorTicksX is True:
				plt.gca().xaxis.set_minor_locator( matplotlib.ticker.AutoMinorLocator()   )

		if showMinorTicksY is not None:
			if showMinorTicksY is False:
				plt.gca().yaxis.grid(visible=False, which="minor")
			elif showMinorTicksY is True:
				plt.gca().yaxis.set_minor_locator( matplotlib.ticker.AutoMinorLocator()   )


@serializationReg.registerForSerialization()
class SetXLabelStr(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "SetXLabelStr"
		self._description = "Set the string value for the x-label" 
		self._optName = "xLabelStr"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None

		defFontSize = _getDefaultFontSizeFromPlotter(plotterInstance)
		plt.xlabel(targVal, fontsize=defFontSize)

@serializationReg.registerForSerialization()
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


@serializationReg.registerForSerialization()
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

@serializationReg.registerForSerialization()
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


@serializationReg.registerForSerialization()
class SetYLabelStr(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "SetYLabelStr"
		self._description = "Set the string value for the y-label"
		self._optName = "yLabelStr"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._optName).value
		if targVal is None:
			return None

		defFontSize = _getDefaultFontSizeFromPlotter(plotterInstance)
		plt.ylabel(targVal, fontsize=defFontSize)


@serializationReg.registerForSerialization()
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

@serializationReg.registerForSerialization()
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



#Some shared helper functions
def _getDefaultFontSizeFromPlotter(plotterInstance):
	try:
		outVal = getattr(plotterInstance.opts, "fontSizeDefault").value
	except AttributeError:
		outVal = None
	return outVal


def _getValueFromOptName(plotterInstance, optName):
	try:
		outVal = getattr(plotterInstance.opts, optName).value
	except AttributeError:
		outVal = None
	return outVal

def _setAttributeIfPresent(plotterInstance, optName, value):
	try:
		getattr(plotterInstance.opts, optName).value = value
	except AttributeError:
		pass

def _setScratchSpaceDictKey(plotterInstance, dictName, key, value):
	#
	try:
		useDict = plotterInstance._scratchSpace[dictName]
	except KeyError:
		useDict = dict()
		plotterInstance._scratchSpace[dictName] = useDict

	#
	useDict[key] = value



