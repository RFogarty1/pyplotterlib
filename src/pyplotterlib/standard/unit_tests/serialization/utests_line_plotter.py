
import os
import unittest

import pyplotterlib.standard.plotters as ppl

class TestLinePlotterSerialization(unittest.TestCase):

	def setUp(self):
		self.expected = _createStandardLinePlotter()
		self.tempFileName = "_tempFileLinePlotter.json"

		ppl.writePlotterToFile(self.expected, self.tempFileName)

	def tearDown(self):
		os.remove(self.tempFileName)

	def testReadAndWriteConsistent(self):
		""" Check reading/writing to file consistent for LinePlotter """
		actPlotter = ppl.readPlotterFromFile(self.tempFileName)
		self.assertEqual(self.expected, actPlotter)


#Use some kind of value for as many properties as possible
def _createStandardLinePlotter():
	currKwargs = {
	
	"axisBorderMakeInvisible.right":True,
	"axisColorX":'red',
	"axisColorX_exclSpines":True,
	"axisColorY":'green',
	"dataLabels": ["a", "b"],
	"figSizeOnCreation": (20,10),
	"legendFractPosStart": [0.3,0.6],
	"legendLocStr": 'best',
	"lineColors": ['r', 'g'],
	"lineMarkerStyles":['x','o'],
	"lineStyles":['-','None'],
	"plotData": [  [[1,1],[2,4]], [ [4,20], [5,29] ] ],
	"showLegend":True,
	"xLabelFractPos": [0.5,-0.1],
	"xLabelStr": "Test x-label",
	"xLimit": [0,12],
	"yLabelFractPos": [-0.1,0.5],
	"yLabelStr": "y-label",
	"yLimit": [0,50]
	}

	return ppl.LinePlotter(**currKwargs)
