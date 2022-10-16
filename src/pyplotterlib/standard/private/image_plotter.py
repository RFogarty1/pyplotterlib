
import types

import matplotlib.pyplot as plt

from . import shared

from .. import plot_options as plotOptStdHelp
from .. import plot_commands as plotCmdStdHelp

from ...core import plotters as plotterCoreHelp
from ...core import plot_command as plotCmdCoreHelp
from ...core import plot_options as plotOptCoreHelp

from ...core.serialization import register as serializationReg

@serializationReg.registerForSerialization()
class ImagePlotter(shared.FromJsonMixin, plotterCoreHelp.SingleGraphPlotter):

	def __init__(self, **kwargs):
		""" Initializer
		
		Args:
			kwargs: keys are strs in [x.name for x in ImagePlotter().opts]. Values are the values you want to set them to
				 
		"""
		self._createCommands()
		self._createOptions()
		self._scratchSpace = {"plotKwargs":{}}
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
	SetAspectStr(),
	SetColormap(),
	AddImageToPlot(),
	AddColorBar(),
	plotCmdStdHelp.SetXLabelStr(),
	plotCmdStdHelp.SetYLabelStr(),
	plotCmdStdHelp.SetTickLabelFontSize(),
	plotCmdStdHelp.SetAxisTickAndLabelVisibilitiesEachSide(),
	plotCmdStdHelp.SetXLabelFractPos(),
	plotCmdStdHelp.SetYLabelFractPos(),
	plotCmdStdHelp.SetXLimit(),
	plotCmdStdHelp.SetYLimit(),
	plotCmdStdHelp.SetAxisColorX(), #Best if done after labels etc. set
	plotCmdStdHelp.SetAxisColorY(),
	plotCmdStdHelp.SetTitleStr()
	]

	return outList


#Write in alphabetical order
def _createOptionsList():
	outList = [
	AspectString(),
	plotOptStdHelp.AxisColorX(),
	plotOptStdHelp.AxisColorX_exclSpines(),
	plotOptStdHelp.AxisColorY(),
	plotOptStdHelp.AxisColorY_exclSpines(),
	ColorBarShow(),
	ColormapStr(),
	plotOptStdHelp.FontSizeDefault(),
	PlotDataImage(),
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
class AspectString(plotOptCoreHelp.StringPlotOption):
	""" String controlling how the image aspect works

	equal: Pixels kept square; aspect ratio is maintained but axes may not fill the space
	auto: Aspect ratio is altered such that the image fits the axes; may be useful when creating grids of images

	"""
	def __init__(self, name=None, value=None):
		self.name = "aspectStr"
		self.value = value

@serializationReg.registerForSerialization()
class ColormapStr(plotOptCoreHelp.StringPlotOption):
	""" String representing the color map to use. These correspond to matplotlib color maps, which are described here:

	https://matplotlib.org/stable/tutorials/colors/colormaps.html

	"""
	def __init__(self, name=None, value=None):
		self.name = "colorMapStr"
		self.value = value

@serializationReg.registerForSerialization()
class PlotDataImage(plotOptCoreHelp.NumpyArrayPlotOption):
	""" Numpy representation of an image. The allowed formats are those allowed by matplotlibs plt.imshow

	For grayscale images this will be an NxM matrix, with each value representing intensity at one pixel. 

	For color images this will be an NxMx3 (RGB) or NxMx4 (RGBA) matrix. N/M represnt pixel indices, whilst the vector represents RGB or RGBA values for that pixel

	"""
	def __init__(self, name=None, value=None):
		self.name = "plotDataImage"
		self.value = value

@serializationReg.registerForSerialization()
class ColorBarShow(plotOptCoreHelp.BooleanPlotOption):
	""" Whether to show a colorbar; True=Show it, False=Dont show it

	"""
	def __init__(self, name=None, value=None):
		self.name = "colorBarShow"
		self.value = value

#Commands
@serializationReg.registerForSerialization()
class AddImageToPlot(plotCmdCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "add-image-to-plot"
		self._description = "Adds the image to the current axis"
		self._plotDataAttr = "plotDataImage"

	def execute(self, plotterInstance):
		data = plotCmdStdHelp._getValueFromOptName(plotterInstance, self._plotDataAttr)
		if data is None:
			return None
		else:
			plt.imshow(data, **plotterInstance._scratchSpace["plotKwargs"])

@serializationReg.registerForSerialization()
class AddColorBar(plotCmdCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "add-color-bar"
		self._description = "Adds a color bar to the plot"
		self._showAttr = "colorBarShow"

	def execute(self, plotterInstance):
		toShow = plotCmdStdHelp._getValueFromOptName(plotterInstance, self._showAttr)
		if toShow is True:
			plt.colorbar()
		


@serializationReg.registerForSerialization()
class SetAspectStr(plotCmdCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "set-aspect-str"
		self._description = "Sets the aspect string for the axis"
		self._optName = "aspectStr"

	def execute(self, plotterInstance):
		aspectStr = plotCmdStdHelp._getValueFromOptName(plotterInstance, self._optName)
		if aspectStr is None:
			return None
		else:
			plotterInstance._scratchSpace["plotKwargs"]["aspect"] = aspectStr

@serializationReg.registerForSerialization()
class SetColormap(plotCmdCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "set-color-map"
		self._description = "Sets the color map to use"
		self._optName = "colorMapStr"

	def execute(self, plotterInstance):
		colorMapStr = plotCmdStdHelp._getValueFromOptName(plotterInstance, self._optName)
		if colorMapStr is None:
			return None
		else:
			plotterInstance._scratchSpace["plotKwargs"]["cmap"] = colorMapStr

