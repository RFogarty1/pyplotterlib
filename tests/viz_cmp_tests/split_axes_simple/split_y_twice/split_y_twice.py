
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

	yLims = [ [0,10], [70,130], [800,1200] ]  

	currKwargs = {"plotData":[dataAll],
	              "lineMarkerStyles":['x'], "lineStyles":['none'],
	              "yLabelFractPos":[-0.1, 2], "xLabelStr":"x-label",
	              "yLimit":yLims[0], "yLabelStr":"y-label"}
	plotterY0 = plotters.LinePlotter(**currKwargs)
	plotterY1 = plotterY0.createFactory(yLabelStr=None, yLimit=yLims[1], xLabelStr=None)
	plotterY2 = plotterY0.createFactory(yLabelStr=None, yLimit=yLims[2], xLabelStr=None)

	return [ [plotterY0, plotterY1, plotterY2] ]


def setRelevantBordersInvisible(plotterGrid):
	plotterGrid[0][0].opts.axisBorderMakeInvisible.value.top = True
	plotterGrid[0][1].opts.axisBorderMakeInvisible.value.bottom = True
	plotterGrid[0][1].opts.axisBorderMakeInvisible.value.top = True
	plotterGrid[0][2].opts.axisBorderMakeInvisible.value.bottom = True


def getSplitAxisPlotterFromPlotterGrid(inpGrid):
	currKwargs = {"fractsX":0.3, "fractsY":0.3, "plotterGrid":inpGrid, "spacingX":0.05, "spacingY":0.05}
	outPlotter = plotters.SplitAxisPlotter(**currKwargs)
	outPlotter.opts.splitDrawDoubleLinesY.value[0].draw = True
	return outPlotter

if __name__ == '__main__':
	main()


