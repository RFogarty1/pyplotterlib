
import json
import types

import numpy as np

import matplotlib.pyplot as plt

from . import shared

from ...core import plotters as plotterCoreHelp
from ...core import plot_command as plotCommCoreHelp
from ...core import plot_options as plotOptCoreHelp
from ...core.serialization import register as serializationReg

from .. import plot_options as plotOptStdHelp
from .. import plot_commands as plotCmdStdHelp


@serializationReg.registerForSerialization()
class HistogramPlotter(shared.FromJsonMixin, shared.FromPlotterMixin, plotterCoreHelp.SingleGraphPlotter):

	def __init__(self, **kwargs):
		""" Initializer
		
		Args:
			kwargs: keys are strs in "HistogramPlotter().optionNames". Values are the values you want to set them to
				 
		"""
		self._createCommands()
		self._createOptions()
		self._scratchSpace = {"legendKwargDict":{}}
		self.setOptionVals(kwargs)

	def _createCommands(self):
		self._commands = _createCommandsList()

	def _createOptions(self):
		_optionsList = _createOptionsList()
		self._options = plotOptCoreHelp.OptionsCollection(options=_optionsList)

def _createCommandsList():
	outList = [
	plotCmdStdHelp.CreateFigureIfNoAxHandle(),
	PlotHistoData(),
	plotCmdStdHelp.SetBarDataLabels(),
	plotCmdStdHelp.SetBarColors(),
	plotCmdStdHelp.SetBarOpacities(),
	plotCmdStdHelp.GridLinesCreate(),
	plotCmdStdHelp.SetXLabelStr(),
	plotCmdStdHelp.SetYLabelStr(),
	plotCmdStdHelp.SetTickMarkerValues(),
	plotCmdStdHelp.SetTickLabelValues(),
	plotCmdStdHelp.SetTickLabelFontSize(),
	plotCmdStdHelp.SetAxisTickAndLabelVisibilitiesEachSide(),
	plotCmdStdHelp.SetTickMinorMarkersOn(),
	plotCmdStdHelp.SetXLabelFractPos(),
	plotCmdStdHelp.SetYLabelFractPos(),
	plotCmdStdHelp.SetXLimit(),
	plotCmdStdHelp.SetYLimit(),
	plotCmdStdHelp.SetAxisColorX(), #Best if done after labels etc. set
	plotCmdStdHelp.SetAxisColorY(),
	plotCmdStdHelp.SetAxisBorderInvisible(),
	plotCmdStdHelp.SetTitleStr(),
	plotCmdStdHelp.SetLegendLocStr(),
	plotCmdStdHelp.SetLegendFontSize(),
	plotCmdStdHelp.SetLegendFractPosStart(),
	plotCmdStdHelp.SetLegendNumberColumns(),
	plotCmdStdHelp.PlotHozAndVertLines(),
	plotCmdStdHelp.TurnLegendOnIfRequested(),
	plotCmdStdHelp.AddPlotterToOutput(),
	plotCmdStdHelp.DrawTextAnnotationsGeneric()
	]

	return outList

#Write in alphabetical order
#Largely taken from Line_Plotter
#TODO: Various forms of plotData
def _createOptionsList():
	outList = [
	plotOptStdHelp.AnnotationsTextGeneric(),
	plotOptStdHelp.AxisBorderMakeInvisible(),
	plotOptStdHelp.AxisColorX(),
	plotOptStdHelp.AxisColorX_exclSpines(),
	plotOptStdHelp.AxisColorY(),
	plotOptStdHelp.AxisColorY_exclSpines(),
	plotOptStdHelp.BarColors(),
	plotOptStdHelp.BarOpacities(),
	plotOptStdHelp.DataLabels(),
	plotOptStdHelp.FontSizeDefault(),
	plotOptStdHelp.GridLinesShow(value=False),
	plotOptStdHelp.GridLinesShowX(),
	plotOptStdHelp.GridLinesShowY(),
	plotOptStdHelp.GridLinesStyle(),
	plotOptStdHelp.GridLinesWidth(),
	InterBarFractSpace(),
	plotOptStdHelp.LegendFractPosStart(),
	plotOptStdHelp.LegendLocStr(),
	plotOptStdHelp.LegendNumbCols(),
	plotOptStdHelp.LegendOn(),
	PlotDataHisto(),
	PlotInReverseOrder(),
	plotOptStdHelp.PlotHozLinesColorStrs(),
	plotOptStdHelp.PlotHozLinesPositions(),
	plotOptStdHelp.PlotHozLinesStyleStrs(),
	plotOptStdHelp.PlotVertLinesColorStrs(),
	plotOptStdHelp.PlotVertLinesPositions(),
	plotOptStdHelp.PlotVertLinesStyleStrs(),
	plotOptStdHelp.SetFigsizeOnCreation(),
	plotOptStdHelp.ShowMinorTickMarkersX(),
	plotOptStdHelp.ShowMinorTickMarkersY(),
	plotOptStdHelp.ShowTicksAndLabelsOnSides( value=types.SimpleNamespace(top=None,bottom=None,left=None, right=None) ),
	plotOptStdHelp.TickMarkerLabelsX(),
	plotOptStdHelp.TickMarkerLabelsY(),
	plotOptStdHelp.TickMarkerValsX(),
	plotOptStdHelp.TickMarkerValsY(),
	plotOptStdHelp.TitleFractPosX(),
	plotOptStdHelp.TitleFractPosY(),
	plotOptStdHelp.TitleStr(),
	plotOptStdHelp.XLabelFractPos(),
	plotOptStdHelp.XLabelStr(),
	plotOptStdHelp.YLabelFractPos(),
	plotOptStdHelp.YLabelStr(),
	plotOptStdHelp.XLimit(),
	plotOptStdHelp.YLimit()
	]
	return outList


#Create options
@serializationReg.registerForSerialization()
class InterBarFractSpace(plotOptCoreHelp.FloatPlotOption):
	""" Determines how much space to leave between bars. The value should be between 0.0 (no space) and 1.0 (no bars)

	"""
	def __init__(self, name=None, value=None):
		self.name = "interBarFractSpace"
		self.value = value


@serializationReg.registerForSerialization()
class PlotDataHisto(plotOptCoreHelp.SinglePlotOptionInter):
	""" Data for plotting in a histogram. The format is an iter of [counts,edges]; each element is equivalent to the return value of numpy.histogram()

	counts (float iter) The counts for each bin; Dimension will be len(edges)-1. (e.g. [3,6,2])
	edges: (float iter) Bin edges from left to right (e.g. [1.0, 1.5, 2.0, 2.5])

	An example value might be:
	[ [ [5,10], [1.0,1.5,2.0] ],
	  [ [20,8], [1.0,1.5,2.0] ] ]

	which would lead to plotting two separate histograms on top of each other
	
	"""
	def __init__(self, name=None, value=None):
		self.name = "plotDataHisto"
		self.value = value

	def __eq__(self, other):
		if self.name != other.name:
			return False

		#Deal with None
		if (self.value is None) and (other.value is None):
			return True

		if (self.value is None) or (other.value is None):
			return False

		#Deal with values in both
		if len(self.value) != len(other.value):
			return False

		for valsA,valsB in zip(self.value, other.value):
			_edgesA, _countsA = valsA
			_edgesB, _countsB = valsB
			if not np.allclose( np.array(_edgesA), np.array(_edgesB) ):
				return False

			if not np.allclose( np.array(_countsA), np.array(_countsB) ):
				return False

		return True

	#fromJSON just inherited; this means fromJSON will use lists rather than np arrays
	def toJSON(self):
		#Note np arrays arent JSON-compatible; hence need to work with them as lists
		if self.value is None:
			outVal = None
		else:
			outVal = self._getValsAsList()

		return json.dumps({"class":str(self.__class__), "payload":{"name":self.name, "value":outVal}})

	def _getValsAsList(self):
		outVals = list()
		for edges, counts in self.value:
			_currEdges = np.array(edges).tolist()
			_currCounts = np.array(counts).tolist()
			outVals.append( [_currEdges, _currCounts] )

		return outVals


@serializationReg.registerForSerialization()
class PlotInReverseOrder(plotOptCoreHelp.BooleanPlotOption):
	""" If True, reverse the plotting order of dataseries. This should ONLY affect which overlays which (rather than anything like colors used). 

	True: Plot in reverse order (earlier dataseries will be plotted on top of later ones)
	False/None: Plot in forward order

	Note: This will also affect the default legend ordering	

	"""

	def __init__(self, name=None, value=None):
		self.name = "plotInRevOrder"
		self.value = value


#Create commands
@serializationReg.registerForSerialization()
class PlotHistoData(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "plot-histogram-data"
		self._description = "Plots histogram data"
		self._revOrderOpt = "plotInRevOrder"

	def execute(self, plotterInstance):
		data = plotCmdStdHelp._getValueFromOptName(plotterInstance, "plotDataHisto")
		if data is None:
			return None

		#Figure out all our bars centres and widths
		_fractSpace = plotCmdStdHelp._getValueFromOptName(plotterInstance, "interBarFractSpace", retIfNone=0.0)
		centresAndWidths = list()
		for currData in data:
			edges = currData[1]
			_currVals = _getBarCentresAndWidthsFromEdges(edges, fractSpace=_fractSpace)
			centresAndWidths.append(_currVals)

		counts = [x[0] for x in data]

		#Reverse order on request
		plotInRevOrder = plotCmdStdHelp._getValueFromOptName(plotterInstance, self._revOrderOpt)
		if plotInRevOrder:
			centresAndWidths = reversed(centresAndWidths)
			counts = list(reversed(counts))

		#Plot the bars
		outBars = list()
		for idx,(centres,widths) in enumerate(centresAndWidths):
			currBars = plt.bar( np.array(centres), np.array(counts[idx]), width=widths)
			outBars.append(currBars)

		#Reverse order on request
		if plotInRevOrder:
			outBars = list(reversed(outBars))

		plotterInstance._scratchSpace["barHandles"] = outBars


def _getBarCentresAndWidthsFromEdges(edges, fractSpace=0.0):
	outCentres, outWidths = list(), list()

	for idx,_unused in enumerate(edges[:-1]):
		_edgePair = edges[idx], edges[idx+1]
		_currWidth = abs(_edgePair[0] - _edgePair[1])
		_currCentre = min(_edgePair) + 0.5*_currWidth
		_useWidth = _currWidth - (fractSpace*_currWidth)
		outCentres.append(_currCentre)
		outWidths.append(_useWidth)

	return outCentres, outWidths



