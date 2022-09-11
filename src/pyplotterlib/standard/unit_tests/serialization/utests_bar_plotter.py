
import os
import unittest

import pyplotterlib.standard.plotters as ppl

class TestBarPlotterSerialization(unittest.TestCase):

	def setUp(self):
		self.expected = _createStandardBarPlotter()
		self.tempFileName = "_tempFileBarPlotter.json"

		ppl.writePlotterToFile(self.expected, self.tempFileName)

	def tearDown(self):
		os.remove(self.tempFileName)

	def testReadAndWriteConsistent(self):
		actPlotter = ppl.readPlotterFromFile(self.tempFileName)
		self.assertEqual(self.expected, actPlotter)



def _createStandardBarPlotter():
	currKwargs = {"axisBorderMakeInvisible.top":True,
	"axisColorX":'red',
	"axisColorX_exclSpines":True,
	"axisColorY":'green',
	"dataLabels":["A","B","C"],
	"figSizeOnCreation":[10,6],
	"legendFractPosStart":[0.2,0.3],
	"legendLocStr":'best',
	"plotData1D": [ [1,2,3], [3,2,1] ],
	"plotHorizontally":True,
	"showLegend": True,
	"widthBars": 0.8,
	"widthInterSpacing": 1.6,
	"widthIntraSpacing": 0.2,
	"xLabelFractPos": [0.5,-0.2],
	"xLabelStr": "Here is an x-label",
	"xLimit": [0,24],
	"yLabelStr": "Here is a y-label",
	"yLimit": [50, 160]
	}

	return ppl.BarPlotter(**currKwargs)


