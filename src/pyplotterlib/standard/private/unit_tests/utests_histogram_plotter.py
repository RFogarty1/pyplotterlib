

import copy
import unittest

import numpy as np

import pyplotterlib.standard.private.histogram_plotter as tCode

class TestPlotDatOption(unittest.TestCase):

	def setUp(self):
		self.name = "test-name"
		self.edgesA = np.array([1,2,3]) 
		self.valsA = np.array([2.3, 3.6])
		self.edgesB = np.array([4,6,8,10])
		self.valsB = np.array([4.5, 7.3, 5.2])
		self.createTestObjs()

	def createTestObjs(self):
		vals = [ [self.edgesA, self.valsA],
		         [self.edgesB, self.valsB] ]
		self.testObjA = tCode.PlotDataHisto(name=self.name, value=vals)
		self.testObjB = copy.deepcopy(self.testObjA)

	def testEqCmpEq(self):
		""" Two equal PlotDataHisto options should compare equal """
		self.assertEqual(self.testObjA, self.testObjB)

	def testEqCmpEq_valsNone(self):
		""" Two PlotDataHisto should compare equal if both values are None """
		self.testObjA.value = None
		self.testObjB.value = None
		self.assertEqual(self.testObjA, self.testObjB)

	def testNonEqCmpNonEq_diffNames(self):
		""" Two PlotDataHisto with different name attributes should compare unequal """
		self.testObjB.name = self.name + "-extra-bit"
		self.assertNotEqual(self.testObjA, self.testObjB)

	def testNonEqCmpNonEq_diffLengths(self):
		""" Two PlotDataHisto with different lengths of data should compare unequal """
		self.testObjB.value = [ [self.edgesA, self.valsA] ]
		self.assertNotEqual(self.testObjA, self.testObjB)

	def testNonEqCmpNonEq_diffVals(self):
		""" Two PlotDataHisto with different values should compare unequal """
		objA = copy.deepcopy(self.testObjA)
		self.edgesB[-1] += 2.3
		self.createTestObjs()
		objB = self.testObjB
		self.assertNotEqual(objA, objB)

	def testNonEqCmpNonEq_oneIsNone(self):
		""" Two PlotDataHisto should compare unequal if one value is None """
		self.testObjB.value = None
		self.assertNotEqual(self.testObjA, self.testObjB)

	def testSerializationConsistent(self):
		""" toJSON() and fromJSON() should be consistent for PlotDataHisto """
		objA = self.testObjA
		objB = tCode.PlotDataHisto.fromJSON( objA.toJSON() )
		self.assertEqual(objA, objB)




