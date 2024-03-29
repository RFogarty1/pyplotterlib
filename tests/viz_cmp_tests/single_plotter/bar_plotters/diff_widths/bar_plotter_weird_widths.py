
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
	"barOpacities":[0.3,0.8],
	"dataLabels": ["SeriesA", "SeriesB"],
	"groupLabels": ["propA", "propB", "propC"],
	"figSizeOnCreation": [8,4],
	"gridLinesShowY":True,
	"plotData1D": [dataA, dataB],
	"showLegend": True,
	"xLabelStr":"Test x-label",
	"widthInterSpacing":-0.4,
	"widthIntraSpacing":0.4,
	"widthBars":0.1
	}
	return _plotOptsDict
	

if __name__ == '__main__':
	main()



