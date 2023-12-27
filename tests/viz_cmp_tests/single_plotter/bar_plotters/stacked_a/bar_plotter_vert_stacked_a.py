
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
	dataC = [3,1,5]
	dataD = [8,2,14]
	
	_plotOptsDict = {
	
	"dataLabels": ["Series A", "Series B", "Series C", "Series D"],
	"groupLabels": ["propA", "propB", "propC"],
	"groupLabelTickPosKey":"groupLeftEdges",
	"figSizeOnCreation": [8,4],
	"gridLinesShowY":True,
	"plotData1D": [dataA, dataB,dataC,dataD],
	"stackBars":[False,True,True],
	"showLegend": True,
	"xLabelStr":"Test x-label"
	
	}
	return _plotOptsDict
	

if __name__ == '__main__':
	main()



