
import itertools as it

import matplotlib.pyplot as plt
import numpy as np

from ...core import plotters as plotterCoreHelp
from ...core import plot_command as plotCommCoreHelp
from ...core import plot_options as plotOptCoreHelp

from .. import plot_options as plotOptStdHelp
from .. import plot_commands as plotCmdStdHelp


class BarPlotter(plotterCoreHelp.SingleGraphPlotter):

	def __init__(self, **kwargs):
		""" Initializer
		
		Args:
			kwargs: keys are strs in [x.name for x in BarPlotter().opts]. Values are the values you want to set them to
				 
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
	plotCmdStdHelp.AddPlotterToOutput(),
	plotCmdStdHelp.CreateFigureIfNoAxHandle(),
	CalculateCentreVals(),
	PlotOneDimDataAsBars(),
	SetTickValsToGroupCentres(),
	SetTickLabelsToGroupLabels(),
	SetBarDataLabels(),
	plotCmdStdHelp.SetXLabelStr(),
	plotCmdStdHelp.SetYLabelStr(),
	plotCmdStdHelp.SetXLabelFractPos(),
	plotCmdStdHelp.SetYLabelFractPos(),
	plotCmdStdHelp.SetXLimit(),
	plotCmdStdHelp.SetYLimit(),
	plotCmdStdHelp.SetAxisColorX(), #Best if done after labels etc. set
	plotCmdStdHelp.SetAxisColorY(),
	plotCmdStdHelp.SetAxisBorderInvisible(),
	plotCmdStdHelp.SetLegendLocStr(),
	plotCmdStdHelp.SetLegendFractPosStart(),
	plotCmdStdHelp.SetLegendNumberColumns(),
	plotCmdStdHelp.TurnLegendOnIfRequested()
	]
	return outList

def _createOptionsList():
	outList = [
	plotOptStdHelp.AxisBorderMakeInvisible(),
	plotOptStdHelp.AxisColorX(),
	plotOptStdHelp.AxisColorX_exclSpines(),
	plotOptStdHelp.AxisColorY(),
	plotOptStdHelp.AxisColorY_exclSpines(),
	plotOptStdHelp.DataLabels(),
	GroupLabels(),
	plotOptStdHelp.LegendFractPosStart(),
	plotOptStdHelp.LegendLocStr(),
	plotOptStdHelp.LegendNumbCols(),
	plotOptStdHelp.LegendOn(),
	plotOptStdHelp.PlotData1D(),
	PlotHorizontally(value=False),
	WidthBars(value=1.0),
	WidthInterSpacing(),
	WidthIntraSpacing(value=0.0),
	plotOptStdHelp.SetFigsizeOnCreation(),
	plotOptStdHelp.XLabelFractPos(),
	plotOptStdHelp.XLabelStr(),
	plotOptStdHelp.YLabelFractPos(),
	plotOptStdHelp.YLabelStr(),
	plotOptStdHelp.XLimit(),
	plotOptStdHelp.YLimit()
	
	]
	return outList


#Options

class GroupLabels(plotOptCoreHelp.StringIterPlotOption):
	"""String iter. Each is a label for a group of bars; if your only plotting one data series then this means 1 label per value input. 

	E.g. If plotting years vs population this might be ["1970", "1980", "1990"]

	"""
	def __init__(self, name=None, value=None):
		self.name = "groupLabels"
		self.value = value


class PlotHorizontally(plotOptCoreHelp.BooleanPlotOption):
	""" Boolean. If False labels are on the x-axis and bars on the y-axis. If True, its the other way around.

	"""
	def __init__(self, name=None, value=None):
		self.name = "plotHorizontally"
		self.value = value


class WidthBars(plotOptCoreHelp.FloatPlotOption):
	""" Width value for each bar in the bar chart. The default is generally 1.0

	"""
	def __init__(self, name=None, value=None):
		self.name = "widthBars"
		self.value = value

class WidthInterSpacing(plotOptCoreHelp.FloatPlotOption):
	""" Space between data for different labels. E.g. if you had a plot of population by various years, this would be the space between a bar for year 1971 and year 1972. Default will generally be some multiple of bar width

	"""
	def __init__(self, name=None, value=None):
		self.name = "widthInterSpacing"
		self.value = value

class WidthIntraSpacing(plotOptCoreHelp.FloatPlotOption):
	""" Space between bars with the same label, but for different data series. The default is generally 0.

	"""
	def __init__(self, name=None, value=None):
		self.name = "widthIntraSpacing"
		self.value = value




#Commands
class CalculateCentreVals(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "calculate-bar-centre-vals"
		self._description = "Calculates the central position of each bar in the bar plot and saves to the scratch space"

	def execute(self, plotterInstance):
		#Get the data, exit if none present
		plotData = getattr(plotterInstance.opts, "plotData1D").value
		if plotData is None:
			return None
		elif len(plotData)==0:
			return None

		#Get the relevant widths
		widthBars = plotterInstance.opts.widthBars.value
		widthInterSpacing = plotterInstance.opts.widthInterSpacing.value
		widthIntraSpacing = plotterInstance.opts.widthIntraSpacing.value

		widthBars = 1 if widthBars is None else widthBars
		widthInterSpacing = 1 if widthInterSpacing is None else widthInterSpacing
		widthIntraSpacing = 0.0 if widthIntraSpacing is None else widthIntraSpacing

		#Calculate the centre values
		nGroups = max( [len(x) for x in plotData] )
		nSeries = len(plotData)
		outCentres = [ list() for x in range(nSeries) ] 
		currPos = 0

		for groupIdx in range(nGroups):
			for seriesIdx in range(nSeries):
				outCentres[seriesIdx].append(currPos)
				currPos += widthBars
				currPos += widthIntraSpacing

			currPos += widthInterSpacing

		plotterInstance._scratchSpace["centres"] = outCentres

		#Figure out the centre of each GROUP
		groupCentres = list()
		for idx in range(nGroups):
			currCentres = [ x[idx] for x in outCentres ]
			currAverage = sum(currCentres)/len(currCentres)
			groupCentres.append(currAverage)
		plotterInstance._scratchSpace["groupCentres"] = groupCentres


#This will get A LOT more complicated later (when dealing with widths etc)
class PlotOneDimDataAsBars(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "plot-bar-data"
		self._description = "Plots available data using bar chart plotter"
		self._optName = "plotData1D"

	def execute(self, plotterInstance):
		#Get the data; exit if none present
		targVal = getattr(plotterInstance.opts, self._optName).value

		if not( _doesPlotterInstanceHaveData(plotterInstance) ):
			return None

		#Check if we plot vertically or horizontally
		plotHoz = plotterInstance.opts.plotHorizontally.value
		allCentres = plotterInstance._scratchSpace["centres"]

		#Figure out the bar widths
		barWidth = plotterInstance.opts.widthBars.value
		barWidth = 1.0 if barWidth is None else barWidth


		#Plot the data; may want to return handles to scratch space later
		outBars = list()
		for idx,currData in enumerate(targVal):
			centres = allCentres[idx]

			useCentres = [centre for centre,val in zip(centres,currData) if val is not None]
			useData = [val for val in currData if val is not None]

			if plotHoz:
				currBars = plt.barh( np.array(useCentres), np.array(useData), height=barWidth )
			else:
				currBars = plt.bar( np.array(useCentres), np.array(useData), width=barWidth )

			outBars.append(currBars)

		plotterInstance._scratchSpace["barHandles"] = outBars
		return


class SetBarDataLabels(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "set-data-labels-for-bars"
		self._description = "Sets the data labels (to use in a legend) for a bar chart; this is different to the line plotter version since theres no safe equivalent to ax.get_lines()"
		self._optName = "dataLabels"

	def execute(self, plotterInstance):
		dataLabels = getattr(plotterInstance.opts, self._optName).value
		if dataLabels is None:
			return None

		if not _doesPlotterInstanceHaveData(plotterInstance):
			return None

		plottedBars = plotterInstance._scratchSpace["barHandles"] 
		for barHandle, dataLabel in zip(plottedBars, dataLabels):
			if dataLabel is not None:
				barHandle.set_label(dataLabel)


class SetTickValsToGroupCentres(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "set-tick-val-to-group-centres"
		self._description = "Sets the tick markers to the centre of each group of bars"
		
	def execute(self, plotterInstance):
		#Check if we have any data; exit if not
		if not( _doesPlotterInstanceHaveData(plotterInstance) ):
			return None

		plotHoz = plotterInstance.opts.plotHorizontally.value
		groupCentres = plotterInstance._scratchSpace["groupCentres"]
		if plotHoz:
			plt.gca().set_yticks(groupCentres)
		else:
			plt.gca().set_xticks(groupCentres)
		
class SetTickLabelsToGroupLabels(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "set-tick-labels-to-group-names"
		self._description = "Sets the axis tick labels to group names"

	def execute(self, plotterInstance):
		#Check if we have any data; exit if not
		if not( _doesPlotterInstanceHaveData(plotterInstance) ):
			return None

		groupLabels = plotterInstance.opts.groupLabels.value
		if groupLabels is None:
			return None

		#
		nGroups = len(plotterInstance._scratchSpace["groupCentres"])
		useLabels = [ label for label,unused in it.zip_longest(groupLabels, range(nGroups)) ]

		#
		plotHoz = plotterInstance.opts.plotHorizontally.value
		if plotHoz:
			plt.gca().set_yticklabels(useLabels)
		else:
			plt.gca().set_xticklabels(useLabels)



def _doesPlotterInstanceHaveData(plotterInstance):
	targVal = getattr(plotterInstance.opts, "plotData1D").value
	if targVal is None:
		return False
	elif len(targVal)==0:
		return False
	return True


