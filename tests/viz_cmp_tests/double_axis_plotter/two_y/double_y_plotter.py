
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
	currKwargs = {"independentXAxis":False, "independentYAxis":True, "plotters":singlePlotters}
	return plotters.DoubleAxisPlotter(**currKwargs)

def _getIndividualPlotters():
	_xVals = [1,2,3,7,8]
	_yValsA = [ x**1.2 for x in _xVals]
	_yValsB = [ x**3.4 for x in _xVals]
	
	_dataA = np.array( [[x,val] for x,val in it.zip_longest(_xVals, _yValsA)] )
	_dataB = np.array( [[x,val] for x,val in it.zip_longest(_xVals, _yValsB)] )
	
	_plotOptsDict = {
	"axisColorY": 'blue',
	"axisColorY_exclSpines":True,
	"dataLabels": ["LabelA"],
	"plotData": [_dataA],
	"legendFractPosStart":[0.1,0.9],
	"lineColors": ['blue'],
	"lineMarkerStyles":['x'],
	"showLegend": True,
	"xLabelStr":"Test x-label",
	"xLimit": [-1,10],
	"yLabelStr": "y-label-A"
	
	}

	plotterA = plotters.LinePlotter(**_plotOptsDict)

	modKwargs = {

	"axisColorY":'orange',
	"axisColorY_exclSpines":True,
	"dataLabels":["LabelB"],
	"plotData":[_dataB],
	"legendFractPosStart":[0.1,0.5],
	"lineColors":['orange'],
	"lineMarkerStyles":['o'],
	"yLabelStr": "y-label-B"

	}
	plotterB = plotterA.createFactory(**modKwargs)

	return [plotterA, plotterB]
	

if __name__ == '__main__':
	main()



