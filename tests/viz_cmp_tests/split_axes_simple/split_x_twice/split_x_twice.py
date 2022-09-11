
import itertools as it
import pyplotterlib.standard.plotters as plotters
import pyplotterlib.reg_testing.viz_diff.helpers as helpers


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

	currKwargs = {"plotData":[dataAll],
	              "lineMarkerStyles":['x'], "lineStyles":['none'],
	              "xLabelFractPos":[1.5, -0.1], "xLabelStr":"x-label",
	              "xLimit":xLims[0], "yLabelStr":"y-label"}
	plotterX0 = plotters.LinePlotter(**currKwargs)
	plotterX1 = plotterX0.createFactory(xLabelStr=None, xLimit=xLims[1], yLabelStr=None)
	plotterX2 = plotterX0.createFactory(xLabelStr=None, xLimit=xLims[2], yLabelStr=None)

	return [ [plotterX0], [plotterX1], [plotterX2] ]


def setRelevantBordersInvisible(plotterGrid):
	plotterGrid[0][0].opts.axisBorderMakeInvisible.value.right = True
	plotterGrid[1][0].opts.axisBorderMakeInvisible.value.left = True
	plotterGrid[1][0].opts.axisBorderMakeInvisible.value.right = True
	plotterGrid[2][0].opts.axisBorderMakeInvisible.value.left = True


def getSplitAxisPlotterFromPlotterGrid(inpGrid):
	currKwargs = {"fractsX":0.3, "plotterGrid":inpGrid, "spacingX":0.05}
	outPlotter = plotters.SplitAxisPlotter(**currKwargs)
	outPlotter.opts.splitDrawDoubleLinesX.value[0].draw = True
	return outPlotter

if __name__ == '__main__':
	main()


