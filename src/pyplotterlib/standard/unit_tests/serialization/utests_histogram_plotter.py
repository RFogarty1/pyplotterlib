
import os
import unittest

import pyplotterlib.standard.plotters as ppl

class TestHistogramSerialization(unittest.TestCase):

	def setUp(self):
		self.expected = _createStandardHistogramPlotter()
		self.tempFileName = "_tempHistoPlotter.json"
		ppl.writePlotterToFile(self.expected, self.tempFileName)

	def tearDown(self):
		os.remove(self.tempFileName)

	def testReadAndWriteConsistent(self):
		""" Check reading/writing to file is consistent for HistogramPlotter """
		actPlotter = ppl.readPlotterFromFile(self.tempFileName)
		self.assertEqual(self.expected, actPlotter)

def _createStandardHistogramPlotter():
	_edgesA = [1,2,3]
	_countsA = [5,7]
	_currKwargs = {"dataLabels":["A","B"],
	               "plotDataHisto": [ [_countsA, _edgesA] ],
	               "gridLinesShow":True,
	               "xLabelStr": "Here is an x-label"}
	return ppl.HistogramPlotter(**_currKwargs)




