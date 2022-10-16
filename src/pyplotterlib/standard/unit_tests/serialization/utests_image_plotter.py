
import os
import unittest

import numpy as np

import pyplotterlib.standard.plotters as ppl


class TestImagePlotterSerialization(unittest.TestCase):

	def setUp(self):
		self.expected = _createStandardImagePlotter()
		self.tempFileName = "_tempImagePlotter.json"
		ppl.writePlotterToFile(self.expected, self.tempFileName)

	def tearDown(self):
		os.remove(self.tempFileName)

	def testReadAndWriteConsistent(self):
		""" Check reading/writing to file is consistent for ImagePlotter """
		actPlotter = ppl.readPlotterFromFile(self.tempFileName)
		self.assertEqual(self.expected, actPlotter)

def _createStandardImagePlotter():
	_data = np.zeros( (8,8) )
	_data[0][2], _data[1][4] = 55, 220

	_currKwargs = {"aspectStr":"auto","colorBarShow":True, "colorMapStr":"binary",
	               "plotDataImage":_data, "showTicksAndLabelsOnSides.bottom":False,
	               "showTicksAndLabelsOnSides.left":False}
	return ppl.ImagePlotter(**_currKwargs)


