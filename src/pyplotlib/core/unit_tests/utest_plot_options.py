
import copy
import unittest

import numpy as np

import pyplotlib.core.plot_options as tCode


class TestOptionsCol(unittest.TestCase):

	def setUp(self):
		self.nameA, self.nameB = "nameA", "nameB"
		self.valA, self.valB = True, False
		self.clsA, self.clsB = tCode.BooleanPlotOption , tCode.BooleanPlotOption
		self.createTestObjs()

	def createTestObjs(self):
		self.plotOptA = self.clsA(self.nameA, self.valA)
		self.plotOptB = self.clsB(self.nameB, self.valB)

		#Pass options in the opposite order for each; should NOT affect anything if coded up sensibly
		self.testObjA = tCode.OptionsCollection(options=[copy.deepcopy(self.plotOptA), copy.deepcopy(self.plotOptB)])
		self.testObjB = tCode.OptionsCollection(options=[copy.deepcopy(self.plotOptB), copy.deepcopy(self.plotOptA)])

	def testEqCmpEq(self):
		""" Two equal OptionsCollection instances should compare equal """
		self.assertEqual(self.testObjA, self.testObjB)

	def testNonEqCmpNonEq_LengthOptions(self):
		""" Two OptionsCollection instances with different length options should compare unequal """
		self.testObjB = tCode.OptionsCollection(options=[self.plotOptB])
		self.assertNotEqual(self.testObjA, self.testObjB)

	def testNonEqCmpNonEq_diffVals(self):
		""" Test OptionsCollection instances with different values on the options compare unequal """
		optA = getattr(self.testObjB.opts,self.nameA)
		optA.value = not(self.valA)
		self.assertNotEqual(self.testObjA, self.testObjB)

	def testToAndFromJSONConsistent(self):
		""" The .toJSON and .fromJSON should be able to be combined to copy an object """
		objA = self.testObjA
		objB = tCode.OptionsCollection.fromJSON( objA.toJSON() )
		self.assertEqual(objA, objB)


class TestBoolean(unittest.TestCase):

	def setUp(self):
		self.name = "test-name"
		self.value = False
		self.createTestObjs()

	def createTestObjs(self):
		self.testObjA = tCode.BooleanPlotOption(self.name, value=self.value)
		self.testObjB = copy.deepcopy(self.testObjA)

	def testEqCmpEq(self):
		""" Two equal BooleanPlotOption instances should compare equal """
		self.assertEqual(self.testObjA, self.testObjB)

	def testNonEqCmpNonEq_diffName(self):
		""" Two BooleanPlotOption with different .name should compare unequal """
		self.testObjB.name = self.testObjA.name + "ext"
		self.assertNotEqual(self.testObjA, self.testObjB)

	def testNonEqCmpNonEq_diffVal(self):
		""" Two BooleanPlotOption with different .value should compare unequal """
		self.testObjB.value = not(self.testObjA.value)
		self.assertNotEqual(self.testObjA, self.testObjB)

	def testToAndFromJsonEqual(self):
		""" Checking .toJSON and .fromJSON are consistent for BooleanPlotOption """
		self.testObjB = tCode.BooleanPlotOption.fromJSON(self.testObjA.toJSON())
		self.assertEqual(self.testObjA, self.testObjB)


class TestNumpyIter(unittest.TestCase):

	def setUp(self):
		self.name = "test-name"
		self.value = [ np.array([ [1,1], [2,4.14] ]), np.array([ [1,1], [2,8.23] ]) ]
		self.createTestObjs()

	def createTestObjs(self):
		self.testObjA = tCode.NumpyIterPlotOption(self.name, self.value)
		self.testObjB = copy.deepcopy(self.testObjA)

	def testEqCmpEq(self):
		""" Two equal NumpyIterPlotOption instances should compare equal """
		self.assertEqual(self.testObjA, self.testObjB)

	def testNonEqCmpNonEq_diffName(self):
		""" Two NumpyIterPlotOption with different .name should compare unequal """
		self.testObjB.name = self.testObjA.name + "extra-bit"
		self.assertNotEqual(self.testObjA, self.testObjB)

	def testNonEqCmpNonEq_diffLength(self):
		""" Two NumpyIterPlotOption with different numbers of arrays should compare unequal """
		self.testObjB.value.append(self.testObjA.value[0])
		self.assertNotEqual(self.testObjA, self.testObjB)

	def testNonEqCmpNonEq_diffValues(self):
		""" Two NumpyIterPlotOption with different values in the arrays should compare unequal """
		self.testObjB.value[1][0][0] += 2
		self.assertNotEqual(self.testObjA, self.testObjB)

	def testToAndFromJSONEqual(self):
		""" Checking .toJSON and .fromJSON are consistent for NumpyIterPlotOption """
		self.testObjB = tCode.NumpyIterPlotOption.fromJSON(self.testObjA.toJSON())
		self.assertEqual(self.testObjA, self.testObjB)



if __name__ == '__main__':
	unittest.main()
