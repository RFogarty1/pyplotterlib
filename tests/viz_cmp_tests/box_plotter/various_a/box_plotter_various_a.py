

import numpy as np

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
	_currKwargs = {"dataLabels":["a","b","c"],"fontSizeDefault":12 , "gridLinesShowY":True,
#	               "groupLabelTicksEveryN":1,
	               "showLegend":True,
	               "titleStr":"Title Str A", "xLabelStr":"Test x-string", "yLabelStr":"Test y-string"}
	templPlotter = ppl.BoxPlotter(**_currKwargs)

	#Create input values
	inpValsA = [ 1,3,4,2,3,8,5 ]
	inpValsB = [ 5,3,1,6,8,3 ]
	inpValsC = [ 8, 6, 4, 7 ]
	inpValsD = [ 4, 6, 5, 5, 4] 

	#Create a few plotters with varying properties
	outPlotters = list()

	#Single series plotter
	_currKwargs = { "groupLabels":["A", "B", "C"], "legendFractPosStart": [0.7,0.1],
	                "plotDataSingleSeries":[ inpValsA, inpValsB, inpValsC ], "titleStr":"Plot A" }
	outPlotters.append( templPlotter.createFactory(**_currKwargs) )

	#Single series with colors on it + a notch
	outPlotters.append(  outPlotters[0].createFactory(boxColorsOn=True, boxNotchOn=True, titleStr="Plot B")  )

	#Multi series with smaller font
	_currKwargs = {"fontSizeDefault":8, "legendFractPosStart":[0.4,0.1],
	               "plotDataMultiSeries":[  [inpValsA,inpValsB], [inpValsC, inpValsD] ], "titleStr":"Plot C" }
	outPlotters.append( outPlotters[-1].createFactory(**_currKwargs) )  

	#Multi series with horizontally plotted boxes
	_currKwargs = {"boxColorsOn":None, "boxNotchOn":False, "boxColorStrsInterSeries":['r','g'],
	               "groupLabelRotation":45, "groupLabels":["Hello", "There"], "legendFractPosStart":None,
	               "plotHorizontally":True,
	               "plotVertLinePositions":8,
	               "titleStr":"Plot D", "widthBoxes":0.5}
	outPlotters.append( outPlotters[-1].createFactory(**_currKwargs))

	#Simple with tick markers shown every 2 (rather than every 1)
	#Also dont show whiskers or outliers
	_currKwargs = { "groupLabels":["A", "B", "C"], "groupLabelTicksEveryN":2,"legendFractPosStart": [0.7,0.1],
	                "outliersShow":False, 
	                "plotDataSingleSeries":[ inpValsA, inpValsB, inpValsC ], "titleStr":"Plot A",
	                "plotHozLinePositions":6.5,
	                "whiskersShow":False }
	outPlotters.append( templPlotter.createFactory(**_currKwargs) )


	return outPlotters


def _createMultiPlotter(inpPlotters):
	_currKwargs = {"constrainedLayout":True, "figHeightPerRow":2, "figWidthPerCol":3,
	               "nColsGrid":3, "plotters": inpPlotters}
	outPlotter = ppl.RectMultiPlotter(**_currKwargs)
	return outPlotter



if __name__ == '__main__':
	main()
