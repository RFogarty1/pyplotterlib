
import os
import unittest

import pyplotlib.standard.plotters as ppl

class TestSharedAxisPlotterSerialization(unittest.TestCase):

	def setUp(self):
		self.expected = _createStandardSharedAxisPlotter()
		self.tempFileName = "_tempSharedAxisPlotter.json"
		ppl.writePlotterToFile(self.expected, self.tempFileName)

	def tearDown(self):
		os.remove(self.tempFileName)

	def testReadAndWriteConsistent(self):
		""" Check reading/writing to file consistent for DoubleAxisPlotter """
		actPlotter = ppl.readPlotterFromFile(self.tempFileName)
		self.assertEqual(self.expected, actPlotter)

def _createStandardSharedAxisPlotter():
	lineKwargA = {"xLabelStr":"Here is a label"}
	lineKwargB = {"lineStyles":['None','-'],"yLimit":[10,24]}
	linePlotterA = ppl.LinePlotter(**lineKwargA)
	linePlotterB = ppl.LinePlotter(**lineKwargB)

	doubleAxisKwargs = {"independentYAxis":True, "independentXAxis":False,
	                    "allowTwoIndependentAxes":False,
	                    "plotters":[linePlotterA, linePlotterB]}
	outPlotter = ppl.DoubleAxisPlotter(**doubleAxisKwargs)
	return outPlotter 


