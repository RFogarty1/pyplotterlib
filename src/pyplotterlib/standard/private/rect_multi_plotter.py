
import itertools as it
import string

import numpy as np
import matplotlib.pyplot as plt

from . import shared

from ...core import plotters as plotterCoreHelp
from ...core import plot_options as plotOptCoreHelp
from .. import plot_options as plotOptStdHelp
from .. import plot_commands as plotCmdStdHelp

from ...core import plot_command as plotCmdCoreHelp
from ...core.serialization import register as serializationReg

@serializationReg.registerForSerialization()
class RectMultiPlotter(shared.FromJsonMixin,  shared.FromPlotterMixin, plotterCoreHelp.MultiGraphPlotter):
	""" MultiGraphPlotter which combines individual plotters into a rectangular grid

	"""
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
	PopulateAxesWithPlotters(),
	AddStringLabelAnnotations()

	]
	return outList

def _createOptionsList():
	outList = [

	AnnotateLabelFontSize(),
	AnnotateLabelPosFract(),
	AnnotateLabelStrings(),
	AnnotateLabelStringsBoldedLowerAlphabetDefault(),
	ConstrainedLayout(),
	FillColsToMatchPlotters(),
	FillPlottersToMatchGrid(),
	FillRowsToMatchPlotters(value=True),
	FigHeightPerRow(),
	FigWidthPerCol(),
	NColsGrid(),
	NRowsGrid(),
	plotOptStdHelp.PlotterIter(),
	RelGridHeights(),
	RelGridWidths(),
	plotOptStdHelp.SetFigsizeOnCreation(),
	SpacingHoz(),
	SpacingVert()

	]
	return outList


#Options
@serializationReg.registerForSerialization()
class AnnotateLabelFontSize(plotOptCoreHelp.IntOrIntIterPlotOption):
	""" The font sizes to use for annotation labels

	Example A: value=None; Will fall back on matplotlib defaults for font sizes
	Example B: value=12; Will set all annotation label font sizes to 12
	Example C: value = [10,12]; Will alternatingly set label font sizes to 10 and 12

	"""
	def __init__(self, name=None, value=None):
		self.name = "annotateLabelFontSize"
		self.value = value

@serializationReg.registerForSerialization()
class AnnotateLabelPosFract(plotOptCoreHelp.IterOfFloatIterPlotOption):
	""" The positions of annotation labels, expressed as fractional values for each subplot.

	Example A: [ [0.4,0.3] ] would put each annotation 40% along each x-axis and 30% along each y-axis
	Example B: [ [0.1,0.2], [0.1,0.3] ] would put 1st/3rd/5th etc. 10%/20% along x/y. It would then put 2nd/4th/6th at 10%/30% along x/y.

	"""
	def __init__(self, name=None, value=None):
		self.name = "annotateLabelPosFract"
		self.value = value

@serializationReg.registerForSerialization()
class AnnotateLabelStrings(plotOptCoreHelp.StringIterPlotOption):
	""" The strings to use as annotation labels. Setting a value of None for one entry will skip a plotter

	Example A: ["a)",None,"b)"] means 1st/3rd plotters have labels a) and b). 2nd has no annotation label 
	Example B: [r"$\bf{a)}$", r"$\bf{b)}$"] will have labels a) and b) but in bold

	"""
	def __init__(self, name=None, value=None):
		self.name = "annotateLabelStrings"
		self.value = value

@serializationReg.registerForSerialization()
class AnnotateLabelStringsBoldedLowerAlphabetDefault(plotOptCoreHelp.BooleanPlotOption):
	""" If True, annotateLabelStrings option will automatically be set to use bolded lowercase letters for each plot. [i.e. bolded a) b) c) d) etc.]

	"""
	def __init__(self, name=None, value=None):
		self.name = "annotateLabelStrings_useBoldedLowerAlphabetByDefault"
		self.value = value


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

	For example, [1,2,1] would mean the 1st/3rd plot spanned 1 col each, whilst the second spanned 2 cols

	"""
	def __init__(self, name=None, value=None):
		self.name = "relGridWidths" if name is None else name
		self.value = value


@serializationReg.registerForSerialization()
class SpacingHoz(plotOptCoreHelp.FloatPlotOption):
	""" Fractional value that controls horizontal spacing between plots. Corresponds to "wspace" in matplotlib. The value is relative to the width of the average plot.

	Typical values are around 0.1

	"""
	def __init__(self, name=None, value=None):
		self.name = "spacingHoz" if name is None else name
		self.value = value

@serializationReg.registerForSerialization()
class SpacingVert(plotOptCoreHelp.FloatPlotOption):
	""" Fractional value that controls vertical spacing between plots. Corresponds to "hspace" in matplotlib. The value if relative to the height of the average plot

	Typical values are around 0.1

	"""
	def __init__(self, name=None, value=None):
		self.name = "spacingVert" if name is None else name
		self.value = value

#Commands
@serializationReg.registerForSerialization()
class AddStringLabelAnnotations(plotCmdCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "add-string-label-annotations"
		self._description = "Add string-label annotations to each subplot (e.g. to label a,b,c)"
		self._userStrOptName = "annotateLabelStrings"
		self._userPosFractName = "annotateLabelPosFract"
		self._userFontOptName = "annotateLabelFontSize"

	def execute(self, plotterInstance):
		#Get default values
		useBoldedLowerAsDefault = plotCmdStdHelp._getValueFromOptName(plotterInstance, "annotateLabelStrings_useBoldedLowerAlphabetByDefault")
		defStrs = self._getDefaultLowerCaseBolded() if useBoldedLowerAsDefault else None

		#get user values
		userStrs = plotCmdStdHelp._getValueFromOptName(plotterInstance, self._userStrOptName)

		#figure out what to use based on user/def values 
		useStrs = userStrs if userStrs is not None else defStrs
		if useStrs is None:
			return None

		#Create the annotations
		cycledPositions = self._getAnnotationPositions(plotterInstance)
		axes = plotterInstance._scratchSpace["ax_handles"]
		fontSizes = self._getFontSizes(plotterInstance)

		#
		for idx, (ax, inpStr, inpPos, fntSize) in enumerate( zip(axes,useStrs, cycledPositions, fontSizes) ):
			if ax.get_visible():
				currXLim, currYLim = ax.get_xlim(), ax.get_ylim()
				xRange, yRange = currXLim[1]-currXLim[0], currYLim[1]-currYLim[0]
				absPos = [ currXLim[0] + (xRange*inpPos[0]), currYLim[0] + (yRange*inpPos[1]) ]
				annotation = ax.annotate(inpStr, absPos, fontsize=fntSize)
			else:
				self._addAnnotationForSplitAxis(plotterInstance, idx, inpStr, inpPos, fntSize)


			#Take the annotation from the axis and put it on the figure level [FAILS]
			#https://stackoverflow.com/questions/13831824/how-to-prevent-a-matplotlib-annotation-being-clipped-by-other-axes
#			ax.figure.texts.append(ax.texts.pop())
#			annotation.set_visible(True)
#			annotation.set_zorder(500)

#			ax.figure.texts.append(copy.deepcopy(annotation))
#			ax.texts[-1].set_visible(False)
#			annotation.set_visible(False)



	def _getAnnotationPositions(self, plotterInstance):
		defaultPositions = it.cycle([[0.1,0.9]])
		userPositions = plotCmdStdHelp._getValueFromOptName(plotterInstance, self._userPosFractName)
		outVal = it.cycle(userPositions) if userPositions is not None else defaultPositions
		return outVal

	def _getDefaultLowerCaseBolded(self):
		lowerCase = [x for x in string.ascii_lowercase]
		output = [r"$\bf{" + x + r")}$" for x in lowerCase]
		return output

	def _getFontSizes(self, plotterInstance):
		usrFontSize = plotCmdStdHelp._getValueFromOptName(plotterInstance, self._userFontOptName)

		if usrFontSize is not None:
			try:
				iter(usrFontSize)
			except TypeError:
				outFont = it.cycle([usrFontSize])
			else:
				outFont = it.cycle(usrFontSize)
		else:
			outFont = it.cycle([None])

		return outFont


	def _addAnnotationForSplitAxis(self, plotterInstance, idx, inpStr, inpPos, fntSize):
		#Get the relevant axes
		currOutput = plotterInstance._scratchSpace["plotters_outputs"][idx]
		origAxis = plotterInstance._scratchSpace["ax_handles"][idx]
		useAxis = currOutput["plotter"]._scratchSpace["axis_grid"][0][0] #Starts at bottom left

		#Figure out the scale factors for x/y
		_origPos = origAxis.get_position().bounds
		_newPos = useAxis.get_position().bounds
		origWidth, origHeight = _origPos[2], _origPos[3]
		newWidth, newHeight = _newPos[2], _newPos[3]
		scaleX, scaleY = origWidth/newWidth, origHeight/newHeight

		#Get the positions needed + add annotations
		usePos = [inpPos[0]*scaleX, inpPos[1]*scaleY]
		useAxis.annotate(inpStr, usePos, fontsize=fntSize, xycoords="axes fraction")

		#Put this axis ABOVE the last plotted
		baseZOrder = currOutput["plotter"]._scratchSpace["axis_grid"][0][0].get_zorder()
		useAxis.set_zorder(baseZOrder+1)
		


	def _getVisibleAxis(self, plotterInstance):
		axes = plotterInstance._scratchSpace["ax_handles"]
		useAxis = None

		#1) Try to find a visible primary axis
		for rIdx, unused in enumerate(axes):
			if axes[rIdx].get_visible():
				useAxis = axes[rIdx]

		#2) Else, assume we're dealing with a split axis plotter + look for the secondary axes
		if useAxis is None:
			raise NotImplementedError("")
#			axGrid = plotterInstance

		return useAxis


@serializationReg.registerForSerialization()
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


@serializationReg.registerForSerialization()
class CreateRectGridAndAxes(plotCmdCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "create-rect-grid-and-axes"
		self._description = "Creates a grid of empty axes and places handles in _scratchSpace[\"multi_axes\"]"
		self._nRowsAttr, self._nColsAttr = "nRowsGrid", "nColsGrid"
		self._relHeightAttr, self._relWidthAttr = "relGridHeights", "relGridWidths"
		self._plottersAttr = "plotters"
		self._hozSpaceAttr, self._vertSpaceAttr = "spacingHoz", "spacingVert"

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
		hozSpace = plotCmdStdHelp._getValueFromOptName(plotterInstance, self._hozSpaceAttr)
		vertSpace = plotCmdStdHelp._getValueFromOptName(plotterInstance, self._vertSpaceAttr)
		gridSpec = outFig.add_gridspec(nRows, nCols, wspace=hozSpace, hspace=vertSpace)

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


@serializationReg.registerForSerialization()
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


@serializationReg.registerForSerialization()
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

@serializationReg.registerForSerialization()
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


@serializationReg.registerForSerialization()
class PopulateAxesWithPlotters(plotCmdCoreHelp.PlotCommand):

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

		plottersOutputs = list()
		for currAx, currPlotter in zip(axHandles, plotters):
			if currPlotter is not None:
				currOutput = currPlotter.createPlot(currAx)
			else:
				currOutput = dict()
			plottersOutputs.append(currOutput)

		plotterInstance._scratchSpace["plotters_outputs"] = plottersOutputs

@serializationReg.registerForSerialization()
class SetHeightBasedOnNumberRows(plotCmdCoreHelp.PlotCommand):

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


@serializationReg.registerForSerialization()
class SetWidthBasedOnNumberCols(plotCmdCoreHelp.PlotCommand):

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

