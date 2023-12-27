

import types

from . import shared

from ...core import plotters as plotterCoreHelp
from ...core import plot_options as plotOptCoreHelp
from ...core.serialization import register as serializationReg

from .. import plot_options as plotOptStdHelp
from .. import plot_commands as plotCmdStdHelp


@serializationReg.registerForSerialization()
class LinePlotter(shared.FromJsonMixin, shared.FromPlotterMixin, plotterCoreHelp.SingleGraphPlotter):

	def __init__(self, **kwargs):
		""" Initializer
		
		Args:
			kwargs: keys are strs in "LinePlotter().optionNames". Values are the values you want to set them to
				 
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
	plotCmdStdHelp.AddPlotterToOutput(),
	plotCmdStdHelp.PlotDataAsLines(),
	plotCmdStdHelp.GridLinesCreate(),
	plotCmdStdHelp.SetDataLabels(),
	plotCmdStdHelp.SetLineAlpha(),
	plotCmdStdHelp.SetLineColors(),
	plotCmdStdHelp.SetLineMarkerSizes(),
	plotCmdStdHelp.SetLineMarkerStyles(),
	plotCmdStdHelp.SetLineStyles(),
	plotCmdStdHelp.SetLineThickness(),
	plotCmdStdHelp.SetLineErrorBarColors(),
	plotCmdStdHelp.SetXLabelStr(),
	plotCmdStdHelp.SetYLabelStr(),
	plotCmdStdHelp.SetAxisScaleX(),
	plotCmdStdHelp.SetAxisScaleY(),
	plotCmdStdHelp.SetTickMarkerValues(),
	plotCmdStdHelp.SetTickLabelValues(),
	plotCmdStdHelp.SetTickLabelFontSize(),
	plotCmdStdHelp.SetAxisTickAndLabelVisibilitiesEachSide(),
	plotCmdStdHelp.SetTickMinorMarkersOn(),
	plotCmdStdHelp.SetTickLabelRotations(),
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
	plotCmdStdHelp.SetLegendHandlesToPlottedLinesDefault(),
	plotCmdStdHelp.PlotHozAndVertLines(),
	plotCmdStdHelp.TurnLegendOnIfRequested(),
	plotCmdStdHelp.DrawShadedAnnotationsGeneric(),
	plotCmdStdHelp.DrawTextAnnotationsGeneric()
	]

	return outList

#Write in alphabetical order
def _createOptionsList():
	outList = [
	plotOptStdHelp.AnnotationsShadedGeneric(),
	plotOptStdHelp.AnnotationsTextGeneric(),
	plotOptStdHelp.AxisBorderMakeInvisible(),
	plotOptStdHelp.AxisColorX(),
	plotOptStdHelp.AxisColorX_exclSpines(),
	plotOptStdHelp.AxisColorY(),
	plotOptStdHelp.AxisColorY_exclSpines(),
	plotOptStdHelp.AxisScaleX(),
	plotOptStdHelp.AxisScaleY(),
	plotOptStdHelp.DataLabels(),
	plotOptStdHelp.ErrorBarCapsize(),
	plotOptStdHelp.ErrorBarColors(),
	plotOptStdHelp.ErrorBarColorsMatchLinesByDefault(value=True),
    plotOptStdHelp.ErrorBarDataX(),
    plotOptStdHelp.ErrorBarDataY(),
    plotOptStdHelp.ErrorBarLineMplHooks(),
	plotOptStdHelp.FontSizeDefault(),
	plotOptStdHelp.GridLinesShow(value=False),
	plotOptStdHelp.GridLinesShowX(),
	plotOptStdHelp.GridLinesShowY(),
	plotOptStdHelp.GridLinesStyle(),
	plotOptStdHelp.GridLinesWidth(),
	plotOptStdHelp.LegendFractPosStart(),
	plotOptStdHelp.LegendLocStr(),
	plotOptStdHelp.LegendNumbCols(),
	plotOptStdHelp.LegendOn(),
	plotOptStdHelp.LineAlpha(),
	plotOptStdHelp.LineColors(),
	plotOptStdHelp.LineMarkerSizes(),
	plotOptStdHelp.LineMarkerStyles(),
	plotOptStdHelp.LineStyles(),
	plotOptStdHelp.LineThickness(),
	plotOptStdHelp.PlotData2D(),
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
	plotOptStdHelp.TickLabelRotationX(),
	plotOptStdHelp.TickLabelRotationY(),
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

