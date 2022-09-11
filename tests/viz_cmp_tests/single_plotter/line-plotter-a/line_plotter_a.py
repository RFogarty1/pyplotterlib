
import itertools as it
import os

import numpy as np
import matplotlib.pyplot as plt

import pyplotterlib.standard.plotters as plotters
import pyplotterlib.reg_testing.viz_diff.helpers as helpers


def main():
	cmdLineArgs = helpers.parseStdCommandLineArgs()
	outPlotter = plotters.LinePlotter( **getPlotterKwargDict() )

	currKwargs = {"saveExp":cmdLineArgs.saveExp, "saveAct":cmdLineArgs.saveAct, "expName":cmdLineArgs.expName, "actName":cmdLineArgs.actName}
	helpers.createAndSavePlotForPlotter(outPlotter, **currKwargs)


def getPlotterKwargDict():
	_xVals = [1,2,3,7,8]
	_yValsA = [ x**1.2 for x in _xVals]
	_yValsB = [ x**1.4 for x in _xVals]
	
	_dataA = np.array( [[x,val] for x,val in it.zip_longest(_xVals, _yValsA)] )
	_dataB = np.array( [[x,val] for x,val in it.zip_longest(_xVals, _yValsB)] )
	
	_plotOptsDict = {
	
	"dataLabels": ["LabelA", "LabelB"],
	"figSizeOnCreation": [8,4],
	"plotData": [_dataA, _dataB],
	"showLegend": True,
	"xLabelStr":"Test x-label",
	"xLimit": [-1,10] 
	
	}
	return _plotOptsDict
	

if __name__ == '__main__':
	main()



