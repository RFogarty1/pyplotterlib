
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

	#The data	
	_dataA = np.array( [[x,val] for x,val in it.zip_longest(_xVals, _yValsA)] )
	_dataB = np.array( [[x,val] for x,val in it.zip_longest(_xVals, _yValsB)] )
	
	#Asymmetric error bars
	_errorBarsA_x = [ [0.2,0.1] for x in _xVals ]
	_errorBarsA_y = [ [0.2*y, 0.05*y] for y in _yValsA ]

	#Symmetric error bars
	_errorBarsB_x = [0.4 for x in _xVals]
	_errorBarsB_y = [0.2*y for y in _yValsB]

	_plotOptsDict = {
	"annotationsTextGeneric": _getTextAnnotateObjs(),
	"annotationsShadedGeneric": _getShadedAnnotateObjs(),
	"dataLabels": ["LabelA", "LabelB"],
	"errorBarCapsize":[None,7],
	"errorBarColors":['red'],
	"errorBarDataX":[_errorBarsA_x,_errorBarsB_x],
	"errorBarDataY":[_errorBarsA_y,_errorBarsB_y],
	"figSizeOnCreation": [8,4],
	"lineMarkerStyles":["x","."],
	"plotData": [_dataA, _dataB],
	"showLegend": True,
	"xLabelStr":"Test x-label",
	"xLimit": [-1,10] 
	
	}
	return _plotOptsDict


def _getTextAnnotateObjs():
	#Basic annotation A
	_currKwargs = {"textVal":"Annotation A", "textPos":[0,16],"arrowPos":[6,16]}
	annotationA = plotters.annotations.TextAnnotation(**_currKwargs)

	#Different coord system
	_updateKwargs = {"textVal":"Annotation B","arrowPos":None, "textPos":[0.1,0.5], "textCoordSys":"axes fraction"}
	_currKwargs.update(_updateKwargs)
	annotationB = plotters.annotations.TextAnnotation(**_currKwargs)

	#Changes to text color and arrow width
	_updateKwargs =  {"arrowPropHooks":{"width":1}, "annotateMplHooks":{"color":"blue"}, "textPos":[0.1,0.4], "textVal":"Annotation C"} 
	_currKwargs.update(_updateKwargs)
	annotationC = plotters.annotations.TextAnnotation(**_currKwargs)

	return [annotationA, annotationB, annotationC]


def _getShadedAnnotateObjs():
	annotationA = plotters.annotations.ShadedSliceAnnotation([7,8]  ,opacity=0.1, direction="vertical", color="red")
	annotationB = plotters.annotations.ShadedSliceAnnotation([2.5,5],opacity=0.8, direction="horizontal", color="purple")
	return [annotationA, annotationB]




if __name__ == '__main__':
	main()



