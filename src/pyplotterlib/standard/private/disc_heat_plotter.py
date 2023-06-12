
import itertools as it

import matplotlib.colors
import matplotlib.pyplot as plt

import numpy as np

from . import shared

from .. import plot_options as plotOptStdHelp
from .. import plot_commands as plotCmdStdHelp

from ...core import plotters as plotterCoreHelp
from ...core import plot_command as plotCmdCoreHelp
from ...core import plot_options as plotOptCoreHelp

from ...core.serialization import register as serializationReg


@serializationReg.registerForSerialization()
class DiscreteHeatMapPlotter(shared.FromJsonMixin, shared.FromPlotterMixin, plotterCoreHelp.SingleGraphPlotter):
	""" Plotter for creating heat-map visualisations of discrete data. Examples are to visualise correlation or covariance matrices between variables; each pair is then displayed as a rectangle with color mapped to the value.

	"""
	def __init__(self, **kwargs):
		""" Initializer
		
		Args:
			kwargs: Keys are strs in "DiscreteHeatMapPlotter().optionNames". Values are the values you want to set them to
				 
		"""
		self._createCommands()
		self._createOptions()
		self._scratchSpace = dict()
		self.setOptionVals(kwargs)

	def _createCommands(self):
		self._commands = _createCommandsList()

	def _createOptions(self):
		_optionsList = _createOptionsList()
		self._options = plotOptCoreHelp.OptionsCollection(options=_optionsList)



def _createCommandsList():
	outList = [
	plotCmdStdHelp.CreateFigureIfNoAxHandle(),
	plotCmdStdHelp.SetAspectStr(),
	plotCmdStdHelp.AddPlotterToOutput(),
	plotCmdStdHelp.CopyNumpyArrayPlotDataToScratchSpace(),
	RemoveUnwantedPlotData(),
	plotCmdStdHelp.SetColormapInPlotKwargs(),
	plotCmdStdHelp.SetColormapMaxValInPlotKwargs(),
	plotCmdStdHelp.SetColormapMinValInPlotKwargs(),
	AddDataToPlot(),
	plotCmdStdHelp.AddColorBar(),
	plotCmdStdHelp.SetColorbarFontSizes(),
	plotCmdStdHelp.SetXLabelStr(),
	plotCmdStdHelp.SetYLabelStr(),
	SetTicksToDataCentres(),
	SetTickLabelsToGroupLabels(),
	AddDataAnnotations(),
	plotCmdStdHelp.SetTickLabelFontSize(),
	plotCmdStdHelp.GridLinesCreate(),
	plotCmdStdHelp.SetTitleStr(),
	plotCmdStdHelp.DrawTextAnnotationsGeneric(),
	]
	return outList

def _createOptionsList():
	outList = [
	AnnotateVals(),
	AnnotateValsFontSize(),
	AnnotateValsRotation(),
	AnnotateValsStrFmt(value="{:.2f}"),
	AnnotateValsTextColor(),
	plotOptStdHelp.AnnotationsTextGeneric(),
	plotOptStdHelp.AspectString(value="auto"),
	plotOptStdHelp.ColorBarFontSize(),
	plotOptStdHelp.ColorBarLabelFontSize(),
	plotOptStdHelp.ColorBarTickLabelFontSize(),
	plotOptStdHelp.ColorBarLabel(),
	plotOptStdHelp.ColorBarLocation(),
	plotOptStdHelp.ColorBarShow(),
	plotOptStdHelp.ColorBarLabelRotation(),
	plotOptStdHelp.ColormapMaxVal(),
	plotOptStdHelp.ColormapMinVal(),
	plotOptStdHelp.ColormapStr(),
	plotOptStdHelp.FontSizeDefault(),
	plotOptStdHelp.GridLinesShow(value=False),
	plotOptStdHelp.GridLinesShowX(),
	plotOptStdHelp.GridLinesShowY(),
	plotOptStdHelp.GridLinesStyle(),
	plotOptStdHelp.GridLinesWidth(),
	plotOptStdHelp.GroupLabels(),
	GroupLabelsCols(),
	GroupLabelsColsRotation(),
	GroupLabelsRows(),
	GroupLabelsRowsRotation(),
	PlotDataDiscHeat(),
	PlotDiag(value=True),
	PlotLowerTri(value=True),
	PlotUpperTri(value=True),
	plotOptStdHelp.SetFigsizeOnCreation(),
	plotOptStdHelp.TitleStr(),
	plotOptStdHelp.XLabelStr(),
	plotOptStdHelp.YLabelStr()
	]
	return outList


#Note: Similar option in image_plotter; just has a different self.name and array can be 3-dimensional
@serializationReg.registerForSerialization()
class AnnotateVals(plotOptCoreHelp.BooleanPlotOption):
	""" Whether to add annotations showing the value in each cell (True=Add annotations; False=Dont)
	
	"""
	def __init__(self, name=None, value=None):
		self.name = "annotateVals"
		self.value = value

@serializationReg.registerForSerialization()
class AnnotateValsFontSize(plotOptCoreHelp.IntPlotOption):
	""" The font size to use for annotations; will override less-specific "fontSizeDefault" option
	
	"""
	def __init__(self, name=None, value=None):
		self.name = "annotateValsFontSize"
		self.value = value

@serializationReg.registerForSerialization()
class AnnotateValsRotation(plotOptCoreHelp.FloatPlotOption):
	""" The rotation of text annotations. Units are degrees

	"""
	def __init__(self, name=None, value=None):
		self.name = "annotateValsRotation"
		self.value = value

@serializationReg.registerForSerialization()
class AnnotateValsStrFmt(plotOptCoreHelp.StringPlotOption):
	""" The string format to use when generating annotation values from data. E.g. "{:.2f}" means use two decimal places. We generate each annotation by applying AnnotateValsStrFmt.value.format(x) [where x is the plotted data value]
	
	"""
	def __init__(self, name=None, value=None):
		self.name = "annotateValsStrFmt"
		self.value = value

@serializationReg.registerForSerialization()
class AnnotateValsTextColor(plotOptCoreHelp.StringOrStringIterPlotOption):
	""" The text color to use for value annotations. Allowed strings are the same as in matplotlib, meaning special color names or hex rgb codes are both fine. For Example ['red','green','orange'] are valid values.

	Note: This can be set to either a single string (e.g. 'r') or an array of strings (e.g. ['r','g']). If an array is used then the text color used depends on the value of the data point. For example, if your plot data is in the range[-1,1] then ['r','g'] will switch between red for low values (<=0) and green for higher values (>0). Two colors (at least) are usually needed for all to be visible
	
	"""
	def __init__(self, name=None, value=None):
		self.name = "annotateValsTextColor"
		self.value = value

@serializationReg.registerForSerialization()
class GroupLabelsRows(plotOptCoreHelp.StringIterPlotOption):
	""" Labels for rows of matrix; these will be displayed along the y-axis.

	Note: These should take priority over less specific "groupLabels" options 
	"""
	def __init__(self, name=None, value=None):
		self.name = "groupLabelsRows"
		self.value = value

@serializationReg.registerForSerialization()
class GroupLabelsCols(plotOptCoreHelp.StringIterPlotOption):
	""" Labels for columns of matrix; these will be displayed along the x-axis.

	Note: These should take priority over less specific "groupLabels" options 
	"""
	def __init__(self, name=None, value=None):
		self.name = "groupLabelsCols"
		self.value = value

@serializationReg.registerForSerialization()
class GroupLabelsColsRotation(plotOptCoreHelp.FloatPlotOption):
	""" The rotation of labels for the columns (x-axis). Units are degrees.
	
	"""
	def __init__(self, name=None, value=None):
		self.name = "groupLabelsColsRotation"
		self.value = value

@serializationReg.registerForSerialization()
class GroupLabelsRowsRotation(plotOptCoreHelp.FloatPlotOption):
	""" The rotation of labels for the rows (y-axis). Units are degrees
	
	"""
	def __init__(self, name=None, value=None):
		self.name = "groupLabelsRowsRotation"
		self.value = value

@serializationReg.registerForSerialization()
class PlotDataDiscHeat(plotOptCoreHelp.NumpyArrayPlotOption):
	""" Data to plot; should be a SINGLE two-dimensional numpy array (e.g. np.array( [ [1.0,0.3], [0.3,1.0] ]) """

	def __init__(self, name=None, value=None):
		self.name = "plotData"
		self.value = value

@serializationReg.registerForSerialization()
class PlotLowerTri(plotOptCoreHelp.BooleanPlotOption):
	""" Boolean; whether to plot the lower triangular part of the input matrix (True=yes;False=No) """

	def __init__(self, name=None, value=None):
		self.name = "plotLowerTri"
		self.value = value

@serializationReg.registerForSerialization()
class PlotDiag(plotOptCoreHelp.BooleanPlotOption):
	""" Boolean; whether to plot the diagonal elements of the input matrix (True=yes;False=No) """

	def __init__(self, name=None, value=None):
		self.name = "plotDiag"
		self.value = value


@serializationReg.registerForSerialization()
class PlotUpperTri(plotOptCoreHelp.BooleanPlotOption):
	""" Boolean; whether to plot the upper triangular part of the input matrix (True=yes;False=No) """

	def __init__(self, name=None, value=None):
		self.name = "plotUpperTri"
		self.value = value



#All commands
@serializationReg.registerForSerialization()
class AddDataToPlot(plotCmdCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "add-data-to-plot"
		self._description = "Adds data to the plot using plt.imshow(data)"
		self._plotDataAttr = "plotData"

	def execute(self, plotterInstance):
		data = plotterInstance._scratchSpace["usePlotData"]
		if data is None:
			return None
		else:
			plotKwargs = plotterInstance._scratchSpace.get("plotKwargs", dict())
			plt.imshow(data, **plotKwargs)

@serializationReg.registerForSerialization()
class AddDataAnnotations(plotCmdCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "add-data-annotations"
		self._description = "Adds float-annotations to each plotted data point"
	
	def execute(self, plotterInstance):
		annotate = plotCmdStdHelp._getValueFromOptName(plotterInstance, "annotateVals")
		if annotate is not True:
			return None

		#Do nothing if we have no data
		data = plotterInstance._scratchSpace["usePlotData"]
		if data is None:
			return None
		data = np.array(data)

		#Add the text annotations
		fmtStr = plotCmdStdHelp._getValueFromOptName(plotterInstance,"annotateValsStrFmt", retIfNone="{}")
		nRows, nCols = data.shape
		annotateColor = plotCmdStdHelp._getValueFromOptName(plotterInstance, "annotateValsTextColor")
		annotateRotation = plotCmdStdHelp._getValueFromOptName(plotterInstance, "annotateValsRotation")

		useFontSize = plotCmdStdHelp._getValueFromOptName(plotterInstance, "fontSizeDefault")
		useFontSize = plotCmdStdHelp._getValueFromOptName(plotterInstance, "annotateValsFontSize", retIfNone=useFontSize)

		colorArray = self._getColorArray(plotterInstance, data)

		for rIdx in range(nRows):
			for cIdx in range(nCols):
				currVal = data[rIdx,cIdx]
				if not np.isnan(currVal):
					plt.gca().text(cIdx, rIdx, fmtStr.format(currVal),
					               ha="center", va="center", color=colorArray[rIdx][cIdx], fontsize=useFontSize, rotation=annotateRotation)


	def _getColorArray(self, plotterInstance, inpData):
		outArray = np.empty( inpData.shape, dtype= object )
		nRows, nCols = inpData.shape
		colors = self._getListOfColorsToUse(plotterInstance)

		#Normalizer the data
		lowerBound, upperBound = np.nanmin(inpData), np.nanmax(inpData)
		lowerBound = plotCmdStdHelp._getValueFromOptName(plotterInstance, "colorMapMinVal", retIfNone=lowerBound)
		upperBound = plotCmdStdHelp._getValueFromOptName(plotterInstance, "colorMapMaxVal", retIfNone=upperBound)
		_normalizer = matplotlib.colors.Normalize(vmin=lowerBound, vmax=upperBound)
		useData = _normalizer(inpData)

		#Figure out the colormapping
		minVal, maxVal, rangeCurr = 0.0, 1.0, 1.0 #Properties of normalisation
		nColors = len(colors)
		stepVal = rangeCurr/(nColors)

		#Figure out the thresholds
		thresHolds = list()
		for idx in range(nColors):
			if idx==0:
				currVal = minVal + stepVal
			else:
				currVal = thresHolds[idx-1] + stepVal
			thresHolds.append(currVal)


		#Function to get a color from a data value
		def _getColor(inpVal):
			useIdx = -1
			for idx,thres in enumerate(thresHolds):
				if inpVal <= thres:
					useIdx = idx
					break
			outColor = colors[useIdx]
			return outColor

		#
		for rIdx in range(nRows):
			for cIdx in range(nCols):
				outArray[rIdx][cIdx] = _getColor(useData[rIdx][cIdx])

		return outArray	

	def _getListOfColorsToUse(self, plotterInstance):
		rawColors = plotCmdStdHelp._getValueFromOptName(plotterInstance, "annotateValsTextColor")
		if rawColors is None:
			return [None]

		if isinstance(rawColors,str):
			output = [rawColors]
		else:
			output = rawColors
		return output




@serializationReg.registerForSerialization()
class RemoveUnwantedPlotData(plotCmdCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "remove-unwanted-plot-data"
		self._description = "Sets certain plot-data values to np.nan as requested (e.g. if you dont want to plot the diagonal elements)"


	def execute(self, plotterInstance):
		data = plotterInstance._scratchSpace["usePlotData"]
		lowerTri = plotCmdStdHelp._getValueFromOptName(plotterInstance, "plotLowerTri")
		diagTri  = plotCmdStdHelp._getValueFromOptName(plotterInstance, "plotDiag")
		upperTri = plotCmdStdHelp._getValueFromOptName(plotterInstance, "plotUpperTri")

		#TODO: Merging all would be nice more efficient
		if not lowerTri:
			self._setLowerTriToNan(data)

		if not upperTri:
			self._setUpperTriToNan(data)

		if not diagTri:
			self._setDiagTriToNan(data)

	def _setLowerTriToNan(self,data):
		nRows, nCols = data.shape
		for rIdx in range(nRows):
			for cIdx in range(nCols):
				if rIdx > cIdx:
					data[rIdx][cIdx] = np.nan

	def _setDiagTriToNan(self, data):
		nRows, nCols = data.shape
		for rIdx in range(nRows):
			for cIdx in range(nCols):
				if rIdx == cIdx:
					data[rIdx][cIdx] = np.nan

	def _setUpperTriToNan(self,data):
		nRows, nCols = data.shape
		for rIdx in range(nRows):
			for cIdx in range(nCols):
				if rIdx < cIdx:
					data[rIdx][cIdx] = np.nan

#Similar in bar plotter; but this is actually a bit different since we set both x/y as standard
@serializationReg.registerForSerialization()
class SetTickLabelsToGroupLabels(plotCmdCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "set-tick-labels-to-group-names"
		self._description = "Sets the axis tick labels to group names"
		self._plotDataAttr = "plotData"
		self._groupLabelAttr = "groupLabels"

	def execute(self, plotterInstance):
		data = plotCmdStdHelp._getValueFromOptName(plotterInstance, self._plotDataAttr)
		groupLabels = plotCmdStdHelp._getValueFromOptName(plotterInstance, self._groupLabelAttr)
		groupLabelsCols = plotCmdStdHelp._getValueFromOptName(plotterInstance, "groupLabelsCols")
		groupLabelsRows = plotCmdStdHelp._getValueFromOptName(plotterInstance, "groupLabelsRows")

		if (data is None):
			return None

		if (groupLabels is None) and (groupLabelsCols is None) and (groupLabelsRows is None):
			return None

		#
		groupLabelsX = groupLabelsCols
		groupLabelsX = groupLabelsX if groupLabelsX is not None else groupLabels
		rotationX = plotCmdStdHelp._getValueFromOptName(plotterInstance, "groupLabelsColsRotation")

		groupLabelsY = groupLabelsRows
		groupLabelsY = groupLabelsY if groupLabelsY is not None else groupLabels
		rotationY = plotCmdStdHelp._getValueFromOptName(plotterInstance, "groupLabelsRowsRotation")

		#Figure out the labels to use
		ticksX, ticksY = plt.gca().get_xticks(), plt.gca().get_yticks()
		def _getUseLabels(inpTicks, inpLabels):
			if inpLabels is None:
				return None
			outLabels = [label if label is not None else tickVal for label,tickVal in it.zip_longest(inpLabels, inpTicks)]
			return outLabels[:len(inpTicks)]

		useLabelsX = _getUseLabels(ticksX, groupLabelsX)
		useLabelsY = _getUseLabels(ticksY, groupLabelsY)

		#
		if useLabelsX is not None:
			plt.gca().set_xticklabels(useLabelsX, rotation=rotationX)
		if useLabelsY is not None:
			plt.gca().set_yticklabels(useLabelsY, rotation=rotationY)
		


@serializationReg.registerForSerialization()
class SetTicksToDataCentres(plotCmdCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "set-ticks-to-data-centres"
		self._description = "Sets the x/y tick marker positions to match up with centres of data points"
		self._plotDataAttr = "plotData"

	def execute(self, plotterInstance):
		data = plotCmdStdHelp._getValueFromOptName(plotterInstance, self._plotDataAttr)
		if data is None:
			return None

		data = np.array(data, copy=False)
		assert len(data.shape)==2
		nY, nX = np.array(data).shape
		
		plt.gca().set_xticks( list(range(nX)) )
		plt.gca().set_yticks( list(range(nY)) ) 


