

from ...core import plotters as plotterCoreHelp
from ...core import plot_options as plotOptCoreHelp
from .. import plot_options as plotOptStdHelp
from .. import plot_commands as plotCmdStdHelp

class LinePlotter(plotterCoreHelp.SingleGraphPlotter):

	def __init__(self, **kwargs):
		""" Initializer
		
		Args:
			kwargs: keys are strs in [x.name for x in LinePlotter().opts]. Values are the values you want to set them to
				 
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





#Less indenting required this way
def _createCommandsList():
	outList = [
	plotCmdStdHelp.CreateFigureIfNoAxHandle(),
	plotCmdStdHelp.PlotDataAsLines(),
	plotCmdStdHelp.SetDataLabels(),
	plotCmdStdHelp.SetLineColors(),
	plotCmdStdHelp.SetLineMarkerStyles(),
	plotCmdStdHelp.SetXLabelStr(),
	plotCmdStdHelp.SetYLabelStr(),
	plotCmdStdHelp.SetXLimit(),
	plotCmdStdHelp.SetYLimit(),
	plotCmdStdHelp.SetAxisColorX(), #Best if done after labels etc. set
	plotCmdStdHelp.SetAxisColorY(),
	plotCmdStdHelp.SetLegendLocStr(),
	plotCmdStdHelp.SetLegendFractPosStart(),
	plotCmdStdHelp.SetLegendNumberColumns(),
	plotCmdStdHelp.TurnLegendOnIfRequested()
	]

	return outList

#Write in alphabetical order
def _createOptionsList():
	outList = [
	plotOptStdHelp.AxisColorX(),
	plotOptStdHelp.AxisColorX_exclSpines(),
	plotOptStdHelp.AxisColorY(),
	plotOptStdHelp.AxisColorY_exclSpines(),
	plotOptStdHelp.DataLabels(),
	plotOptStdHelp.LegendFractPosStart(),
	plotOptStdHelp.LegendLocStr(),
	plotOptStdHelp.LegendNumbCols(),
	plotOptStdHelp.LegendOn(),
	plotOptStdHelp.LineColors(),
	plotOptStdHelp.LineMarkerStyles(),
	plotOptStdHelp.PlotData2D(),
	plotOptStdHelp.SetFigsizeOnCreation(),
	plotOptStdHelp.XLabelStr(),
	plotOptStdHelp.YLabelStr(),
	plotOptStdHelp.XLimit(),
	plotOptStdHelp.YLimit()

	]
	return outList

