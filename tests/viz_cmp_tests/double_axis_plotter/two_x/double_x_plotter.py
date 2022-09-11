
import itertools as it
import os

import numpy as np
import matplotlib.pyplot as plt

import pyplotterlib.standard.plotters as plotters
import pyplotterlib.reg_testing.viz_diff.helpers as helpers


def main():
	cmdLineArgs = helpers.parseStdCommandLineArgs()
	outPlotter = _getPlotter()

#	currKwargs = {"saveExp":cmdLineArgs.saveExp, "saveAct":cmdLineArgs.saveAct, "expName":cmdLineArgs.expName, "actName":cmdLineArgs.actName}

	currKwargs = helpers.getKwargDictFromCmdLineArgs(cmdLineArgs)
	helpers.createAndSavePlotForPlotter(outPlotter, **currKwargs)



def _getPlotter():
	singlePlotters = _getIndividualPlotters()
	currKwargs = {"independentXAxis":True, "independentYAxis":False, "plotters":singlePlotters}
	return plotters.DoubleAxisPlotter(**currKwargs)

def _getIndividualPlotters():
	_xVals = [1,2,3,7,8]
	_xValsB = [ x*2 for x in _xVals]
	_yValsA = [ x**1.2 for x in _xVals]
	_yValsB = [ x**3.4 for x in _xVals]
	
	_dataA = np.array( [[x,val] for x,val in it.zip_longest(_xVals, _yValsA)] )
	_dataB = np.array( [[x,val] for x,val in it.zip_longest(_xValsB, _yValsA)] )
	
	_plotOptsDict = {
#	"axisColorX": 'blue',
#	"axisColorX_exclSpines":True,
	"dataLabels": ["LabelA"],
	"plotData": [_dataA],
	"legendFractPosStart":[0.1,0.9],
	"lineColors": ['blue'],
	"lineMarkerStyles":['x'],
	"showLegend": True,
	"xLabelStr":"x-label-A",
#	"xLimit": [-1,10],
	"yLabelStr": "y-label-A"
	
	}

	plotterA = plotters.LinePlotter(**_plotOptsDict)

	modKwargs = {
	"dataLabels":["LabelB"],
	"plotData":[_dataB],
	"showLegend": False,
#	"legendFractPosStart":[0.1,0.5],
#	"lineColors":['orange'],
	"lineMarkerStyles":['o'],
	"xLabelStr": "x-label-B",
	"xLimit":None
	}
	plotterB = plotterA.createFactory(**modKwargs)

	return [plotterA, plotterB]
	

if __name__ == '__main__':
	main()



