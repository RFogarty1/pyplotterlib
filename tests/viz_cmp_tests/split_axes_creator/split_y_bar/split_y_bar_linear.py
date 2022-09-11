
import itertools as it
import pyplotterlib.standard.plotters as plotters
import pyplotterlib.reg_testing.viz_diff.helpers as helpers


def main():
	cmdLineArgs = helpers.parseStdCommandLineArgs()
	templatePlotter = createTemplatePlotter()
	currKwargs = {"axisSizeLinear":True,
	              "legendPlotterGridCoords":[0,1], "plotter":templatePlotter,
	              "splitLinesDraw":True,
	              "yLimits":[ [0,15], [248,270]],
	              "ySpacingFract":0.02
	}
	              
	outPlotter = plotters.SplitAxisPlotterCreator(**currKwargs)

	currKwargs = helpers.getKwargDictFromCmdLineArgs(cmdLineArgs)
	helpers.createAndSavePlotForPlotter(outPlotter, **currKwargs)


def createTemplatePlotter():
	dataA = [10,8,12]
	dataB = [4, 256, 267]
	
	_plotOptsDict = {
	
	"dataLabels": ["SeriesA", "SeriesB"],
	"groupLabels": ["propA", "propB", "propC"],
	"figSizeOnCreation": [8,4],
	"plotData1D": [dataA, dataB],
	"plotHorizontally":False,
	"showLegend": True,
	"xLabelStr":"Test x-label",
	}

	outPlotter = plotters.BarPlotter(**_plotOptsDict)

	return outPlotter


if __name__ == '__main__':
	main()


