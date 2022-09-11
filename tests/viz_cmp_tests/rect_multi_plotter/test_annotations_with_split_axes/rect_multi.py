
import itertools as it
import numpy as np


import pyplotterlib.standard.plotters as plotters
import pyplotterlib.reg_testing.viz_diff.helpers as helpers

def main():
	cmdLineArgs = helpers.parseStdCommandLineArgs()

	#Note: Constrained layout simply fails for the split axis plotters 
	singlePlotters = createTwoPlotters()
	currKwargs = { "annotateLabelPosFract":[[0.1,0.7]],
	               "annotateLabelStrings_useBoldedLowerAlphabetByDefault":True,
	               "plotters":singlePlotters, "figSizeOnCreation":(12,4),
	               "nColsGrid":2, "fillRowsToMatchPlotters":True,
	               "constrainedLayout":False }
	outPlotter = plotters.RectMultiPlotter(**currKwargs)

	#Save plot
#	currKwargs = {"saveExp":cmdLineArgs.saveExp, "saveAct":cmdLineArgs.saveAct, "expName":cmdLineArgs.expName, "actName":cmdLineArgs.actName}
	currKwargs = helpers.getKwargDictFromCmdLineArgs(cmdLineArgs)
	helpers.createAndSavePlotForPlotter(outPlotter, **currKwargs)


def createTwoPlotters():
	currKwargs = {"dataLabels":["labelA"], "showLegend":True}
	basePlotter = plotters.LinePlotter( **currKwargs )
	dataA, dataB, dataC, dataD = _getDataAToD()

	#Create a simple line plotter
	plotterA = basePlotter.createFactory(xLabelStr="x-label-A", plotData=[dataA])

	#Create a split axes plotter
	_tempPlotterB = basePlotter.createFactory(xLabelStr="x-label-B", plotData=[dataB])

	currKwargs = {"plotter":_tempPlotterB,
	              "legendPlotterGridCoords":[0,1],
	              "yLimits":[ [0,5], [8,25] ]}
	outPlotterB = plotters.SplitAxisPlotterCreator(**currKwargs)

	return [plotterA, outPlotterB]


#def createFourPlotters():
#	currKwargs = {"dataLabels":["labelA"], "showLegend":True, "yLimit":[0,20]}
#	basePlotter = plotters.LinePlotter( **currKwargs )
#
#	dataA, dataB, dataC, dataD = _getDataAToD()
#	plotterA = basePlotter.createFactory(xLabelStr="x-label-A", plotData=[dataA])
#	plotterB = basePlotter.createFactory(xLabelStr="x-label-B", plotData=[dataB])
#	plotterC = basePlotter.createFactory(xLabelStr="x-label-C", plotData=[dataC])
#	plotterD = basePlotter.createFactory(xLabelStr="x-label-D", plotData=[dataD])
#
#	return [plotterA, plotterB, plotterC, plotterD]

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


