

import copy
import itertools as it
import matplotlib.pyplot as plt

import numpy as np

from . import shared

from .. import plot_options as plotOptStdHelp
from .. import plot_commands as plotCmdStdHelp


from ...core import plotters as plotterCoreHelp
from ...core import plot_options as plotOptCoreHelp

from ...core.serialization import register as serializationReg
from ...core import plot_command as plotCmdCoreHelp
from ...core import plot_options as plotOptCoreHelp


@serializationReg.registerForSerialization()
class BoxPlotter(shared.FromJsonMixin, shared.FromPlotterMixin, plotterCoreHelp.SingleGraphPlotter):
	""" Plotter for creating box-plots - also known as a box-and-whisker plot

	"""
	def __init__(self, **kwargs):
		""" Initializer
		
		Args:
			kwargs: Keys are strs in "BoxPlotter().optionNames"
				 
		"""
		self._createCommands()
		self._createOptions()
		self._scratchSpace = {"boxPlotKwargsGlobal":{}, "boxPlotKwargsEach":list()}
		self.setOptionVals(kwargs)

	def _createCommands(self):
		self._commands = _createCommandsList()

	def _createOptions(self):
		_optionsList = _createOptionsList()
		self._options = plotOptCoreHelp.OptionsCollection(options=_optionsList)




def _createCommandsList():
	outList = [
	plotCmdStdHelp.AddPlotterToOutput(),
	plotCmdStdHelp.CreateFigureIfNoAxHandle(),
	AddDataToScratch(),
	AddBoxColorToScratch(),
	AddBoxPositionsToScratch(),
	AddHozPlotOptionToScratch(),
	AddNotchesOnOrOffToScratch(),
	AddOutlierOptsToScratch(),
	AddWhiskerOnOrOffToScratch(),
	PlotBoxData(),
	plotCmdStdHelp.SetTickValsToGroupCentres(),
	plotCmdStdHelp.SetTickLabelsToGroupLabels(),
	plotCmdStdHelp.SetTickLabelFontSize(),
	plotCmdStdHelp.GridLinesCreate(),
	plotCmdStdHelp.SetTitleStr(),
	plotCmdStdHelp.SetXLabelStr(),
	plotCmdStdHelp.SetXLabelFractPos(),
	plotCmdStdHelp.SetYLabelStr(),
	plotCmdStdHelp.SetYLabelFractPos(),
	plotCmdStdHelp.SetXLimit(),
	plotCmdStdHelp.SetYLimit(),

	plotCmdStdHelp.PlotHozAndVertLines(),

	plotCmdStdHelp.SetLegendFontSize(),
	plotCmdStdHelp.SetLegendNumberColumns(),
	plotCmdStdHelp.SetLegendLocStr(),
	plotCmdStdHelp.SetLegendFractPosStart(),
	SetLegendDataHandlesAndLabels(),
	plotCmdStdHelp.TurnLegendOnIfRequested(),
	]
	return outList


def _createOptionsList():
	outList = [
	BoxColorsOn(),
	BoxColorStrsInterSeries(),
	BoxNotchOn(),
	plotOptStdHelp.DataLabels(),
	plotOptStdHelp.FontSizeDefault(),
	plotOptStdHelp.GridLinesShow(),
	plotOptStdHelp.GridLinesShowX(),
	plotOptStdHelp.GridLinesShowY(),
	plotOptStdHelp.GroupLabels(),
	plotOptStdHelp.GroupLabelRotation(),
	plotOptStdHelp.GroupLabelTicksEveryN(),
	plotOptStdHelp.LegendLocStr(),
	plotOptStdHelp.LegendFractPosStart(),
	plotOptStdHelp.LegendOn(),
	plotOptStdHelp.LegendNumbCols(),
	OutliersShow(),
	PlotDataSingleSeries(),
	PlotDataBox(),
	plotOptStdHelp.PlotHorizontally(value=False),
	plotOptStdHelp.PlotHozLinesColorStrs(),
	plotOptStdHelp.PlotHozLinesPositions(),
	plotOptStdHelp.PlotHozLinesStyleStrs(),
	plotOptStdHelp.PlotVertLinesColorStrs(),
	plotOptStdHelp.PlotVertLinesPositions(),
	plotOptStdHelp.PlotVertLinesStyleStrs(),
	plotOptStdHelp.SetFigsizeOnCreation(),
	plotOptStdHelp.TitleFractPosX(),
	plotOptStdHelp.TitleFractPosY(),
	plotOptStdHelp.TitleStr(),
	plotOptStdHelp.XLabelStr(),
	plotOptStdHelp.XLabelFractPos(),
	plotOptStdHelp.YLabelStr(),
	plotOptStdHelp.YLabelFractPos(),
	plotOptStdHelp.XLimit(),
	plotOptStdHelp.YLimit(),
	WidthBoxes(),
	WidthInterSpacing(),
	WidthIntraSpacing(),
	WhiskersShow()
	]
	return outList



@serializationReg.registerForSerialization()
class BoxColorsOn(plotOptCoreHelp.BooleanPlotOption):
	""" Whether to fill boxes with colors (True=Fill, anything else means don't fill).

	This doesn't need explicitly setting if you have used an option to specify colors for the boxes; its meant for turning on colors with default values. 

	"""
	def __init__(self, name="boxColorsOn", value=None):
		self.name = name
		self.value = value

@serializationReg.registerForSerialization()
class BoxColorStrsInterSeries(plotOptCoreHelp.StringIterPlotOption):
	""" Colors for boxes; whereby each data series is given a different color (but same color is used within a series). This may be overwritten by more specific options.

	Allowed strings are the same as in matplotlib, meaning special color names or hex rgb codes are both fine. For Example ['red','green','orange'] is a valid value

	Note: The number of colors doesnt have to match the number of data series. If you provide too few colors, they will simply cycle. For example if you set ['red','green'] then plotted data would be [red, green, red, green,.... etc]

	"""
	def __init__(self, name="boxColorStrsInterSeries", value=None):
		self.name = name
		self.value = value

@serializationReg.registerForSerialization()
class BoxNotchOn(plotOptCoreHelp.BooleanPlotOption):
	""" Boolean. If True then boxes will have notches representing the confidence interval around the median.

	"""
	def __init__(self, name="boxNotchOn", value=None):
		self.name = name
		self.value = value

@serializationReg.registerForSerialization()
class OutliersShow(plotOptCoreHelp.BooleanPlotOption):
	""" Boolean. If True then outliers will be shown.

	"""
	def __init__(self, name="outliersShow", value=None):
		self.name = name
		self.value = value


@serializationReg.registerForSerialization()
class PlotDataSingleSeries(plotOptCoreHelp.NumpyIterPlotOption):
	""" Plot data option when you only need to plot a single data series (i.e. a non-grouped box plot)

	Format is an iterable of 1-D numpy arrays (or lists); each array represents the data for one box. 

	e.g. "value = [  [1,5,2,3], [6,1,5] ]" will lead to two boxes plotted

	"""
	def __init__(self, name="plotDataSingleSeries", value=None):
		self.name =  name
		self.value = value


@serializationReg.registerForSerialization()
class PlotDataBox(plotOptCoreHelp.IterOfNumpyIterPlotOption):
	""" Plot data for a box plotter. The format is an "iter-of-numpy-iters"; best demonstrated with examples (shown below). The awkward format is to allow for multiple data series; a less general but simpler option ("plotDataSingleSeries") is available if this isnt required.

	Example 1: Single box; (plotDataSingleSeries is the simpler option to use)
		If rawData = [1,4,2] then plotData = [[rawData]]. This gives a single box drawn.

	Example 2: Multiple boxes for different categories; (plotDataSingleSeries is the simpler option to use)
		If ageData = [1,3,1], incomeData=[2,1,5] then plotData = [ [ageData,incomeData] ]. These can then be labelled separately on the axis (e.g. groupLabels=["age", "income"])

	Example 3: Multiple boxes for a single category
		If incomeDataMale=[7,3,5], incomeDataFemale=[8,4] we may want these to share the axis label "income", but (for example) be plotted in different colors with different legend entries. In this case plotData = [ [incomeDataMale], [incomeDataFemale] ] 

	Example 4: Multiple boxes for multiple categories
		Imagine incomeDataMale=[7,3,5], incomeDataFemale=[8,4], ageDataMale=[25,60,45], ageDataFemale=[27,32]. In this case we might want "incomeData" and "ageData" lablled on the axis, but to make separate box-plots for male and female groups. In this case plotData = [ [incomeDataMale, ageDataMale], [incomeDataFemale, ageDataFemale] ]


	"""
	def __init__(self, name="plotDataMultiSeries", value=None):
		self.name = name
		self.value = value


@serializationReg.registerForSerialization()
class WidthBoxes(plotOptCoreHelp.FloatPlotOption):
	""" Width for each box in the chart

	"""
	def __init__(self, name="widthBoxes", value=0.5):
		self.name = name
		self.value = value

@serializationReg.registerForSerialization()
class WidthInterSpacing(plotOptCoreHelp.FloatPlotOption):
	""" Extra space between boxes with different labels

	"""
	def __init__(self, name="widthInterSpacing", value=1.0):
		self.name = name
		self.value = value

@serializationReg.registerForSerialization()
class WidthIntraSpacing(plotOptCoreHelp.FloatPlotOption):
	""" Space between boxes which share a groupLabel but are in different data series

	"""
	def __init__(self, name="widthIntraSpacing", value=0.1):
		self.name = name
		self.value = value

@serializationReg.registerForSerialization()
class WhiskersShow(plotOptCoreHelp.BooleanPlotOption):
	"""The summary line for a class docstring should fit on one line.

	"""
	def __init__(self, name="whiskersShow", value=None):
		self.name = name
		self.value = value

#Commands down here
@serializationReg.registerForSerialization()
class AddDataToScratch(plotCmdCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "add-data-to-plot"
		self._description = "Adds the to-plot data to the scratch space; this allows multiple options for input formats (this command will translate to the native form)"

	#Will be 
	def execute(self, plotterInstance):
		#singleSeries has lowest priority
		singleSeriesPlotData = plotCmdStdHelp._getValueFromOptName(plotterInstance, "plotDataSingleSeries")
		usePlotData = [singleSeriesPlotData]

		multiSeriesPlotData = plotCmdStdHelp._getValueFromOptName(plotterInstance, "plotDataMultiSeries")
		if multiSeriesPlotData is not None:
			usePlotData = list()
			for pData in multiSeriesPlotData:
				currData = [x if x is not None else list() for x in pData]
				usePlotData.append(currData)

		#Set the scratch space values
		plotterInstance._scratchSpace["plotData"] = usePlotData
		def _getLocalDict():
			outDict = dict()
			outDict["boxprops"] = dict()
			return outDict
		plotterInstance._scratchSpace["boxPlotKwargsLocal"] = [_getLocalDict() for x in usePlotData]



@serializationReg.registerForSerialization()
class AddBoxColorToScratch(plotCmdCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "add-box-color-to-scratch-space"
		self._description = "Adds information on the box-colors to use to the scratch space"

	def execute(self, plotterInstance):
		def _setPatchArtistToTrue():
			plotterInstance._scratchSpace["boxPlotKwargsGlobal"]["patch_artist"] = True

		#Basic on/off
		colorsOnOpt = plotCmdStdHelp._getValueFromOptName(plotterInstance, "boxColorsOn")
		if colorsOnOpt is True:
			_setPatchArtistToTrue()

		#Get plot data; needed to figure out ANY other color options
		plotData = plotterInstance._scratchSpace.get("plotData",None)
		if plotData is None:
			return None

		#Figure out colors to use across series
		boxColorStrsInterSeries = plotCmdStdHelp._getValueFromOptName(plotterInstance, "boxColorStrsInterSeries")
		localDicts = plotterInstance._scratchSpace["boxPlotKwargsLocal"]
		if boxColorStrsInterSeries is not None:
			_setPatchArtistToTrue()
			useColors = it.cycle(boxColorStrsInterSeries)
			for colorStr, currDict in zip(useColors, localDicts):
				currDict["boxprops"]["facecolor"] = colorStr

@serializationReg.registerForSerialization()
class AddBoxPositionsToScratch(plotCmdCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "add-box-positions-to-scratch-space"
		self._description = "Adds the positions of each box to the scratch space"

	def execute(self, plotterInstance):
		plotData = plotterInstance._scratchSpace.get("plotData",None)
		if plotData is None:
			return None

		nGroups = max( [len(x) for x in plotData] )
		nSeries = len(plotData)
		widthBoxes = plotCmdStdHelp._getValueFromOptName(plotterInstance, "widthBoxes")
		widthInterSpace = plotCmdStdHelp._getValueFromOptName(plotterInstance, "widthInterSpacing")
		widthIntraSpace = plotCmdStdHelp._getValueFromOptName(plotterInstance, "widthIntraSpacing")

		#Set the global width boxes here; debatable whether it should be moved to another function
		plotterInstance._scratchSpace["boxPlotKwargsGlobal"]["widths"] = widthBoxes

		#
		_currArgs = [nGroups, nSeries, widthBoxes, widthIntraSpace, widthInterSpace]
		barCentres, groupCentres = shared._getIndividAndGroupCentresBarLikePlot(*_currArgs, startPos=0)

		#
		plotterInstance._scratchSpace["centres"] = barCentres
		plotterInstance._scratchSpace["groupCentres"] = groupCentres

		#Set the position keywords based on them [the groupCentres are used in the tick/label code instead]
		for idx,currDict in enumerate(plotterInstance._scratchSpace["boxPlotKwargsLocal"]):
			currDict["positions"] = barCentres[idx] [: len(plotData[idx]) ]

@serializationReg.registerForSerialization()
class AddHozPlotOptionToScratch(plotCmdCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "add-hoz-plot-option-to-scratch"
		self._description = "Modifies boxPlotKwargsGlobal to include an option on whether to plot horizontally or not"

	def execute(self, plotterInstance):
		plotHozOpt = plotCmdStdHelp._getValueFromOptName(plotterInstance, "plotHorizontally")
		if plotHozOpt is True:
			plotCmdStdHelp._setScratchSpaceDictKey(plotterInstance, "boxPlotKwargsGlobal", "vert", False)

@serializationReg.registerForSerialization()
class AddOutlierOptsToScratch(plotCmdCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "add-outlier-opts-to-scratch"
		self._description = "Modifies boxPlotKwargsGlobal to include options related to how to plot outliers (if at all)"

	def execute(self, plotterInstance):
		onOpt = plotCmdStdHelp._getValueFromOptName(plotterInstance, "outliersShow")
		if onOpt is False:
			plotCmdStdHelp._setScratchSpaceDictKey(plotterInstance, "boxPlotKwargsGlobal", "showfliers", False)

@serializationReg.registerForSerialization()
class AddNotchesOnOrOffToScratch(plotCmdCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "set-notches-on-or-off"
		self._description = "Modifies boxPlotKwargsGlobal to set notches on the boxes on or off"

	def execute(self, plotterInstance):
		notchesOn = plotCmdStdHelp._getValueFromOptName(plotterInstance, "boxNotchOn")
		if notchesOn is True:
			plotCmdStdHelp._setScratchSpaceDictKey(plotterInstance, "boxPlotKwargsGlobal", "notch", True)

@serializationReg.registerForSerialization()
class AddWhiskerOnOrOffToScratch(plotCmdCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "set-whiskers-on-or-off"
		self._description = "Modifies boxPlotKwargsGlobal to turn whiskers on or off"

	def execute(self, plotterInstance):
		showWhiskers = plotCmdStdHelp._getValueFromOptName(plotterInstance, "whiskersShow")
		if showWhiskers is False:
			plotCmdStdHelp._setScratchSpaceDictKey(plotterInstance, "boxPlotKwargsGlobal", "whis", 0)

@serializationReg.registerForSerialization()
class PlotBoxData(plotCmdCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "plot-box-data"
		self._description = "Plots boxplot data"

	def execute(self, plotterInstance):
		plotData = plotterInstance._scratchSpace.get("plotData",None)
		if plotData is None:
			return None

		#Will be A LOT more complicated later
		plotKwargsGlobal = plotterInstance._scratchSpace.get("boxPlotKwargsGlobal", dict() )
		seriesHandleDicts = list()
		for pIdx,pData in enumerate(plotData):
			currKwargs = copy.deepcopy( plotKwargsGlobal )
			currKwargs.update( plotterInstance._scratchSpace["boxPlotKwargsLocal"][pIdx] )

			try:
				useData = pData.tolist()
			except AttributeError:
				useData = pData

			currDict = plt.boxplot( useData, **currKwargs)
			seriesHandleDicts.append(currDict)

		plotterInstance._scratchSpace["boxHandles"] = seriesHandleDicts

@serializationReg.registerForSerialization()
class SetLegendDataHandlesAndLabels(plotCmdCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "set-legend-handles-and-labels"
		self._description = "Sets the handles/labels to use in the legend"

	def execute(self, plotterInstance):
		handleDicts = plotterInstance._scratchSpace.get("boxHandles",None)
		dataLabels = plotCmdStdHelp._getValueFromOptName(plotterInstance, "dataLabels")

		if (handleDicts is None) or (dataLabels is None):
			return None

		boxHandles = [x["boxes"][0] for x in handleDicts]

		outLabels, outHandles = list(), list()
		for boxHandle, dataLabel in zip(boxHandles, dataLabels):
			if (boxHandle is not None) and (dataLabel is not None):
				outLabels.append(dataLabel)
				outHandles.append(boxHandle)

		plotCmdStdHelp._setScratchSpaceDictKey(plotterInstance, "legendKwargDict", "handles", outHandles)
		plotCmdStdHelp._setScratchSpaceDictKey(plotterInstance, "legendKwargDict", "labels", outLabels)



