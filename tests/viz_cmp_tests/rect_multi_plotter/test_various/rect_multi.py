
import itertools as it
import numpy as np

import pyplotterlib.standard.plotters as plotters
import pyplotterlib.reg_testing.viz_diff.helpers as helpers

def main():
	cmdLineArgs = helpers.parseStdCommandLineArgs()
	singlePlotters = createFourPlotters()
	currKwargs = { "plotters":singlePlotters, "relGridWidths":[2,1,1,1],
	               "relGridHeights":[1,2,1,1], "nColsGrid":3,
	               "nRowsGrid":2, "fillRowsToMatchPlotters":True,
	               "constrainedLayout":True,
	               "spacingVert":0.4, "spacingHoz":0.2 }
	outPlotter = plotters.RectMultiPlotter(**currKwargs)

	#Save plot
#	currKwargs = {"saveExp":cmdLineArgs.saveExp, "saveAct":cmdLineArgs.saveAct, "expName":cmdLineArgs.expName, "actName":cmdLineArgs.actName}
	currKwargs = helpers.getKwargDictFromCmdLineArgs(cmdLineArgs)
	helpers.createAndSavePlotForPlotter(outPlotter, **currKwargs)



def createFourPlotters():
	currKwargs = {"dataLabels":["labelA"], "showLegend":True, "yLimit":[0,20]}
	basePlotter = plotters.LinePlotter( **currKwargs )

	dataA, dataB, dataC, dataD = _getDataAToD()
	plotterA = basePlotter.createFactory(xLabelStr="x-label-A", plotData=[dataA])
	plotterB = basePlotter.createFactory(xLabelStr="x-label-B", plotData=[dataB])
	plotterC = basePlotter.createFactory(xLabelStr="x-label-C", plotData=[dataC])
	plotterD = basePlotter.createFactory(xLabelStr="x-label-D", plotData=[dataD])

	return [plotterA, plotterB, plotterC, plotterD]

def _getDataAToD():
	#Generate some data
	xVals = [1,2,3,4]
	_yValsA = [x**1.1 for x in xVals]
	_yValsB = [x**2 for x in xVals]
	_yValsC = [x**2.5 for x in xVals]
	_yValsD = [x**3 for x in xVals]

	#
	dataA = np.array( [ [x,x**1.1] for x in xVals ] )
	dataB = np.array( [ [x,x**2.0] for x in xVals ] )
	dataC = np.array( [ [x,x**2.5] for x in xVals ] )
	dataD = np.array( [ [x,x**3.0] for x in xVals ] )

	return [dataA, dataB, dataC, dataD]

if __name__ == '__main__':
	main()


