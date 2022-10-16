
import os
import unittest

import pyplotterlib.standard.plotters as ppl


class TestSplitAxisCreatorSerialization(unittest.TestCase):

	def setUp(self):
		self.expected = _createStandardSplitAxisCreator()
		self.tempFileName = "_tempSplitAxisCreator.json"
		ppl.writePlotterToFile(self.expected, self.tempFileName)

	def tearDown(self):
		os.remove(self.tempFileName)

	def testReadAndWriteConsistent(self):
		""" Check reading/writing to a file is consistent for SplitAxisPlotterCreator """
		actPlotter = ppl.readPlotterFromFile(self.tempFileName)
		self.assertEqual(self.expected, actPlotter)

	def testReadAndWriteConsistent_noPlotter(self):
		""" Check reading/writing consistent for SplitAxisPlotterCreator without a plotter kwarg set """
		self.expected.setOptionVals({"plotter":None})
		ppl.writePlotterToFile(self.expected, self.tempFileName)
		actPlotter = ppl.readPlotterFromFile(self.tempFileName)
		self.assertEqual(self.expected, actPlotter)


def _createStandardSplitAxisCreator():
	lineKwargA = {"xLabelStr":"Here is a label"}
	linePlotter = ppl.LinePlotter(**lineKwargA)

	splitCreatorKwargs = {"plotter":linePlotter, "splitLinesAngle":35,
	                      "splitLinesDraw":True}
	outPlotter = ppl.SplitAxisPlotterCreator(**splitCreatorKwargs)
	return outPlotter


