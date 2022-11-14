
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
	templImage = _getTemplateImage()
	colorMaps = ["viridis", "inferno", "Blues", "Greys", "hsv", "jet"]

	plotters = _createPlottersForColorMaps(templImage, colorMaps)
	usePlotter = _createMultiPlotter(plotters)

	#
	cmdLineArgs = helpers.parseStdCommandLineArgs()
	currKwargs = {"saveExp":cmdLineArgs.saveExp, "saveAct":cmdLineArgs.saveAct, "expName":cmdLineArgs.expName, "actName":cmdLineArgs.actName}
	helpers.createAndSavePlotForPlotter(usePlotter, **currKwargs)


def _getTemplateImage():
	startImage = mpimg.imread( os.path.join('..','flowers-grayscaled.jpg') )
	oneDimGray = startImage[:,:,0]
	return oneDimGray


def _createPlottersForColorMaps(templImage, colorMaps):
	_currKwargs = {"colorBarShow":True, "plotDataImage":templImage,
	               "showTicksAndLabelsOnSides.bottom":False, "showTicksAndLabelsOnSides.left":False}
	templPlotter = ppl.ImagePlotter(**_currKwargs)

	outPlotters = list()
	for colorStr in colorMaps:
		currPlotter = templPlotter.createFactory(colorMapStr=colorStr, titleStr=colorStr)
		outPlotters.append( currPlotter )

	#Randomly modify a couple; want to test a few more features
	_currKwargs = {"colorBarLocation":"bottom", "colorBarLabel":"Test Label", "colorMapMaxVal":500,
	               "colorMapMinVal":100}
	outPlotters[-1].setOptionVals(_currKwargs)

	return outPlotters


def _createMultiPlotter(inpPlotters):
	_currKwargs = {"constrainedLayout":True, "figHeightPerRow":2, "figWidthPerCol":3,
	               "nColsGrid":3, "plotters": inpPlotters}
	outPlotter = ppl.RectMultiPlotter(**_currKwargs)
	return outPlotter



if __name__ == '__main__':
	main()
