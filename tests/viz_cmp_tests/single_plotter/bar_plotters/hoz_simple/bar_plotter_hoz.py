
import itertools as it
import os

import numpy as np

import pyplotterlib.standard.plotters as plotters
import pyplotterlib.reg_testing.viz_diff.helpers as helpers


def main():
	cmdLineArgs = helpers.parseStdCommandLineArgs()
	outPlotter = createPlotter()

	currKwargs = {"saveExp":cmdLineArgs.saveExp, "saveAct":cmdLineArgs.saveAct, "expName":cmdLineArgs.expName, "actName":cmdLineArgs.actName}
	helpers.createAndSavePlotForPlotter(outPlotter, **currKwargs)


def createPlotter():
	kwargs = getPlotterKwargDict()
	plotter = plotters.BarPlotter(**kwargs)
	return plotter


def getPlotterKwargDict():
	dataA = [10,8,12]
	dataB = [4, 2, 20]
	
	_plotOptsDict = {
	
	"dataLabels": ["SeriesA", "SeriesB"],
	"groupLabels": ["propA", "propB", "propC"],
	"figSizeOnCreation": [8,4],
	"gridLinesShowX":True,
	"plotData1D": [dataA, dataB],
	"plotHorizontally":True,
	"showLegend": True,
	"xLabelStr":"Test x-label",
	}
	return _plotOptsDict
	

if __name__ == '__main__':
	main()



