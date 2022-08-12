
import itertools as it
import pyplotlib.standard.plotters as plotters
import pyplotlib.reg_testing.viz_diff.helpers as helpers


def main():
	cmdLineArgs = helpers.parseStdCommandLineArgs()
	plotterGrid = createPlotterGrid()
	setRelevantBordersInvisible(plotterGrid)
	outPlotter = getSplitAxisPlotterFromPlotterGrid(plotterGrid)

	currKwargs = helpers.getKwargDictFromCmdLineArgs(cmdLineArgs)
	helpers.createAndSavePlotForPlotter(outPlotter, **currKwargs)



def createPlotterGrid():
	xValsAll = [1,2,3,10,11,12,30,31,32]
	yValsAll = [x**2 for x in xValsAll]
	dataAll = [ [x,y] for x,y in it.zip_longest(xValsAll, yValsAll) ]

	xLims = [ [0,4], [9,13], [29,33] ]  
	yLims = [ [0,10], [70,130], [800,1200] ]

	currKwargs = {"plotData":[dataAll],
	              "lineMarkerStyles":['x'], "lineStyles":['none'],
	              "xLabelFractPos":[1.5, -0.3], "xLabelStr":"x-label", "xLimit":xLims[0],
	              "yLabelFractPos":[-0.3,1.5],  "yLabelStr":"y-label", "yLimit":yLims[0]}
	_basePlotter = plotters.LinePlotter(**currKwargs)

	plotterX0Y0 = _basePlotter.createFactory()
	plotterX0Y1 = _basePlotter.createFactory(xLabelStr=None, yLabelStr=None, xLimit=xLims[0], yLimit=yLims[1] )
	plotterX0Y2 = _basePlotter.createFactory(xLabelStr=None, yLabelStr=None, xLimit=xLims[0], yLimit=yLims[2] )

	plotterX1Y0 = _basePlotter.createFactory(xLabelStr=None, yLabelStr=None, xLimit=xLims[1], yLimit=yLims[0] )
	plotterX1Y1 = _basePlotter.createFactory(xLabelStr=None, yLabelStr=None, xLimit=xLims[1], yLimit=yLims[1] )
	plotterX1Y2 = _basePlotter.createFactory(xLabelStr=None, yLabelStr=None, xLimit=xLims[1], yLimit=yLims[2] )

	plotterX2Y0 = _basePlotter.createFactory(xLabelStr=None, yLabelStr=None, xLimit=xLims[2], yLimit=yLims[0] )
	plotterX2Y1 = _basePlotter.createFactory(xLabelStr=None, yLabelStr=None, xLimit=xLims[2], yLimit=yLims[1] )
	plotterX2Y2 = _basePlotter.createFactory(xLabelStr=None, yLabelStr=None, xLimit=xLims[2], yLimit=yLims[2] )


	return [ [plotterX0Y0, plotterX0Y1, plotterX0Y2],
	         [plotterX1Y0, plotterX1Y1, plotterX1Y2],
	         [plotterX2Y0, plotterX2Y1, plotterX2Y2] ]


def setRelevantBordersInvisible(plotterGrid):
	# 
	plotterGrid[0][0].opts.axisBorderMakeInvisible.value.right = True
	plotterGrid[0][0].opts.axisBorderMakeInvisible.value.top = True

	plotterGrid[0][1].opts.axisBorderMakeInvisible.value.top = True
	plotterGrid[0][1].opts.axisBorderMakeInvisible.value.bottom = True
	plotterGrid[0][1].opts.axisBorderMakeInvisible.value.right = True

	plotterGrid[0][2].opts.axisBorderMakeInvisible.value.bottom = True
	plotterGrid[0][2].opts.axisBorderMakeInvisible.value.right = True

	#
	plotterGrid[1][0].opts.axisBorderMakeInvisible.value.left = True
	plotterGrid[1][0].opts.axisBorderMakeInvisible.value.right = True
	plotterGrid[1][0].opts.axisBorderMakeInvisible.value.top = True

	plotterGrid[1][1].opts.axisBorderMakeInvisible.value.top = True
	plotterGrid[1][1].opts.axisBorderMakeInvisible.value.bottom = True
	plotterGrid[1][1].opts.axisBorderMakeInvisible.value.right = True
	plotterGrid[1][1].opts.axisBorderMakeInvisible.value.left = True

	plotterGrid[1][2].opts.axisBorderMakeInvisible.value.bottom = True
	plotterGrid[1][2].opts.axisBorderMakeInvisible.value.right = True
	plotterGrid[1][2].opts.axisBorderMakeInvisible.value.left = True

	#
	plotterGrid[2][0].opts.axisBorderMakeInvisible.value.left = True
	plotterGrid[2][0].opts.axisBorderMakeInvisible.value.top = True

	plotterGrid[2][1].opts.axisBorderMakeInvisible.value.top = True
	plotterGrid[2][1].opts.axisBorderMakeInvisible.value.bottom = True
	plotterGrid[2][1].opts.axisBorderMakeInvisible.value.left = True

	plotterGrid[2][2].opts.axisBorderMakeInvisible.value.bottom = True
	plotterGrid[2][2].opts.axisBorderMakeInvisible.value.left = True



def getSplitAxisPlotterFromPlotterGrid(inpGrid):
	currKwargs = {"fractsX":0.3, "plotterGrid":inpGrid, "spacingX":0.05}
	outPlotter = plotters.SplitAxisPlotter(**currKwargs)
	outPlotter.opts.splitDrawDoubleLinesX.value[0].draw = True
	outPlotter.opts.splitDrawDoubleLinesY.value[0].draw = True
	return outPlotter

if __name__ == '__main__':
	main()


