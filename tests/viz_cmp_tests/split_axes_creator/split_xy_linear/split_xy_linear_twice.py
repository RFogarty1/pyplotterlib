
import itertools as it
import pyplotlib.standard.plotters as plotters
import pyplotlib.reg_testing.viz_diff.helpers as helpers


def main():
	cmdLineArgs = helpers.parseStdCommandLineArgs()
	templatePlotter = createTemplatePlotter()
	currKwargs = {"axisSizeLinear":True,
	              "legendPlotterGridCoords":[0,1], "plotter":templatePlotter,
	              "splitLinesDraw":True,
	              "xLimits":[ [0,4], [9,13], [29,33] ],
	              "yLimits":[ [-10,10], [70,130], [800,1200]] }
	outPlotter = plotters.SplitAxisPlotterCreator(**currKwargs)

	currKwargs = helpers.getKwargDictFromCmdLineArgs(cmdLineArgs)
	helpers.createAndSavePlotForPlotter(outPlotter, **currKwargs)


def createTemplatePlotter():
	xValsAll = [1,2,3,10,11,12,30,31,32]
	yValsAll = [x**2 for x in xValsAll]
	dataAll = [ [x,y] for x,y in it.zip_longest(xValsAll, yValsAll) ]

	currKwargs = {"dataLabels":["dataA"],"plotData":[dataAll],
	              "lineMarkerStyles":['x'], "lineStyles":['none'],
	              "showLegend":True,
	              "titleStr": "Should be centred still (even after splits)",
	              "xLabelStr":"x-label", "yLabelStr":"y-label"}
	outPlotter = plotters.LinePlotter(**currKwargs)

	return outPlotter


if __name__ == '__main__':
	main()


