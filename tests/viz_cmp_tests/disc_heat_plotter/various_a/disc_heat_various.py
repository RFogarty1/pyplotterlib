
#import copy
#import itertools as it
#import os

import numpy as np
#import matplotlib.pyplot as plt


import pyplotterlib.standard.plotters as ppl
import pyplotterlib.reg_testing.viz_diff.helpers as helpers



def main():
	#Create the plotter to use
	plotters = createPlotters()
	usePlotter = _createMultiPlotter(plotters)

	#
	cmdLineArgs = helpers.parseStdCommandLineArgs()
	currKwargs = {"saveExp":cmdLineArgs.saveExp, "saveAct":cmdLineArgs.saveAct, "expName":cmdLineArgs.expName, "actName":cmdLineArgs.actName}
	helpers.createAndSavePlotForPlotter(usePlotter, **currKwargs)


def createPlotters():
	#Create a basic template plotter
	_currKwargs = {"colorBarLabel": "Test Label", "colorMapStr":"cool", "fontSizeDefault":12,
	               "gridLinesShow":True, "yLabelStr":"Pointless y-label"}
	templPlotter = ppl.DiscreteHeatMapPlotter(**_currKwargs)

	#Create input matrices
	rectMatrixA = np.array(  [ [1.0, 0.5, 1.2], [2.5, 1.8, 0.7] ] )
	sqrMatrixA = np.array( [ [1.0, 0.1, -0.7], [0.1, 1.0, 0.5], [-0.7, 0.5, 1.0] ] )

	#Create a few plotters with slightly varying properties
	outPlotters = list()
	
	#Few different shapes
	outPlotters.append( templPlotter.createFactory(plotData=rectMatrixA) )
	outPlotters.append( templPlotter.createFactory(plotData=sqrMatrixA) )
	outPlotters.append( templPlotter.createFactory(plotData=sqrMatrixA, plotUpperTri=False))

	#Add colorbar, grouplabel, title
	_currKwargs = {"colorBarShow":True, "gridLinesShow":False,
	               "groupLabels":["labelA", "labelB", "labelC"], "groupLabelsColsRotation":20,
	               "titleStr": "Disc. Heat Plotter"} 
	secondTemplPlotter = templPlotter.createFactory(**_currKwargs)

	#Relatively normal one
	outPlotters.append( secondTemplPlotter.createFactory(plotData=sqrMatrixA) )

	#UpperTri missing + Annotations on + colorbar moved
	_currKwargs = {"annotateVals":True, "colorBarLocation":"bottom", "plotData":sqrMatrixA, "plotUpperTri":False}  
	outPlotters.append( secondTemplPlotter.createFactory(**_currKwargs) )

	#Add some annotation colors + lower some of the font sizes
	_currKwargs = {"annotateVals":True, "annotateValsFontSize":10, "annotateValsStrFmt":"{:.1f}",
	               "annotateValsTextColor":['r','orange','green'], "colorBarLabelRotation":90,
	               "colorBarLocation":"right", "colorBarFontSize":10, "colorMapStr":"binary",
	               "colorMapMinVal":-1.0, "colorMapMaxVal":1.0,
	               "plotData":sqrMatrixA, "plotUpperTri":False,
	               "titleStr":None, "yLabelStr":None}
	outPlotters.append( secondTemplPlotter.createFactory(**_currKwargs) ) 

	return outPlotters


def _createMultiPlotter(inpPlotters):
	_currKwargs = {"constrainedLayout":True, "figHeightPerRow":2, "figWidthPerCol":3,
	               "nColsGrid":3, "plotters": inpPlotters}
	outPlotter = ppl.RectMultiPlotter(**_currKwargs)
	return outPlotter



if __name__ == '__main__':
	main()
