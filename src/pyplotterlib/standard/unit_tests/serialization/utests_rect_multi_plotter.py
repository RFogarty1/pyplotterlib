
import os
import unittest

import pyplotterlib.standard.plotters as ppl

class TestRectMultiPlotterSerialization(unittest.TestCase):

	def setUp(self):
		self.expected = _createStandardRectMultiPlotter()
		self.tempFileName = "_tempRectMultiPlotter.json"
		ppl.writePlotterToFile(self.expected, self.tempFileName)

	def tearDown(self):
		os.remove(self.tempFileName)

	def testReadAndWriteConsistent(self):
		""" Check reading/writing to file consistent for RectMultiPlotter """
		actPlotter = ppl.readPlotterFromFile(self.tempFileName)
		self.assertEqual(self.expected, actPlotter)


def _createStandardRectMultiPlotter():
	lineKwargA = {"xLabelStr":"Here is a label"}
	lineKwargB = {"lineStyles":['None','-'],"yLimit":[10,24]}
	linePlotterA = ppl.LinePlotter(**lineKwargA)
	linePlotterB = ppl.LinePlotter(**lineKwargB)

	rectPlotterKwargs = {"constrainedLayout":True, "figHeightPerRow":3,
	                     "nColsGrid":1, "plotters":[linePlotterA, linePlotterB]}
	outPlotter = ppl.RectMultiPlotter(**rectPlotterKwargs)
	return outPlotter 



