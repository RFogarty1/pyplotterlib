
import itertools as it
import math

import numpy as np
import matplotlib.lines as lines
import matplotlib.pyplot as plt

from ...core import plotters as plotterCoreHelp
from ...core import plot_options as plotOptCoreHelp
from ...core import plot_command as plotCmdCoreHelp
from ...core import json_transform as jsonTransformCoreHelp

from .. import plot_commands as plotCmdStdHelp



class SplitAxisPlotter(plotterCoreHelp.SingleGraphPlotter):

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
		plotCmdStdHelp.CreateFigureIfNoAxHandle(),
		CreateOutputAxes(),
		AddPlotsToAxisGrid(),
		MakeOrigAxisInvisible(),
		DrawDoubleLinesForAxisSplits()
	]
	return outList


def _createOptionsList():
	outList = [
	
	FractsX(),
	FractsY(),
	PlotterGrid(),
	SpacingX(),
	SpacingY(),
	SplitDrawDoubleLinesX(),
	SplitDrawDoubleLinesY()

	]
	return outList


#Options


class SplitDrawDoubleLinesX(plotOptCoreHelp.ObjectIterPlotOption):
	""" Controls drawing of double lines to demarcate points where the x-axis is split. Values are iters of DoubleLinesConfig objects.

	Note: If the iter is length-1 (as by default) these settings will cycle over all x-axis splits (i.e. you will only usually need a len-1 array)

	"""
	def __init__(self, name=None, value=None):
		self.name = "splitDrawDoubleLinesX" if name is None else name
		self.value = [DoubleLinesConfig(draw=False)] if value is None else value

class SplitDrawDoubleLinesY(plotOptCoreHelp.ObjectIterPlotOption):
	""" Controls drawing of double lines to demarcate points where the y-axis is split. Values are iters of DoubleLinesConfig objects.

	Note: If the iter is length-1 (as by default) these settings will cycle over all t-axis splits (i.e. you will only usually need a len-1 array)

	"""
	def __init__(self, name=None, value=None):
		self.name = "splitDrawDoubleLinesY" if name is None else name
		self.value = [DoubleLinesConfig(draw=False)] if value is None else value



class DoubleLinesConfig(jsonTransformCoreHelp.JSONTransformInterface):
	""" Effectively a namespace for holding options related to drawing double lines for points where an axis is split 

	Attributes:
		draw (Boolean): If True, draw the lines. Else dont draw them. 
		length (Float): The length of the lines to draw. Should be a fraction of axis height (when splitting x) or width (when splitting y).
		angle (Float): The Angle of rotation to apply. For angle=0 the lines will point along the y-axis when splitting x, and the x-axis when splitting y 

	"""
	def __init__(self, draw=True, length=0.05, angle=45):
		self.draw = draw
		self.length = length
		self.angle = angle

	def toJSON(self):
		raise NotImplementedError("")

	@classmethod
	def fromJSON(cls, inpJSON):
		raise NotImplementedError("")


#NOTE: Cant serialize this 2-d grid of objects yet
#@serializationReg.registerForSerialization()
class PlotterGrid(plotOptCoreHelp.SinglePlotOptionInter):
	""" Contains individual plotters for the axis. Iter of iters (essentially a 2-d grid) with each element being an iter of plotters for one x-segment. For example: [ [plotterX0Y0, plotterX0Y1, plotterX0Y2], [plotterX1Y0, plotterX1Y1, plotter X1Y2] ] corresponds to a case of 1-split on the x-axis and 2 splits on the y-axis

	"""
	def __init__(self, name=None, value=None):
		self.name = "plotterGrid" if name is None else name
		self.value = value


class FractsX(plotOptCoreHelp.FloatIterOrSingleFloatOption):
	""" The fractional widths of each x-plotter. Can set as a float if they are all equal, else a list. Note, these values will be normalised it doesnt matter if the sum of fractsX and spacingX add to 1.0 or not 

	e.g. value = 0.3, value = [0.2,0.3,0.2]

	"""
	def __init__(self, name=None, value=None):
		self.name = "fractsX" if name is None else name
		self.value = 0.5 if value is None else value

class FractsY(plotOptCoreHelp.FloatIterOrSingleFloatOption):
	""" The fractional heights of each y-plotter. Can set as a float if they are all equal, else a list. Note, these values will be normalised it doesnt matter if the sum of fractsY and spacingX add to 1.0 or not 

	e.g. value = 0.3, value = [0.2,0.3,0.2]

	"""
	def __init__(self, name=None, value=None):
		self.name = "fractsY" if name is None else name
		self.value = 0.5 if value is None else value


class SpacingX(plotOptCoreHelp.FloatIterOrSingleFloatOption):
	""" The fractional spacing BETWEEN each pair of split x-axes. Can be a single float or an iter of floats. If an iter, it should be 1 less than the number of x-plotters (and equal the number of splits).

	e.g value=0.1, value = [0.05, 0.1] are both valid

	"""
	def __init__(self, name=None, value=None):
		self.name = "spacingX" if name is None else name
		self.value = 0.1 if value is None else value

class SpacingY(plotOptCoreHelp.FloatIterOrSingleFloatOption):
	""" The fractional spacing BETWEEN each pair of split y-axes. Can be a single float or an iter of floats. If an iter, it should be 1 less than the number of y-plotters (and equal the number of splits).

	e.g value=0.1, value = [0.05, 0.1] are both valid

	"""
	def __init__(self, name=None, value=None):
		self.name = "spacingY" if name is None else name
		self.value = 0.1 if value is None else value

#Commands

class DrawDoubleLinesForAxisSplits(plotCmdCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "draw-double-lines-for-axis-splits"
		self._description = "Draws a pair of double lines for each point in which each axis splits"

	#TODO: We likely need to just be passing args to a generic function (which works on x AND y)
	# The class should mainly handle getting the corrects args etc.
	def execute(self, plotterInstance):

		#1) Get the centroids
		xCentroids = self._getCentroidPositionsX(plotterInstance)
		yCentroids = self._getCentroidPositionsY(plotterInstance)

		#2) Figure out how wide/high the TOTAL graph is
		#TODO: Currently wrong; need the original axis NOT gca
#		_startX, _startY, _endX, _endY = _getAxisEdges(plt.gca())
		_startX, _startY, _endX, _endY = _getAxisEdges( plotterInstance._scratchSpace["original_axis"] )
		axWidth, axHeight = _endX - _startX, _endY - _startY

		#3) Use all previous info to draw lines around x-splits
		_drawDoubleLineOnXSplitsIfNeeded(plotterInstance.opts.splitDrawDoubleLinesX.value, xCentroids, axHeight)
		_drawDoubleLineOnXSplitsIfNeeded(plotterInstance.opts.splitDrawDoubleLinesX.value, xCentroids, axHeight, offsetVal=[0,axHeight])

		_drawDoubleLineOnYSplitsIfNeeded(plotterInstance.opts.splitDrawDoubleLinesY.value, yCentroids, axWidth)
		_drawDoubleLineOnYSplitsIfNeeded(plotterInstance.opts.splitDrawDoubleLinesY.value, yCentroids, axWidth, offsetVal=[axWidth,0])

	def _getCentroidPositionsX(self, plotterInstance):
		allPositions = plotterInstance._scratchSpace["new_axis_positions"]
		numbXSplits = len(allPositions) - 1
		if numbXSplits < 1:
			return list()

		centroids = list()
		for idx,unused in enumerate(allPositions[1:],start=1):
			posA, posB = allPositions[idx-1][0], allPositions[idx][0]
			startY = posA[1]
			startX = posA[0] + posA[2]
			endX = posB[0]
			centroidA = [startX, startY]
			centroidB = [endX, startY]
			centroids.append( [centroidA, centroidB] ) 
		return centroids


	def _getCentroidPositionsY(self, plotterInstance):
		allPositions = plotterInstance._scratchSpace["new_axis_positions"]
		numbYSplits = len(allPositions[0]) - 1
		if numbYSplits < 1:
			return list()


		usePositions = allPositions[0]

		centroids = list()
		for idx,unused in enumerate(usePositions[1:],start=1):
			posA, posB = usePositions[idx-1], usePositions[idx]
			startX = posA[0]
			startY, endY = posA[1] + posA[3], posB[1]
			centroidA = [startX, startY]
			centroidB = [startX, endY]
			centroids.append( [centroidA, centroidB] ) 
		return centroids


def _drawDoubleLineOnXSplitsIfNeeded(drawOpts, centroids, axHeight, offsetVal=None):
	offsetVal = [0,0] if offsetVal is None else offsetVal

	numbSplits = len(centroids)
	useOpts = it.cycle(drawOpts)

	for (centroidA, centroidB), currOpts in zip(centroids, useOpts):
		#Create a vector representing the lines; angle=0 should point along y
		heightY = axHeight*currOpts.length
		inpVector = np.array( [0, heightY] )

		#Apply a rotation to the vector
		rotVal = math.radians(-1*currOpts.angle)
		rotMatrix = np.array( [ [math.cos(rotVal), -1*math.sin(rotVal)],
		                        [math.sin(rotVal), math.cos(rotVal)] ] )

		outVector = np.dot(rotMatrix, inpVector)

		#Build the output lines in terms of these vectors
		centroidA[0] += offsetVal[0]
		centroidA[1] += offsetVal[1]
		centroidB[0] += offsetVal[0]
		centroidB[1] += offsetVal[1]
		xValsA = [ centroidA[0] - outVector[0]*0.5, centroidA[0] + outVector[0]*0.5 ]  
		xValsB = [ centroidB[0] - outVector[0]*0.5, centroidB[0] + outVector[0]*0.5 ]
		yValsA = [ centroidA[1] - outVector[1]*0.5, centroidA[1] + outVector[1]*0.5 ]
		yValsB = [ centroidB[1] - outVector[1]*0.5, centroidB[1] + outVector[1]*0.5 ]


		#If requested; add these output lines to the figure
		if currOpts.draw:
			currFig = plt.gcf()
			currFig.add_artist(lines.Line2D(xValsA, yValsA))
			currFig.add_artist(lines.Line2D(xValsB, yValsB))

#VERY similar to the x-splits
def _drawDoubleLineOnYSplitsIfNeeded(drawOpts, centroids, axWidth, offsetVal=None):
	offsetVal = [0,0] if offsetVal is None else offsetVal
	numbSplits = len(centroids)
	useOpts = it.cycle(drawOpts)

	for (centroidA, centroidB), currOpts in zip(centroids, useOpts):
		widthX = axWidth*currOpts.length
		inpVector = np.array( [widthX, 0] )

		#Apply a rotation
		rotVal = math.radians(currOpts.angle)
		rotMatrix = np.array( [ [math.cos(rotVal), -1*math.sin(rotVal)],
		                        [math.sin(rotVal), math.cos(rotVal)] ])
		outVector = np.dot(rotMatrix, inpVector)

		#Build the output lines in terms of these vectors
		centroidA[0] += offsetVal[0]
		centroidA[1] += offsetVal[1]
		centroidB[0] += offsetVal[0]
		centroidB[1] += offsetVal[1]
		xValsA = [ centroidA[0] - outVector[0]*0.5, centroidA[0] + outVector[0]*0.5 ]  
		xValsB = [ centroidB[0] - outVector[0]*0.5, centroidB[0] + outVector[0]*0.5 ]
		yValsA = [ centroidA[1] - outVector[1]*0.5, centroidA[1] + outVector[1]*0.5 ]
		yValsB = [ centroidB[1] - outVector[1]*0.5, centroidB[1] + outVector[1]*0.5 ]


		#If requested; add these output lines to the figure
		if currOpts.draw:
			currFig = plt.gcf()
			currFig.add_artist(lines.Line2D(xValsA, yValsA))
			currFig.add_artist(lines.Line2D(xValsB, yValsB))

		


class CreateOutputAxes(plotCmdCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "create-output-axes"
		self._description = "Create the output axes to use for the split axes plot"

	def execute(self, plotterInstance):
		origAx = plt.gca()
		plotterInstance._scratchSpace["original_axis"] = origAx

		_attrNames = ["plotterGrid", "fractsX", "fractsY", "spacingX", "spacingY"]
		currArgs = [getattr(plotterInstance.opts,x).value for x in _attrNames]
		if currArgs[0] is None:
			raise ValueError("plotterGrid MUST be set to use split_axis_plotter")
#			currArgs[0], _tempList = list(), list()
#			currArgs[0].append(_tempList)
 
		outPositions = _getOutputAxesPositions(*currArgs)
		plotterInstance._scratchSpace["new_axis_positions"] = outPositions

		outAxesGrid = list()
		figHandle = origAx.figure
		for xIdx, unused in enumerate(outPositions):
			outAxesGrid.append( list() ) 
			for yIdx, unused in enumerate(outPositions[xIdx]):
				currPos = outPositions[xIdx][yIdx]
				currAxis = figHandle.add_axes(currPos)
				outAxesGrid[xIdx].append(currAxis)

		plotterInstance._scratchSpace["axis_grid"] = outAxesGrid


def _getOutputAxesPositions(plotterGrid, fractsX, fractsY, spacingX, spacingY):
	nPlottersX = len(plotterGrid)
	nPlottersY = len(plotterGrid[0])

	#Get the unnormalised fractional positions
	fractXList = _getListFromFloatOrFloatIter(fractsX, nPlottersX)
	fractYList = _getListFromFloatOrFloatIter(fractsY, nPlottersY)
	spaceXList = _getListFromFloatOrFloatIter(spacingX, nPlottersX-1)
	spaceYList = _getListFromFloatOrFloatIter(spacingY, nPlottersY-1)

	#Figure out the original axes bounds; these are fractional with respect to the whole figure so cant go outside them
	startX, startY, endX, endY = _getAxisEdges(plt.gca())

	#Divide the space in the RATIOS determined by spacing and fract values for each
	xSpace, ySpace = endX - startX, endY - startY
	xScaleFactor = xSpace / ( sum(fractXList) + sum(spaceXList) )
	yScaleFactor = ySpace / ( sum(fractYList) + sum(spaceYList) )


	def _getStartPositionsAndLengths(startVal, fractVals, spaceVals, scaleFactor):
		outStartPositions, outLengths = [startVal], [fractVals[0]*scaleFactor]
		for idx, fractVal in enumerate(fractVals[1:], start=1):
			outStartPositions.append( outStartPositions[idx-1] + outLengths[idx-1] + (spaceVals[idx-1]*scaleFactor) )
			outLengths.append( fractVal*scaleFactor ) 
		return outStartPositions, outLengths

	#Figure out the start/length positions for our new axes
	xStartPositions, xLengthVals = _getStartPositionsAndLengths(startX, fractXList, spaceXList, xScaleFactor) 
	yStartPositions, yLengthVals = _getStartPositionsAndLengths(startY, fractYList, spaceYList, yScaleFactor)
	scaledSpacingX = [val*xScaleFactor for val in spaceXList]
	scaledSpacingY = [val*yScaleFactor for val in spaceYList]


	#Get the full output axes positions
	outGridPositions = list()
	for xIdx, unused in enumerate(plotterGrid):
		outGridPositions.append(list())
		for yIdx, unused in enumerate(plotterGrid[xIdx]):
			currStartX = startX + sum(xLengthVals[:xIdx]) + sum(scaledSpacingX[:xIdx])
			currStartY = startY + sum(yLengthVals[:yIdx]) + sum(scaledSpacingY[:yIdx])
			outPos = [currStartX, currStartY, xLengthVals[xIdx], yLengthVals[yIdx]]
			outGridPositions[xIdx].append(outPos)


	return outGridPositions

def _getListFromFloatOrFloatIter(inpVal, maxLen):
	try:
		iter(inpVal)
	except TypeError:
		return [ inpVal for x in range(maxLen) ]
	else:
		return [ x for x,unused in zip( it.cycle(inpVal), range(maxLen) ) ] 


def _getAxisEdges(inpAx):
	startX, startY, xLength, yLength = inpAx.get_position().bounds
	endX, endY = startX+xLength, startY+yLength
	return startX, startY, endX, endY


class AddPlotsToAxisGrid(plotCmdCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "add-plots-to-grid"
		self._description = "Add plotters to the axis grid"

	def execute(self, plotterInstance):
		axGrid = plotterInstance._scratchSpace["axis_grid"]
		plotterGrid = getattr(plotterInstance.opts,"plotterGrid").value

		for xIdx, unused in enumerate(axGrid):
			for yIdx, unused in enumerate(axGrid[xIdx]):
				plotterGrid[xIdx][yIdx].createPlot(axHandle=axGrid[xIdx][yIdx])



class MakeOrigAxisInvisible(plotCmdCoreHelp.PlotCommand):

	def __init__(self):
		self._name = "make-orig-axis-invisible"
		self._description = "Makes the original axis invisible"

	def execute(self, plotterInstance):
		origAx = plotterInstance._scratchSpace["original_axis"]
		origAx.set_visible(False)









