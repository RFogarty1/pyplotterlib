
import itertools as it
import types

import matplotlib.ticker
import matplotlib.pyplot as plt
import numpy as np

from . import shared

from ...core import plotters as plotterCoreHelp
from ...core import plot_command as plotCommCoreHelp
from ...core import plot_options as plotOptCoreHelp

from ...core.serialization import register as serializationReg

from .. import plot_options as plotOptStdHelp
from .. import plot_commands as plotCmdStdHelp

@serializationReg.registerForSerialization()
class BarPlotter(shared.FromJsonMixin, shared.FromPlotterMixin, plotterCoreHelp.SingleGraphPlotter):

	def __init__(self, **kwargs):
		""" Initializer
		
		Args:
			kwargs: keys are strs in "BarPlotter().optionNames". Values are the values you want to set them to
				 
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
	SetTickMinorValsOnOrOff(),
	plotCmdStdHelp.GridLinesCreate(),
	SetBarDataLabels(),
	plotCmdStdHelp.SetBarColors(),
	plotCmdStdHelp.SetBarOpacities(),
	plotCmdStdHelp.SetXLabelStr(),
	plotCmdStdHelp.SetYLabelStr(),
	plotCmdStdHelp.SetTickLabelFontSize(),
	plotCmdStdHelp.SetXLabelFractPos(),
	plotCmdStdHelp.SetYLabelFractPos(),
	plotCmdStdHelp.SetXLimit(),
	plotCmdStdHelp.SetYLimit(),
	plotCmdStdHelp.SetAxisColorX(), #Best if done after labels etc. set
	plotCmdStdHelp.SetAxisColorY(),
	plotCmdStdHelp.SetAxisBorderInvisible(),
	plotCmdStdHelp.SetAxisTickAndLabelVisibilitiesEachSide(),
	plotCmdStdHelp.SetLegendLocStr(),
	plotCmdStdHelp.SetLegendFontSize(),
	plotCmdStdHelp.SetLegendFractPosStart(),
	plotCmdStdHelp.SetLegendNumberColumns(),
	plotCmdStdHelp.SetTitleStr(),
	plotCmdStdHelp.PlotHozAndVertLines(),
	plotCmdStdHelp.TurnLegendOnIfRequested(),
	plotCmdStdHelp.DrawShadedAnnotationsGeneric(),
	plotCmdStdHelp.DrawTextAnnotationsGeneric()
	]
	return outList

def _createOptionsList():
	outList = [
	plotOptStdHelp.AnnotationsShadedGeneric(),
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
	GroupLabels(),
	GroupLabelRotation(),
	plotOptStdHelp.LegendFractPosStart(),
	plotOptStdHelp.LegendLocStr(),
	plotOptStdHelp.LegendNumbCols(),
	plotOptStdHelp.LegendOn(),
	plotOptStdHelp.PlotData1D(),
	PlotHorizontally(value=False),
	plotOptStdHelp.PlotHozLinesColorStrs(),
	plotOptStdHelp.PlotHozLinesPositions(),
	plotOptStdHelp.PlotHozLinesStyleStrs(),
	plotOptStdHelp.PlotVertLinesColorStrs(),
	plotOptStdHelp.PlotVertLinesPositions(),
	plotOptStdHelp.PlotVertLinesStyleStrs(),
	ShowMinorTickMarkers(),
	ReverseIntraBarOrdering(),
	WidthBars(value=1.0),
	WidthInterSpacing(),
	WidthIntraSpacing(value=0.0),
	plotOptStdHelp.SetFigsizeOnCreation(),
	plotOptStdHelp.ShowTicksAndLabelsOnSides( value=types.SimpleNamespace(top=None,bottom=None,left=None, right=None) ),
	plotOptStdHelp.TitleStr(),
	plotOptStdHelp.XLabelFractPos(),
	plotOptStdHelp.XLabelStr(),
	plotOptStdHelp.YLabelFractPos(),
	plotOptStdHelp.YLabelStr(),
	plotOptStdHelp.XLimit(),
	plotOptStdHelp.YLimit()
	
	]
	return outList


#Options
@serializationReg.registerForSerialization()
class GroupLabels(plotOptStdHelp.GroupLabels):

	"""String iter. Each is a label for a group of bars; if your only plotting one data series then this means 1 label per value input. 

	E.g. If plotting years vs population this might be ["1970", "1980", "1990"]

	"""
	pass

@serializationReg.registerForSerialization()
class GroupLabelRotation(plotOptStdHelp.GroupLabelRotation):
	""" Sets the rotation angle (in degrees) for the bar chart labels (xtick labels for vertical, ytick labels for horizontal)

	"""
	pass

@serializationReg.registerForSerialization()
class PlotHorizontally(plotOptStdHelp.PlotHorizontally):
	""" Boolean. If False labels are on the x-axis and bars on the y-axis. If True, its the other way around.

	"""
	pass

@serializationReg.registerForSerialization()
class ReverseIntraBarOrdering(plotOptCoreHelp.BooleanPlotOption):
	""" Boolean. Setting to True reverses the ordering of bars in a given group (but data series ordering is the same). 

	For example, if you have three data series A,B,C and 1 value on the x-axis (and plot vertically) then setting to False will plot the bars as A/B/C; Setting to True with plot as C/B/A. But ordering in the legend will be unaffected.

	"""
	def __init__(self, name=None, value=None):
		self.name = "reverseIntraBarOrdering"
		self.value = value


@serializationReg.registerForSerialization()
class ShowMinorTickMarkers(plotOptCoreHelp.BooleanPlotOption):
	""" Boolean. Setting to True means the minor tick markers will be shown

	"""
	def __init__(self, name=None, value=None):
		self.name = "showMinorTickMarkers"
		self.value = value

@serializationReg.registerForSerialization()
class WidthBars(plotOptCoreHelp.FloatPlotOption):
	""" Width value for each bar in the bar chart. The default is generally 1.0

	"""
	def __init__(self, name=None, value=None):
		self.name = "widthBars"
		self.value = value

@serializationReg.registerForSerialization()
class WidthInterSpacing(plotOptCoreHelp.FloatPlotOption):
	""" Space between data for different labels. E.g. if you had a plot of population by various years, this would be the space between a bar for year 1971 and year 1972. Default will generally be some multiple of bar width

	"""
	def __init__(self, name=None, value=None):
		self.name = "widthInterSpacing"
		self.value = value

@serializationReg.registerForSerialization()
class WidthIntraSpacing(plotOptCoreHelp.FloatPlotOption):
	""" Space between bars with the same label, but for different data series. The default is generally 0.

	"""
	def __init__(self, name=None, value=None):
		self.name = "widthIntraSpacing"
		self.value = value




#Commands
@serializationReg.registerForSerialization()
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

		_currArgs = [nGroups, nSeries, widthBars, widthIntraSpacing, widthInterSpacing]
		barCentres, groupCentres = shared._getIndividAndGroupCentresBarLikePlot(*_currArgs, startPos=0)

		plotterInstance._scratchSpace["centres"] = barCentres
		plotterInstance._scratchSpace["groupCentres"] = groupCentres


#This will get A LOT more complicated later (when dealing with widths etc)
@serializationReg.registerForSerialization()
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


		#Optionally reverse the order the bars are plotted in
		reverseIntraOrdering = getattr(plotterInstance.opts, "reverseIntraBarOrdering").value

		#Plot the data; may want to return handles to scratch space later
		outBars = list()
		for idx,currData in enumerate(targVal):
			#We need centres for idx from the other end is all
			if reverseIntraOrdering:
				centres = allCentres[len(targVal)-1-idx]

			else:
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

@serializationReg.registerForSerialization()
class SetBarDataLabels(plotCmdStdHelp.SetBarDataLabels):
	pass

@serializationReg.registerForSerialization()
class SetTickMinorValsOnOrOff(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "set-tick-minor-vals-on-or-off"
		self._description = "Sets the minor tick values on/off. The axis to apply to is that which should be showing numerical data (where the height of bars matters)"
		self._optName = "showMinorTickMarkers"

	def execute(self, plotterInstance):
		minorTicksOn = getattr(plotterInstance.opts, self._optName).value
		plotHoz = getattr(plotterInstance.opts, "plotHorizontally").value

		useAx = plt.gca().xaxis if plotHoz else plt.gca().yaxis
		self._applyToAxis(useAx, minorTicksOn)

	def _applyToAxis(self, inpAxis, minorTickOn):
		if minorTickOn is False:
			inpAxis.set_minor_locator( matplotlib.ticker.AutoMinorLocator(n=1) )
		elif minorTickOn is True:
			inpAxis.set_minor_locator( matplotlib.ticker.AutoMinorLocator() )



@serializationReg.registerForSerialization()
class SetTickValsToGroupCentres(plotCmdStdHelp.SetTickValsToGroupCentres):
	pass
		
@serializationReg.registerForSerialization()
class SetTickLabelsToGroupLabels(plotCmdStdHelp.SetTickLabelsToGroupLabels):
	pass


def _doesPlotterInstanceHaveData(plotterInstance):
	targVal = getattr(plotterInstance.opts, "plotData1D").value
	if targVal is None:
		return False
	elif len(targVal)==0:
		return False
	return True


