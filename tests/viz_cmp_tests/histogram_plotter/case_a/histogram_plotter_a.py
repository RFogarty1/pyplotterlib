
import copy
import itertools as it
import os

import numpy as np

import pyplotterlib.standard.plotters as ppl
import pyplotterlib.reg_testing.viz_diff.helpers as helpers

def main():
	#Create the plotter to use
	usePlotter = _createPlotter()

	#
	cmdLineArgs = helpers.parseStdCommandLineArgs()
	currKwargs = {"saveExp":cmdLineArgs.saveExp, "saveAct":cmdLineArgs.saveAct, "expName":cmdLineArgs.expName, "actName":cmdLineArgs.actName}
	helpers.createAndSavePlotForPlotter(usePlotter, **currKwargs)


def _createPlotter():
	#Create the data
	edges = np.linspace(-2,2,num=20)
	countsA = [ 1,  3,  5,  6,  8, 15, 13, 24, 19, 15, 28, 11, 10,  8, 10, 11,  5, 2,  1]
	countsB = [ 3,  5,  5, 10, 11, 10, 15, 15, 16, 17, 15, 19, 14, 12, 11,  8,  4, 3,  2]

	#Create the template plotter
	_currKwargs = {"dataLabels":["Data A", "Data B"], "fontSizeDefault":12, "showLegend":True,
	               "xLabelStr":"Test x-label", "yLabelStr":"Test y-label"}
	templPlotter = ppl.HistogramPlotter(**_currKwargs)


	#Create slightly different histogram plotters
	_kwargsA = {"gridLinesShowX":True, "plotDataHisto":[ [countsA, edges] ], "plotHozLineColorStrs":'black', "plotHozLinePositions":20}
	_kwargsB = {"gridLinesShowY":True, "plotDataHisto":[ [countsB, edges] ], "plotVertLineColorStrs":'black', "plotVertLinePositions":-0.5,
	            "interBarFractSpace":0.2}

	plotterA = templPlotter.createFactory(**_kwargsA)
	plotterB = templPlotter.createFactory(**_kwargsB)

	#Create the output multi plotter
	_currKwargs = {"constrainedLayout":True, "figHeightPerRow":2, "figWidthPerCol":4,
	               "plotters":[plotterA,plotterB], "nColsGrid":2}
	outPlotter = ppl.RectMultiPlotter(**_currKwargs)

	return outPlotter



if __name__ == '__main__':
	main()
