
from . import shared

from .. import plot_options as plotOptStdHelp
from .. import plot_commands as plotCommStdHelp

from ...core import plot_command as plotCommCoreHelp
from ...core import plotters as plotterCoreHelp
from ...core import plot_options as plotOptCoreHelp
from ...core.serialization import register as serializationReg


@serializationReg.registerForSerialization()
class DoubleAxisPlotter(shared.FromJsonMixin, plotterCoreHelp.SingleGraphPlotter):
	""" Plotter which creates a plot from a single axis handle, but can have 2 independent x XOR y axes

	"""

	#Likely a commmon init signature really
	def __init__(self, **kwargs):
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
	CheckMaxThreeAxes(),
	plotCommStdHelp.CreateFigureIfNoAxHandle(),
	GenerateSecondAxisForPlotting(),
	CheckAxesAndPlottersConsistent(),
	PopulateAxesWithPlotters()

	]
	return outList

def _createOptionsList():
	outList = [

	AllowTwoIndependentAxes(),
	plotOptStdHelp.PlotterIter(),
	IndependentXAxis(),
	IndependentYAxis()

	]
	return outList


#These commands/options are only really EVER needed here

@serializationReg.registerForSerialization()
class AllowTwoIndependentAxes(plotOptCoreHelp.BooleanPlotOption):

	def __init__(self, name=None, value=None):
		self.name = "allowTwoIndependentAxes" if name is None else name
		self.value = value

#allowTwoIndependentAxes

@serializationReg.registerForSerialization()
class IndependentYAxis(plotOptCoreHelp.BooleanPlotOption):

	def __init__(self, name=None, value=None):
		self.name = "independentYAxis" if name is None else name
		self.value = value

@serializationReg.registerForSerialization()
class IndependentXAxis(plotOptCoreHelp.BooleanPlotOption):

	def __init__(self, name=None, value=None):
		self.name = "independentXAxis" if name is None else name
		self.value = value


@serializationReg.registerForSerialization()
class GenerateSecondAxisForPlotting(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "generate-second-axis"
		self._description = "Create a second axis for shared-axis plotting"
		self._independentX_key = "independentXAxis"
		self._independentY_key = "independentYAxis"

	def execute(self, plotterInstance):
		newX = getattr(plotterInstance.opts, self._independentX_key).value
		newY = getattr(plotterInstance.opts, self._independentY_key).value
		startAxis = plotterInstance._scratchSpace["axHandle"]
		secondAxis = startAxis.twiny() if newX else startAxis
		thirdAxis = secondAxis.twinx() if newY else secondAxis
		plotterInstance._scratchSpace["shared_axes_second_axis"] = thirdAxis



@serializationReg.registerForSerialization()
class PopulateAxesWithPlotters(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "plot-on-all-axes"
		self._description = "Create plots on main and shared axis"
		self._plottersKey = "plotters"

	def execute(self, plotterInstance):
		targVal = getattr(plotterInstance.opts, self._plottersKey).value
		if targVal is None:
			return None
		targVal[0].createPlot(axHandle=plotterInstance._scratchSpace["axHandle"])
		if len(targVal)>1:
			targVal[1].createPlot(axHandle=plotterInstance._scratchSpace["shared_axes_second_axis"])


@serializationReg.registerForSerialization()
class CheckAxesAndPlottersConsistent(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "check-axes-and-plotters-consistent"
		self._description = "Checks that if we have 2 plotters, we also have two separate axes to plot on; else raises ValueError"
	
	def execute(self, plotterInstance):
		axA, axB = plotterInstance._scratchSpace["axHandle"], plotterInstance._scratchSpace["shared_axes_second_axis"]
		numbPlotters = len(plotterInstance.opts.plotters.value)
		singleAxis = True if axA is axB else False
		if (numbPlotters > 1) and (singleAxis):
			raise ValueError("Cant plot >1 plotter when independentXAxis/independentYAxis are both False")


@serializationReg.registerForSerialization()
class CheckMaxThreeAxes(plotCommCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "check-max-three-axes"
		self._description = "Check that we twin both x AND y axes; since i cant guarantee that working"
		self._indepXOpt = "independentXAxis"
		self._indepYOpt = "independentYAxis"
		self._allowOpt = "allowTwoIndependentAxes"

	def execute(self, plotterInstance):
		indepX = getattr(plotterInstance.opts, self._indepXOpt).value
		indepY = getattr(plotterInstance.opts, self._indepYOpt).value
		allowTwoIndeps = getattr(plotterInstance.opts, self._allowOpt).value

		if not(allowTwoIndeps):
			if (indepX and indepY):
				msg = "Independent x AND y axes are currently not supported; if you want to use them regardless you can supress this error by setting 'allowTwoIndependentAxes' to True but results may be unpredictable"
				raise ValueError(msg)
