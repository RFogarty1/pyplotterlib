
import os
import unittest

import pyplotlib.standard.plotters as ppl

class TestSplitAxisPlotterSerialization(unittest.TestCase):

	def setUp(self):
		self.expected = _createStandardSplitAxisPlotter()
		self.tempFileName = "_tempSplitAxisPlotter.json"
		ppl.writePlotterToFile(self.expected, self.tempFileName)

	def tearDown(self):
		os.remove(self.tempFileName)

	def testReadAndWriteConsistent(self):
		""" Check reading/writing to a file is consistent for SplitAxisPlotter """
		actPlotter = ppl.readPlotterFromFile(self.tempFileName)
		self.assertEqual(self.expected, actPlotter)


def _createStandardSplitAxisPlotter():
	lineKwargA = {"xLabelStr":"Here is a label"}
	lineKwargB = {"lineStyles":['None','-'],"yLimit":[10,24]}
	linePlotterA = ppl.LinePlotter(**lineKwargA)
	linePlotterB = ppl.LinePlotter(**lineKwargB)

	plotterGrid = [ [linePlotterA, linePlotterB] ]

	splitPlotterKwargs = {"fractsY": [ 0.4, 0.6 ],
	                      "plotterGrid": plotterGrid}

	outPlotter = ppl.SplitAxisPlotter(**splitPlotterKwargs)
	return outPlotter 





