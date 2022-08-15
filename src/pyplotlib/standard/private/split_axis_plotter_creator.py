
import copy

from ...core import plotters as plotterCoreHelp
from ...core import plot_options as plotOptCoreHelp
from ...core import plot_command as plotCmdCoreHelp
from ...core.serialization import register as serializationReg

from .line_plotter import LinePlotter
from . import split_axis_plotter as splitAxisPlotterHelp

class SplitAxisPlotterCreator(plotterCoreHelp.SingleGraphPlotter):
	""" Goal is to create a split-axis plotter, with reasonable values, from a single plotter instance. Alternatively this can directly generate plots.

	Note: This is tested on the LinePlotter class; it should work on others but it isnt gauranteed

	"""
	def __init__(self, **kwargs):
		self._createCommands()
		self._createOptions()
		self._scratchSpace = dict()
		self.setOptionVals(kwargs)

	def createPlot(self, axHandle=None, **kwargs):
		plotter = self.createPlotter(**kwargs)
		return plotter.createPlot(axHandle)

	def createPlotter(self, **kwargs):
		""" Creates a SplitAxisPlotter based on current options
		
		Args:
			kwargs: Names are those in self.opts, values are the values you want to set (they override current values for this function call)

		Returns
			plotter (SplitAxisPlotter):
		
		"""
		useFactory = self.createFactory(**kwargs)
		useFactory._scratchSpace["outDict"] = dict()

		for command in self.commands:
			command.execute(useFactory)

		return useFactory._scratchSpace["outPlotter"]


	def _createCommands(self):
		self._commands = _createCommandList()

	def _createOptions(self):
		_optionsList = _createOptionsList()
		self._options = plotOptCoreHelp.OptionsCollection(options=_optionsList)


#TODO: Make the "blankOutputPlotter" contain the plotter grid we create
def _createCommandList():
	outList = [

	StorePlotterGridDimensions(),
	StoreTemplatePlotter(),
	CreatePlotterGrid(),
	CreateBlankOutputPlotter(),
	RemoveAxisLabels(),
	RemoveInternalAxes(),
	RemoveLegends(),
	SetAxisLimits(),
	SetAxesRelativeWidthsAndHeights(),
	SetSpacingXY(),
	SetAxisLabelPositions(), #MUST come after we set the spacing values
	SetSplitLineDrawOpts(),

	AddPlotterGridToOutputPlotter()

	]
	return outList

def _createOptionsList():
	outList = [
	AxisSizeLinear(),
	LegendPlotterGridCoords(),
	PlotterOpt(),
	SplitLinesAngle(),
	SplitLinesDraw(),
	SplitLinesLength(),
	XLimits(),
	YLimits(),
	XLabelOffset(value=-0.1),
	YLabelOffset(value=-0.1),
	XSpacingFract(),
	YSpacingFract()

	]
	return outList


#Options
@serializationReg.registerForSerialization()
class AxisSizeLinear(plotOptCoreHelp.BooleanPlotOption):
	""" Boolean for specifying if split axis width/heights should depend linearly on the x/y limits. If True they will, if False all axes will be equal width/height.

	For example, if you have xLimits = [ [1,10], [100,200] ], then setting to True will mean the second column will be 10x wider than the first.  Setting to False means they'll be the same width

	For finer control of the sizes of axes, you'll need to directly interact with the lower-level split axis plotter

	"""
	def __init__(self, name=None, value=None):
		self.name = "axisSizeLinear"
		self.value = True if value is None else value

@serializationReg.registerForSerialization()
class LegendPlotterGridCoords(plotOptCoreHelp.IntIterPlotOption):
	""" Which plotter to display the legend on (assuming its turned on in the template plotter). [xIdx,yIdx].

	 For example, [0,0] will put the legend on in the first plotter (bottom left), [2,1] will put it on the plotter which shows the third x-limit values and second y-limit values

	Default is for the legend to be placed in the [0,0] position

	"""
	def __init__(self, name=None, value=None):
		self.name = "legendPlotterGridCoords"
		self.value = value

@serializationReg.registerForSerialization()
class PlotterOpt(plotOptCoreHelp.JsonTransObjPlotOption):
	""" Option for specifying a plotter object to use as the template

	"""
	def __init__(self, name=None, value=None):
		self.name = "plotter"
		self.value = value

@serializationReg.registerForSerialization()
class SplitLinesAngle(plotOptCoreHelp.FloatPlotOption):
	""" The angle (in degrees) at which to draw lines marking axis splits. Default is 45.

	90 degrees will point along the relevant axis. 0 degrees will be orthogonal

	"""
	def __init__(self, name=None, value=None):
		self.name = "splitLinesAngle"
		self.value = value

@serializationReg.registerForSerialization()
class SplitLinesDraw(plotOptCoreHelp.BooleanPlotOption):
	""" Whether to draw lines marking the axis split or not (True means draw them, False means dont)

	"""
	def __init__(self, name=None, value=None):
		self.name = "splitLinesDraw"
		self.value = True if value is None else value

@serializationReg.registerForSerialization()
class SplitLinesLength(plotOptCoreHelp.FloatPlotOption):
	""" The Length to draw the lines marking axis splits. These are relative to the size of the overall plot, so values around 0.1 are generally sensible

	"""
	def __init__(self, name=None, value=None):
		self.name = "splitLinesLength"
		self.value = value

@serializationReg.registerForSerialization()
class XLabelOffset(plotOptCoreHelp.FloatPlotOption):
	""" Float representing the fractional distance of the x-label from the x-axis. Setting this to -0.1 (for example) should end up with the xlabel having a similar y-position whether the axis is split or not. 

	"""
	def __init__(self, name=None, value=None):
		self.name = "xLabelOffset"
		self.value = value


@serializationReg.registerForSerialization()
class XLimits(plotOptCoreHelp.IterOfFloatIterPlotOption):
	""" The x-limits for each axis. An iter of len-2 floats, e.g. [ [1,10], [50,60] ] would be for an axis with a single split. [ [1,10] ] would be for an axis with NO splits

	"""
	def __init__(self, name=None, value=None):
		self.name = "xLimits"
		self.value = value

@serializationReg.registerForSerialization()
class XSpacingFract(plotOptCoreHelp.FloatPlotOption):
	""" Float representing the width of the gap between two parts of a split x-axes. This should generally be a small (e.g. 0.05) number, and likely chosen by experimenting with a few values.

	The total width is width-axis + (XSpacingAbs*number-of-splits). The value of width-axis is set to 1, meaning the fraction of width taken up by these spaces is [(XSpacingAbs*numb-of-splits)] / [1 + (XSpacingAbs*numb-of-splits)]

	If not set, then it will use the default spacingX option defined as part of the SplitAxisPlotter

	Note: xSpacingFract is passed directly to SplitAxisPlotter as the xSpacing option

	"""
	def __init__(self, name=None, value=None):
		self.name = "xSpacingFract"
		self.value = value 

@serializationReg.registerForSerialization()
class YLabelOffset(plotOptCoreHelp.FloatPlotOption):
	""" Float representing the fractional distance of the y-label from the y-axis. Setting this to -0.1 (for example) should end up with the ylabel having a similar x-position whether the axis is split or not. 

	"""
	def __init__(self, name=None, value=None):
		self.name = "yLabelOffset"
		self.value = value


@serializationReg.registerForSerialization()
class YLimits(plotOptCoreHelp.IterOfFloatIterPlotOption):
	""" The y-limits for each axis. An iter of len-2 floats, e.g. [ [1,10], [50,60] ] would be for an axis with a single split. [ [1,10] ] would be for an axis with NO splits

	"""
	def __init__(self, name=None, value=None):
		self.name = "yLimits"
		self.value = value

@serializationReg.registerForSerialization()
class YSpacingFract(plotOptCoreHelp.FloatPlotOption):
	""" Float representing the width of the gap between two parts of a split y-axes. This should generally be a small (e.g. 0.05) number, and likely chosen by experimenting with a few values.

	The total width is width-axis + (YSpacingAbs*number-of-splits). The value of width-axis is set to 1, meaning the fraction of width taken up by these spaces is [(YSpacingAbs*numb-of-splits)] / [1 + (YSpacingAbs*numb-of-splits)]

	If not set, then it will use the default spacingY option defined as part of the SplitAxisPlotter

	Note: ySpacingFract is passed directly to SplitAxisPlotter as the ySpacing option

	"""
	def __init__(self, name=None, value=None):
		self.name = "ySpacingFract"
		self.value = value 



#Template commands
class ManipulatePlottersInGrid(plotCmdCoreHelp.PlotCommand):

	def execute(self, plotterInstance):
		plotterGrid = plotterInstance._scratchSpace["plotterGrid"]
		for rIdx, unused in enumerate(plotterGrid):
			for cIdx, unused in enumerate(plotterGrid[rIdx]):
				self._applyManipulation(plotterInstance, plotterGrid, rIdx, cIdx)

	def _applyManipulation(self, plotterInstance, plotterGrid, rowIdx, colIdx):
		raise NotImplementedError("")

#Commands
@serializationReg.registerForSerialization()
class AddPlotterGridToOutputPlotter(plotCmdCoreHelp.PlotCommand):
	
	def __init__(self):
		self._name = "add-plotter-grid-to-output-plotter"
		self._description = "Adds our grid of plotters to the output split axes plotter"

	def execute(self, plotterInstance):
		plotterInstance._scratchSpace["outPlotter"].opts.plotterGrid.value = plotterInstance._scratchSpace["plotterGrid"]


@serializationReg.registerForSerialization()
class CreateBlankOutputPlotter(plotCmdCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "create-blank-output-plotter"
		self._description = "Creates a blank plotter and places in 'outPlotter' scratchSpace"

	def execute(self, plotterInstance):
		plotterInstance._scratchSpace["outPlotter"] = splitAxisPlotterHelp.SplitAxisPlotter()

@serializationReg.registerForSerialization()
class RemoveAxisLabels(ManipulatePlottersInGrid):

	def __init__(self):
		self._name = "remove-axis-labels"
		self._description = "Removes labels on axes EXCEPT at plotterGrid[0][0]"

	def _applyManipulation(self, plotterInstance, plotterGrid, rowIdx, colIdx):
		currPlotter = plotterGrid[rowIdx][colIdx]
		if (rowIdx==0) and (colIdx==0):
			pass
		else:
			currPlotter.opts.xLabelStr.value = None
			currPlotter.opts.yLabelStr.value = None

	

@serializationReg.registerForSerialization()
class RemoveInternalAxes(ManipulatePlottersInGrid):

	def __init__(self):
		self._name = "remove-internal-axes"
		self._description = "Removes internal axes"

	def _applyManipulation(self, plotterInstance, plotterGrid, rowIdx, colIdx):
		numbRows = len(plotterGrid)
		numbCols = len(plotterGrid[rowIdx])
		currPlotter = plotterGrid[rowIdx][colIdx]
		axisVisOpts = currPlotter.opts.axisBorderMakeInvisible.value

		#1) Set all to be invisible
		for currAttr in axisVisOpts.__dict__:
			setattr(axisVisOpts, currAttr, True)

		#2) Add in axes to be visible
		if (rowIdx==0):
			axisVisOpts.left = False
		if (rowIdx==numbRows-1):
			axisVisOpts.right = False
		if (colIdx==0):
			axisVisOpts.bottom = False
		if (colIdx==numbCols-1):
			axisVisOpts.top = False

@serializationReg.registerForSerialization()
class RemoveLegends(ManipulatePlottersInGrid):

	def __init__(self):
		self._name = "remove-legends"
		self._description = "Removes legends from all plotters except the first"

	def _applyManipulation(self, plotterInstance, plotterGrid, rowIdx, colIdx):
		#Figure out where we can ALLOW the legend to be shown
		allowedPosition = plotterInstance.opts.legendPlotterGridCoords.value
		if allowedPosition is None:
			allowedPosition = [0,0]
		allowedRowIdx, allowedColIdx = allowedPosition

		#Remove the legend from anywhere else
		currPlotter = plotterGrid[rowIdx][colIdx]
		if not ( (rowIdx==allowedRowIdx) and (colIdx==allowedColIdx) ):
			currPlotter.opts.showLegend.value = False


#TODO: Maybe later add an option to override any label positions on the template plotter
@serializationReg.registerForSerialization()
class SetAxisLabelPositions(plotCmdCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "set-axis-label-position"
		self._description = "Sets the axis label positions IFF they arent already set by the template plotter"

	def execute(self, plotterInstance):
		self._setXLabelPosition(plotterInstance)
		self._setYLabelPosition(plotterInstance)

	def _setXLabelPosition(self, plotterInstance):
		templPlotter = plotterInstance._scratchSpace["templPlotter"]
		if templPlotter.opts.xLabelFractPos.value is not None:
			return None

		#Get the centre co-ordinate
		totalWidth, widthFirst = self._getRelevantWidthVals(plotterInstance)
		estimatedCentre = 0.5* ( totalWidth/widthFirst )

		#Get a co-ordinate that should be REASONABLY offset from the axis
		offSetVal =  plotterInstance.opts.xLabelOffset.value
		totalHeight, heightFirst = self._getRelevantHeightVals(plotterInstance)
		estimatedOffset = offSetVal * (totalHeight/heightFirst)

		fractCoords = [estimatedCentre, estimatedOffset]
		plotterGrid = plotterInstance._scratchSpace["plotterGrid"]
		plotterGrid[0][0].opts.xLabelFractPos.value = fractCoords

	def _setYLabelPosition(self, plotterInstance):
		templPlotter = plotterInstance._scratchSpace["templPlotter"]
		if templPlotter.opts.yLabelFractPos.value is not None:
			return None

		#Get the centre co-ordinate
		totalHeight, heightFirst = self._getRelevantHeightVals(plotterInstance)
		estimatedCentre = 0.5 * (totalHeight/heightFirst)

		#Get a co-ordinate that should be reasonably offset from the axis
		offSetVal = plotterInstance.opts.yLabelOffset.value
		totalWidth, widthFirst = self._getRelevantWidthVals(plotterInstance)
		estimatedOffset = offSetVal * (totalWidth/widthFirst)

		fractCoords = [estimatedOffset, estimatedCentre]
		plotterGrid = plotterInstance._scratchSpace["plotterGrid"]
		plotterGrid[0][0].opts.yLabelFractPos.value = fractCoords

	def _getRelevantWidthVals(self, plotterInstance):

		outPlotter = plotterInstance._scratchSpace["outPlotter"]
		numbSplitsX = plotterInstance._scratchSpace["numbX"] - 1
		fractPositionsX = outPlotter.opts.fractsX.value

		try:
			iter(fractPositionsX)
		except TypeError:
			fractPositionsX = [fractPositionsX for x in range(numbSplitsX+1)]

		spacingX = outPlotter.opts.spacingX.value

		#Figure out the total width + width of first plotter
		totalWidth = (numbSplitsX*spacingX) + sum(fractPositionsX)
		widthFirst = fractPositionsX[0]

		return totalWidth, widthFirst

	def _getRelevantHeightVals(self, plotterInstance):

		outPlotter = plotterInstance._scratchSpace["outPlotter"]
		numbSplitsY = plotterInstance._scratchSpace["numbY"] - 1
		fractPositionsY = outPlotter.opts.fractsY.value

		try:
			iter(fractPositionsY)
		except TypeError:
			fractPositionsY = [fractPositionsY for x in range(numbSplitsY+1)]

		spacingY = outPlotter.opts.spacingY.value

		#Figure out total height + height of first plotter		
		totalHeight = (numbSplitsY*spacingY) + sum(fractPositionsY)
		heightFirst = fractPositionsY[0]

		return totalHeight, heightFirst




@serializationReg.registerForSerialization()
class SetAxisLimits(ManipulatePlottersInGrid):

	def __init__(self):
		self._name = "set-axis-limits"
		self._description = "Sets limits on all axes"

	def _applyManipulation(self, plotterInstance, plotterGrid, rowIdx, colIdx):
		#Get limits
		_xLims = plotterInstance.opts.xLimits.value
		xLims = [None] if _xLims is None else _xLims

		_yLims = plotterInstance.opts.yLimits.value
		yLims = [None] if _yLims is None else _yLims
	
		#Set them
		currPlotter = plotterGrid[rowIdx][colIdx]
		currPlotter.opts.xLimit.value = xLims[rowIdx]
		currPlotter.opts.yLimit.value = yLims[colIdx]

@serializationReg.registerForSerialization()
class SetAxesRelativeWidthsAndHeights(plotCmdCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "set-axes-relative-widths-heights"
		self._description = "Sets the relative widths and heights of axes"

	#NOTE: This is currently hardcoded to "linear" mode
	def execute(self, plotterInstance):
		outPlotter = plotterInstance._scratchSpace["outPlotter"]

		#Get limits
		_xLims = plotterInstance.opts.xLimits.value
		xLims = [None] if _xLims is None else _xLims

		_yLims = plotterInstance.opts.yLimits.value
		yLims = [None] if _yLims is None else _yLims

		#Figure out the number of plots in each dimension
		numbX, numbY = len(xLims), len(yLims)
		averageX, averageY = 1/numbX, 1/numbY

		#Set vals and return early here if linear mode isnt turned on
		if plotterInstance.opts.axisSizeLinear.value is False:
			outPlotter.opts.fractsX.value = averageX
			outPlotter.opts.fractsY.value = averageY
			return None

		# Figure out the ranges for each
		def _getRanges(inpLims):
			outRanges = list()
			for idx in range(len(inpLims)):
				if inpLims[idx] is None:
					outRanges.append( None )
				else:
					outRanges.append( abs( inpLims[idx][0] - inpLims[idx][1] ) )
			return outRanges

		rangesX, rangesY = _getRanges(xLims), _getRanges(yLims)

		#Set the widths/heights accordingly
		#NOTE: doesnt work well if you mix "None" with values, but theres no reason/way it could 
		def _getFractValsFromRanges(inpRanges, avVal):
			total = sum([x for x in inpRanges if x is not None])
			outVals = list()
			for currRange in inpRanges:
				if currRange is None:
					outVals.append(avVal)
				else:
					outVals.append( currRange/total )
			return outVals		

		fractsX, fractsY = _getFractValsFromRanges(rangesX, averageX), _getFractValsFromRanges(rangesY, averageX)

		outPlotter.opts.fractsX.value = fractsX
		outPlotter.opts.fractsY.value = fractsY

@serializationReg.registerForSerialization()
class SetSpacingXY(plotCmdCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "set-xy-spacing"
		self._description = "Sets the spacing between split axes"

	def execute(self, plotterInstance):
		spacingX = plotterInstance.opts.xSpacingFract.value 
		spacingY = plotterInstance.opts.ySpacingFract.value

		if spacingX is not None:
			plotterInstance._scratchSpace["outPlotter"].opts.spacingX.value = spacingX
		if spacingY is not None:
			plotterInstance._scratchSpace["outPlotter"].opts.spacingY.value = spacingY


@serializationReg.registerForSerialization()
class SetSplitLineDrawOpts(plotCmdCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "set-split-line-draw-opts"
		self._description = "Sets the options for drawing lines that mark axis splits"

	def execute(self, plotterInstance):
		outPlotter = plotterInstance._scratchSpace["outPlotter"]
		drawLinesOptsX = outPlotter.opts.splitDrawDoubleLinesX.value[0]
		drawLinesOptsY = outPlotter.opts.splitDrawDoubleLinesY.value[0]

		#1) Turn them on or off
		if plotterInstance.opts.splitLinesDraw.value is True:
			drawLinesOptsX.draw = True
			drawLinesOptsY.draw = True

		#2) Set their lengths if requested
		length = plotterInstance.opts.splitLinesLength.value
		if length is not None:
			drawLinesOptsX.length = length
			drawLinesOptsY.length = length

		#3) Set their angles if requested
		angle = plotterInstance.opts.splitLinesAngle.value
		if angle is not None:
			drawLinesOptsX.angle = angle
			drawLinesOptsY.angle = angle

@serializationReg.registerForSerialization()
class StoreTemplatePlotter(plotCmdCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "store-template-plotter"
		self._description = "Stores the template plotter in 'templPlotter' key in scratchspace. This is usually a plotter input as an argument, but can also be a newly-created blank one" 

	def execute(self, plotterInstance):
		inputPlotter = plotterInstance.opts.plotter.value
		usePlotter = LinePlotter() if inputPlotter is None else inputPlotter
		plotterInstance._scratchSpace["templPlotter"] = usePlotter

@serializationReg.registerForSerialization()
class StorePlotterGridDimensions(plotCmdCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "store-plotter-grid-dimensions"
		self._description = "Uses lengths of xLimits and yLimits to figure out plotterGrid dimensions, and stores in scratchSpace under 'numbX' and 'numbY'"

	def execute(self, plotterInstance):
		xLims = getattr(plotterInstance.opts, "xLimits").value
		yLims = getattr(plotterInstance.opts, "yLimits").value

		plotterInstance._scratchSpace["numbX"] = 1 if xLims is None else len(xLims)
		plotterInstance._scratchSpace["numbY"]  = 1 if yLims is None else len(yLims)

@serializationReg.registerForSerialization()
class CreatePlotterGrid(plotCmdCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "create-grid-of-plotters"
		self._description = "Create a grid of plotters (all copies of the original) from the axis limits and store in 'plotterGrid' part of scratchSpace"

	def execute(self, plotterInstance):
		numbX, numbY = plotterInstance._scratchSpace["numbX"], plotterInstance._scratchSpace["numbY"]
		templPlotter = plotterInstance._scratchSpace["templPlotter"]
		outGrid = list()
		for xIdx in range(numbX):
			currList = list()
			for yIdx in range(numbY):
				currPlotter = copy.deepcopy(templPlotter)
				currList.append(currPlotter)
			outGrid.append(currList)

		plotterInstance._scratchSpace["plotterGrid"] = outGrid






