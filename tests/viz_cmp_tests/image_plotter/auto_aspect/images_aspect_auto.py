
import copy
import itertools as it
import os

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


import pyplotterlib.standard.plotters as ppl
import pyplotterlib.reg_testing.viz_diff.helpers as helpers



def main():
	#Create the plotter to use
	imgA = mpimg.imread( os.path.join('..','flowers-compressed.jpg') )
	imgB = mpimg.imread( os.path.join('..','cookies.jpg') )
	plotterA, plotterB = _createPlottersAB(imgA,imgB)
	usePlotter = _createMultiPlotter(plotterA, plotterB)

	#
	cmdLineArgs = helpers.parseStdCommandLineArgs()
	currKwargs = {"saveExp":cmdLineArgs.saveExp, "saveAct":cmdLineArgs.saveAct, "expName":cmdLineArgs.expName, "actName":cmdLineArgs.actName}
	helpers.createAndSavePlotForPlotter(usePlotter, **currKwargs)


def _createPlottersAB(imgA, imgB):
	_currKwargs = {"aspectStr":"auto", "showTicksAndLabelsOnSides.bottom":False, "showTicksAndLabelsOnSides.left":False}
	templPlotter = ppl.ImagePlotter(**_currKwargs)

	plotterA = templPlotter.createFactory(plotDataImage=imgA, titleStr="Title A")
	plotterB = templPlotter.createFactory(plotDataImage=imgB, titleStr="Title B")

	return plotterA, plotterB


def _createMultiPlotter(plotterA, plotterB):
	plotterC = copy.deepcopy(plotterA)
	plotterC.setOptionVals({"titleStr":"Image C (Copy of A)"})
	plotters = [plotterA, plotterB, plotterC]

	_currKwargs = {"constrainedLayout":True,"figHeightPerRow":2, "figWidthPerCol":2,
	               "plotters":plotters, "nColsGrid":2}

	outPlotter = ppl.RectMultiPlotter(**_currKwargs)

	return outPlotter

#figHeightPerRow=2, figWidthPerCol=2, constrainedLayout=True, nColsGrid=2


if __name__ == '__main__':
	main()
