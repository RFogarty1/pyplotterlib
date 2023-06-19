
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
	dataC = [6,4,18]
	dataD = [8,10,4]

	errorBarDataB = [x*0.2 for x in dataB]
	errorBarDataC = [x*0.05 for x in dataC]
	
	_plotOptsDict = {
	"barLabels":_getBarLabels(),
	"dataLabels": ["SeriesA", "SeriesB", "Series C", "Series D"],
	"errorBarData":[None, errorBarDataB, errorBarDataC, None],
	"errorBarCapsize":[3,6],
	"errorBarColors":["red","blue"],
	"groupLabels": ["propA", "propB", "propC"],
	"figSizeOnCreation": [8,4],
	"gridLinesShowY":True,
	"plotData1D": [dataA, dataB, dataC, dataD],
	"showLegend": True,
	"xLabelStr":"Test x-label"
	
	}
	return _plotOptsDict
	

def _getBarLabels():
	#
	_kwargs = {"fmt":"{:.0f}", "paddingVal":2, "fontSize":8, "mplBarLabelHooks":{"color":"red"}}
	barLabelsA = plotters.annotations.BarLabelAnnotation(**_kwargs)

	#
	_kwargs.update( {"mplBarLabelHooks":{"color":None, "label_type":"center"}, "fontRotation":90, "fontSize":14} ) 
	barLabelsB = plotters.annotations.BarLabelAnnotation(**_kwargs)

	return [barLabelsA, barLabelsB]

if __name__ == '__main__':
	main()



