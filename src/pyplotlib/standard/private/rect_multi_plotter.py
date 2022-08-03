
import itertools as it
import numpy as np
import matplotlib.pyplot as plt

from ...core import plotters as plotterCoreHelp
from ...core import plot_options as plotOptCoreHelp
from .. import plot_options as plotOptStdHelp
from .. import plot_commands as plotCmdStdHelp

from ...core import plot_command as plotCmdCoreHelp
from ...core.serialization import register as serializationReg

class RectMultiPlotter(plotterCoreHelp.MultiGraphPlotter):

	def __init__(self, **kwargs):
		self._createCommands()
		self._createOptions()
		self._scratchSpace = dict()
		self.setOptionVals(kwargs)

	def _createCommands(self):
		self._commands = _createCommandList()

	def _createOptions(self):
		_optionsList = _createOptionsList()
		self._options = plotOptCoreHelp.OptionsCollection(options=_optionsList)



def _createCommandList():
	outList = [
	CreateEmptyFigureIfNeeded(),
	FillPlottersToMatchGridCommand(),
	FillRowsToMatchPlottersCommand(),
	FillColsToMatchPlottersCommand(),
	CreateRectGridAndAxes(),
	SetHeightBasedOnNumberRows(),
	SetWidthBasedOnNumberCols(),
	PopulateAxesWithPlotters()

	]
	return outList

def _createOptionsList():
	outList = [

	ConstrainedLayout(),
	FillColsToMatchPlotters(),
	FillPlottersToMatchGrid(),
	FillRowsToMatchPlotters(),
	FigHeightPerRow(),
	FigWidthPerCol(),
	NColsGrid(),
	NRowsGrid(),
	plotOptStdHelp.PlotterIter(),
	RelGridHeights(),
	RelGridWidths(),
	plotOptStdHelp.SetFigsizeOnCreation()

	]
	return outList


#Options
@serializationReg.registerForSerialization()
class ConstrainedLayout(plotOptCoreHelp.BooleanPlotOption):
	""" Option for whether to use matplotlibs "constrained_layout" when creating the grid. This helps stop subplots overlapping; though is "experimental" at time of writing so may be removed (though seems unlikely)

	"""
	def __init__(self, name=None, value=None):
		self.name = "constrainedLayout"
		self.value = value


@serializationReg.registerForSerialization()
class FigHeightPerRow(plotOptCoreHelp.IntPlotOption):
	""" Sets the height of the figure as nRows*heightPerRow. This will likely override an absolute figure height

	"""
	def __init__(self, name=None, value=None):
		self.name = "figHeightPerRow"
		self.value = value

@serializationReg.registerForSerialization()
class FigWidthPerCol(plotOptCoreHelp.IntPlotOption):
	""" Sets the width of the figure as nCols*widthPerCol. This will likely override an absolute figure size

	"""
	def __init__(self, name=None, value=None):
		self.name = "figWidthPerCol"
		self.value = value


@serializationReg.registerForSerialization()
class FillColsToMatchPlotters(plotOptCoreHelp.BooleanPlotOption):
	""" If nRows*nGrid < nPlotters, setting this option to true will lead to columns being added until nRows*nGrid>= nPlotters. 

	"""
	def __init__(self, name=None, value=None):
		self.name = "fillColsToMatchPlotters"
		self.value = value


@serializationReg.registerForSerialization()
class FillPlottersToMatchGrid(plotOptCoreHelp.BooleanPlotOption):
	""" If nPlotters < nRows*nGrid, setting this option to True will add "None" to the plotters list; leading to empty axes.

	"""
	def __init__(self, name=None, value=None):
		self.name = "fillPlottersToMatchGrid"
		self.value = value

@serializationReg.registerForSerialization()
class FillRowsToMatchPlotters(plotOptCoreHelp.BooleanPlotOption):

	def __init__(self, name=None, value=None):
		self.name = "fillRowsToMatchPlotters"
		self.value = value


@serializationReg.registerForSerialization()
class NColsGrid(plotOptCoreHelp.IntPlotOption):
	""" Option for how many columns to have on a multiplot grid

	"""
	def __init__(self, name=None, value=None):
		self.name = "nColsGrid" if name is None else name
		self.value = value

@serializationReg.registerForSerialization()
class NRowsGrid(plotOptCoreHelp.IntPlotOption):
	""" Option for how many rows to have on a multiplot grid

	"""
	def __init__(self, name=None, value=None):
		self.name = "nRowsGrid" if name is None else name
		self.value = value

@serializationReg.registerForSerialization()
class RelGridHeights(plotOptCoreHelp.IntIterPlotOption):
	""" Option for relative heights of each subplot in a multi-plot grid. Values should be integers, where 1 is the default.

	For example, [1,2,1] would mean the 1st/3rd plot spanned 1 row each, whilst the second spanned 2 rows

	"""
	def __init__(self, name=None, value=None):
		self.name = "relGridHeights" if name is None else name
		self.value = value

@serializationReg.registerForSerialization()
class RelGridWidths(plotOptCoreHelp.IntIterPlotOption):
	""" Option for relative widths of each subplot in a multi-plot grid. Values should be integers, where 1 is the default


	"""
	def __init__(self, name=None, value=None):
		self.name = "relGridWidths" if name is None else name
		self.value = value













#Commands
class CreateEmptyFigureIfNeeded(plotCmdCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "create-empty-fig-if-needed"
		self._description = "Create an empty figure if axHandles are missing from the scratchSpace"
		self._constrainedLayoutAttr = "constrainedLayout"

	def execute(self, plotterInstance):
		#Check for axis handles; return if they are present
		try:
			plotterInstance._scratchSpace["ax_handles"]
		except KeyError:
			pass
		else:
			return None

		#Also check for a figure handle being present
		try:
			plotterInstance._scratchSpace["figHandle"]
		except KeyError:
			pass
		else:
			return None

		self._createFigure(plotterInstance)


	def _createFigure(self, plotterInstance):
		#Create the figure handle if required
		constrLayout = getattr(plotterInstance.opts, self._constrainedLayoutAttr).value
		figSize = getattr(plotterInstance.opts, "figSizeOnCreation").value

		plotterInstance._scratchSpace["figHandle"] = plt.figure(constrained_layout=constrLayout, figsize=figSize)



class CreateRectGridAndAxes(plotCmdCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "create-rect-grid-and-axes"
		self._description = "Creates a grid of empty axes and places handles in _scratchSpace[\"multi_axes\"]"
		self._nRowsAttr, self._nColsAttr = "nRowsGrid", "nColsGrid"
		self._relHeightAttr, self._relWidthAttr = "relGridHeights", "relGridWidths"
		self._plottersAttr = "plotters"

	def execute(self, plotterInstance):
		#Check if work has already been done; if so quit
		try:
			plotterInstance._scratchSpace["ax_handles"]
		except KeyError:
			pass
		else:
			return

		#Get the figure handle (this should be an empty figure)
		outFig = plotterInstance._scratchSpace["figHandle"]

		#Get options for creating the grid
		allPlotters = getattr(plotterInstance.opts, self._plottersAttr).value
		nRows, nCols = getattr(plotterInstance.opts, self._nRowsAttr).value, getattr(plotterInstance.opts, self._nColsAttr).value
#		relHeights, relWidths = self._getRelHeightsAndWidthArrays(plotterInstance)		

		relHeights, relWidths = _getRelHeightsAndWidthArrays(plotterInstance)

		#Set sensible defaults here for now (though maybe putting in options is better?)
		nRows = 1 if nRows is None else nRows
		nCols = 1 if nCols is None else nCols
		allPlotters = list() if allPlotters is None else allPlotters

		#Create an array, which tracks which grid positions we've used already
		trackingArray = np.full( (nRows,nCols), False, dtype="bool")

		#Check we'll have AT LEAST enough axes for the plots. Another option/command can handle
		#this situation better (e.g. setting nCol/nRow based on number of plotters; but if its got this far we need to throw an error
		if (nRows*nCols) < len(allPlotters):
			raise ValueError("Space for only {} plotters; but {} given".format( nRows*nCols, len(allPlotters)))

		#Create the axes for each plotter
		outAxes = list()
#		outFig = plt.figure()
		gridSpec = outFig.add_gridspec(nRows, nCols)

		currRow, currCol = 0, 0
		for idx, unused in enumerate(allPlotters):
			#If this bit is occupied, move columns until we find one free
			try:
				if trackingArray[currRow][currCol]:
					while trackingArray[currRow][currCol]:
						currCol += 1 
						if currCol >= nCols:
							currCol = 0
							currRow +=1
			except IndexError:
				raise ValueError("Inconsistent relative widths/heights detected")


			#Figure out the grid-spec slices needed + if valid
			#Note: >1 width means we span COLUMNS, whilst >1 height means we span ROWS
			currWidth, currHeight = relWidths[idx], relHeights[idx]
			rowSlice = slice(currRow, currRow + currHeight )
			colSlice = slice(currCol, currCol + currWidth)

			if trackingArray[rowSlice,colSlice].any():
				raise ValueError("Inconsistent relative widths/heights detected")

			#Update entries in tracking array for later
			trackingArray[rowSlice,colSlice] = True

			#Create subplot
			currAx = outFig.add_subplot(gridSpec[rowSlice,colSlice])
			outAxes.append(currAx)

			#Update current row and column
			currCol += currWidth
			if currCol >= nCols:
				currCol = 0
				currRow += 1


		#Add the axes to the scratch space
		plotterInstance._scratchSpace["ax_handles"] = outAxes



class FillPlottersToMatchGridCommand(plotCmdCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "fill-plotters-to-match-grid"
		self._description = "Adds None to plotters such that there is one entry per nRows*nCols"
		self._optionAttr = "fillPlottersToMatchGrid"

	def execute(self, plotterInstance):
		if getattr(plotterInstance.opts, self._optionAttr).value is not True:
			return None

		nRows, nCols, nPlotters = _getNRowsAndColsAndEffectiveNumbPlotters(plotterInstance)

		if nPlotters >= (nRows*nCols):
			return None

		if nPlotters == 0:
			outPlotters = list()
		else:
			outPlotters = getattr(plotterInstance.opts,"plotters").value

		#Add until we fill the grid
		keepAdding = True
		effPlotters = nPlotters
		while keepAdding:
			#Add
			extraPlotters = [None for x in range((nRows*nCols)-effPlotters)]
			outPlotters.extend(extraPlotters)
			getattr(plotterInstance.opts,"plotters").value = outPlotters

			#Check if we have enough to fill the grid
			_unused, _unused, effPlotters = _getNRowsAndColsAndEffectiveNumbPlotters(plotterInstance)
			if effPlotters >= (nRows*nCols):
				keepAdding = False



class FillColsToMatchPlottersCommand(plotCmdCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "fill-cols-to-match-plotters"
		self._description = "Can modify the nColsGrid option such that we have enough rows/columns to accomodate all the plotters"
		self._nRowsAttr, self._nColsAttr = "nRowsGrid", "nColsGrid"
		self._plottersAttr = "plotters"
		self._optionAttr = "fillColsToMatchPlotters"
		self._relHeightAttr, self._relWidthAttr = "relGridHeights", "relGridWidths"


	def execute(self, plotterInstance):
		if getattr(plotterInstance.opts,self._optionAttr).value is not True:
			return None

		nRows, nCols, nPlotters = _getNRowsAndColsAndEffectiveNumbPlotters(plotterInstance)

		outRows, outCols = _getOutputNRowsAndCols(nRows, nCols, nPlotters, colsConstant=False)

		getattr(plotterInstance.opts, self._nColsAttr).value = outCols


class FillRowsToMatchPlottersCommand(FillColsToMatchPlottersCommand):

	def __init__(self):
		super().__init__()
		self._name = "fill-rows-to-match-plotters"
		self._description = "Can modify the nRowsGrid option such that we have enough rows/columns to accomodate all the plotters"
		self._optionAttr = "fillRowsToMatchPlotters"

	def execute(self, plotterInstance):
		if getattr(plotterInstance.opts,self._optionAttr).value is not True:
			return None

		nRows, nCols, nPlotters = _getNRowsAndColsAndEffectiveNumbPlotters(plotterInstance)
		outRows, outCols = _getOutputNRowsAndCols(nRows, nCols, nPlotters, colsConstant=True)

		getattr(plotterInstance.opts, self._nRowsAttr).value = outRows



class PopulateAxesWithPlotters():

	def __init__(self):
		self._name = "populate-axes-with-plotters"
		self._description = "Add plots to axes by calling plotter(axHandle) for each"
		self._axesKey = "ax_handles"
		self._plottersKey = "plotters"

	def execute(self, plotterInstance):
		plotters = getattr(plotterInstance.opts, self._plottersKey).value
		if plotters is None:
			return None

		axHandles = plotterInstance._scratchSpace[self._axesKey]

		for currAx, currPlotter in zip(axHandles, plotters):
			if currPlotter is not None:
				currPlotter.createPlot(currAx)


class SetHeightBasedOnNumberRows():

	def __init__(self):
		self._name = "set-fig-height-based-on-nRows"
		self._description = "Sets the figure height to nRows*heightPerRow"
		self._figKey = "figHandle"
		self._sizeAttr = "figHeightPerRow"

	def execute(self, plotterInstance):
		sizeVal = getattr(plotterInstance.opts, self._sizeAttr).value
		if sizeVal is None:
			return None

		nRows, nCols, unused = _getNRowsAndColsAndEffectiveNumbPlotters(plotterInstance)
		figHandle = plotterInstance._scratchSpace[self._figKey]
		outHeight = nRows*sizeVal
		figHandle.set_figheight(outHeight)

class SetWidthBasedOnNumberCols():

	def __init__(self):
		self._name = "set-fig-width-based-on-nCols"
		self._description = "Sets the figure width to nCols*widthPerCol"
		self._figKey = "figHandle"
		self._sizeAttr = "figWidthPerCol"	

	def execute(self, plotterInstance):
		sizeVal = getattr(plotterInstance.opts, self._sizeAttr).value
		if sizeVal is None:
			return None

		nRows, nCols, unused = _getNRowsAndColsAndEffectiveNumbPlotters(plotterInstance)
		figHandle = plotterInstance._scratchSpace[self._figKey]
		outWidth = nCols*sizeVal
		figHandle.set_figwidth(outWidth)



def _getNRowsAndColsAndEffectiveNumbPlotters(plotterInstance, _nRowsAttr="nRowsGrid", _nColsAttr="nColsGrid"):
	nRows, nCols = [getattr(plotterInstance.opts, attrName).value for attrName in [_nRowsAttr, _nColsAttr]]
	nRows = 1 if nRows is None else nRows
	nCols = 1 if nCols is None else nCols 
	totalGrids = nRows*nCols

	nPlotters = _getEffectiveNumberPlotters(plotterInstance)

	return nRows, nCols, nPlotters

def _getEffectiveNumberPlotters(plotterInstance, _plottersAttr="plotters"):
	plotters = getattr(plotterInstance.opts,_plottersAttr).value
	nPlotters = len(plotters) if plotters is not None else 0

	#Need to account for any 2x width or height
	relWidths, relHeights = _getRelHeightsAndWidthArrays(plotterInstance)
	totalArea = sum( [width*height for width,height in it.zip_longest(relWidths, relHeights)] )

	return totalArea


def _getRelHeightsAndWidthArrays(plotterInstance, _relHeightAttr="relGridHeights",
                                 _relWidthAttr="relGridWidths", _plottersAttr="plotters"):

	_relHeights = getattr(plotterInstance.opts, _relHeightAttr).value
	_relWidths = getattr(plotterInstance.opts, _relWidthAttr).value

	def _getFinalArrayForHeightOrWidth(inpArray):
		outArray = list() if inpArray is None else inpArray
		for idx, val in enumerate(outArray):
			outArray[idx] = val if val is not None else 1

		plotters = getattr(plotterInstance.opts, _plottersAttr).value
		if plotters is None:
			plotters = list()

		nPlotters = len(plotters)
		if len(outArray) < nPlotters:
			extraVals = [1 for x in range(nPlotters-len(outArray))]
			outArray.extend(extraVals)
		return outArray

	outHeights = _getFinalArrayForHeightOrWidth(_relHeights)
	outWidths = _getFinalArrayForHeightOrWidth(_relWidths)
	return outHeights, outWidths



def _getOutputNRowsAndCols(nRows, nCols, nPlotters, colsConstant=False):
	if nPlotters <= nRows*nCols:
		return nRows, nCols

	outNRows, outNCols = nRows, nCols

	while nPlotters>(outNRows*outNCols):
		if colsConstant:
			outNRows += 1
		else:
			outNCols += 1

	return outNRows, outNCols

