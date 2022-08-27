
import copy
import types
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

	def testToAndFromJsonEqual_NoneVals(self):
		""" Checking .toJSON and .fromJSON are consistent for NumpyIterPlotOption when value is None """
		self.testObjA.value = None
		self.testObjB = tCode.NumpyIterPlotOption.fromJSON(self.testObjA.toJSON())
		self.assertEqual(self.testObjA, self.testObjB)


class TestBoolNamespaceOption(unittest.TestCase):

	def setUp(self):
		self.name = "test-name"
		self.value = types.SimpleNamespace(x=True, y=False)
		self.createTestObjs()

	def createTestObjs(self):
		self.testObjA = tCode.BoolNamespaceOption(self.name, self.value)

	def testToAndFromJSONEqual(self):
		""" Checking .toJSON and .fromJSON are consistent for BoolNamespaceOption """
		self.testObjB = tCode.BoolNamespaceOption.fromJSON( self.testObjA.toJSON() )
		self.assertEqual(self.testObjA, self.testObjB)

class TestFloatIter(unittest.TestCase):

	def setUp(self):
		self.name = "test-name"
		self.value = [1.4,3.2,1.8]
		self.createTestObjs()

	def createTestObjs(self):
		self.testObjA = tCode.FloatIterPlotOption(self.name, self.value)
		self.testObjB = copy.deepcopy(self.testObjA)

	def testEqCmpEq(self):
		""" Two equal FloatIterPlotOption instances should compare equal """
		self.assertEqual(self.testObjA, self.testObjB)

	def testNonEqCmpNonEq_diffLength(self):
		""" Two FloatIterPlotOption instances with different value lengths should compare unequal """
		self.testObjB.value.append(5)
		self.assertNotEqual(self.testObjA, self.testObjB)

	def testNonEqCmpNonEq_diffValues(self):
		""" Two FloatIterPlotOption instances with different values should compare unequal """
		self.testObjB.value[1] += 2
		self.assertNotEqual(self.testObjA, self.testObjB)

	def testToAndFromJSONEqual(self):
		""" Checking .toJSON and .fromJSON are consistent for FloatIterPlotOption """
		self.testObjB = tCode.FloatIterPlotOption.fromJSON(self.testObjA.toJSON())
		self.assertEqual(self.testObjA, self.testObjB)

class TestFloatIterOrSingleFloat(unittest.TestCase):

	def setUp(self):
		self.name = "test-name"
		self.value = [1.3,2.4]
		self.createTestObjs()

	def createTestObjs(self):
		self.testObjA = tCode.FloatIterOrSingleFloatOption(self.name, self.value)
		self.testObjB = copy.deepcopy(self.testObjA)

	def testEqCmpEq_floatIters(self):
		""" Two equal FloatIterOrSingleFloatOption should compare equal (both with float-iter vals) """
		self.assertEqual(self.testObjA, self.testObjB)

	def testEqCmpEq_floatVals(self):
		""" Two equal FloatIterOrSingleFloatOption should compare equal (both with float vals) """
		self.value = 5.3
		self.createTestObjs()
		self.assertEqual(self.testObjA, self.testObjB)

	def testNonEqCmpNonEq_floatIterVsFloat(self):
		""" Two FloatIterOrSingleFloatOption should compare unequal if one has a float value and the other a float iter """
		self.testObjB.value = 5.4
		self.assertNotEqual(self.testObjA, self.testObjB)

	def testNonEqCmpNonEq_diffLengthFloatIters(self):
		""" Two unequal FloatIterOrSingleFloatOption should compare unequal when iter lengths vary """
		self.testObjB.value.append(5.8)
		self.assertNotEqual(self.testObjA, self.testObjB)

	def testNonEqCmpNonEq_diffValFloatIters(self):
		""" Two unequal FloatIterOrSingleFloatOption should compare unequal when iter values vary"""
		self.testObjA.value[0] += 1.5
		self.assertNotEqual(self.testObjA, self.testObjB)

	def testNonEqCmpNonEq_diffFloatVals(self):
		""" Two unequal FloatIterOrSingleFloatOption should compare unequal when float values vary (not float-iters) """
		self.value = 5.8
		self.createTestObjs()
		self.testObjB.value = self.value +0.5
		self.assertNotEqual(self.testObjA, self.testObjB)

	def testSerializationConsistent_floatVal(self):
		""" toJSON() and fromJSON() should give consistent results when using a single float """
		self.value = 0.8
		objA = self.testObjA
		objB = tCode.FloatIterOrSingleFloatOption.fromJSON( objA.toJSON() )
		self.assertEqual(objA, objB)

	def testSerializationConsistent_floatIter(self):
		""" toJSON() and fromJSON() should give consistent results when using an iter of floats """
		objA = self.testObjA
		objB = tCode.FloatIterOrSingleFloatOption.fromJSON( objA.toJSON() )
		self.assertEqual(objA, objB)


class TestObjectIterPlotOption(unittest.TestCase):

	def setUp(self):
		self.name = "test-name"
		self.value = [ tCode.FloatIterPlotOption("nameA", [1.2,1.3]),
		               tCode.FloatIterPlotOption("nameB", [4.5]) ]
		self.createTestObjs()

	def createTestObjs(self):
		self.testObjA = tCode.ObjectIterPlotOption(self.name, self.value)
		self.testObjB = copy.deepcopy(self.testObjA)

	def testEqCmpEq(self):
		""" Two equal ObjectIterPlotOption should compare equal """
		self.assertEqual(self.testObjA, self.testObjB)

	def testNonEqCmpNonEq_diffValObj(self):
		""" Two ObjectIterPlotOption should compare unequal if one iter contains a different-valued object """
		self.testObjB.value[1].value[0] += 1
		self.assertNotEqual(self.testObjA, self.testObjB)

	def testSerializationConsistent(self):
		""" ObjectIterPlotOption toJSON() and fromJSON() should give consistent results """
		objA = self.testObjA
		objB = tCode.ObjectIterPlotOption.fromJSON( objA.toJSON() )
		self.assertEqual(objA, objB)

	def testSerializationConsistent_valOfNone(self):
		""" ObjectIterPlotOption toJSON() and fromJSON() should give consistent results when the option value is None """
		objA = self.testObjA
		objA.value = None
		objB = tCode.ObjectIterPlotOption.fromJSON( objA.toJSON() )
		self.assertEqual(objA, objB)


class TestTwoDimObjectIterPlotOption(unittest.TestCase):

	def setUp(self):
		self.name = "test-name"
		listA = [ tCode.FloatIterPlotOption("nameA", [1.2,1.3]),
		          tCode.FloatIterPlotOption("nameB", [4.5]) ]
		listB = [ tCode.FloatIterPlotOption("nameC", [8,7]) ]
		self.value = [ listA, listB ]
		self.createTestObjs()

	def createTestObjs(self):
		self.testObjA = tCode.ObjectTwoDimIterPlotOption(self.name, self.value)
		self.testObjB = copy.deepcopy(self.testObjA)

	def testEqCmpEq(self):
		""" Two equal ObjectTwoDimIterPlotOption plot options should compare equal """
		self.assertEqual(self.testObjA, self.testObjB)

	def testNonEqCmpNonEq_diffValObj(self):
		""" Two ObjectTwoDimIterPlotOption should compare unequal if one contains a different-valued object """
		self.testObjB.value[0][1].value[0] += 2
		self.assertNotEqual(self.testObjA, self.testObjB)

	def testSerializationConsistent(self):
		""" ObjectTwoDimIterPlotOption toJSON() and fromJSON() should give consistent results """
		objA = self.testObjA
		objB = tCode.ObjectTwoDimIterPlotOption.fromJSON( objA.toJSON() )
		self.assertEqual(objA, objB)

	def testSerializationConsistent_valNone(self):
		""" ObjectTwoDimIterPlotOption toJSON() and fromJSON() should give consistent results when value is None """
		objA = self.testObjA
		objA.value = None
		objB = tCode.ObjectTwoDimIterPlotOption.fromJSON( objA.toJSON() )
		self.assertEqual(objA, objB)


class TestJsonTransObjPlotOption(unittest.TestCase):

	def setUp(self):
		self.name = "test-name"
		self.value = tCode.IntPlotOption("nameA", 4)
		self.createTestObjs()

	def createTestObjs(self):
		self.testObjA = tCode.JsonTransObjPlotOption(self.name ,self.value)
		self.testObjB = copy.deepcopy(self.testObjA)

	def testEqCmpEq(self):
		""" Two equal JsonTransObjPlotOption instances should compare equal"""
		self.assertEqual(self.testObjA, self.testObjB)

	def testNonEqCmpNonEq_diffValObj(self):
		""" Two JsonTransObjPlotOption with different valued objects should compare unequal """
		self.testObjB.value.value += 1
		self.assertNotEqual(self.testObjA, self.testObjB)

	def testSerializationConsistent(self):
		""" JsonTransObjPlotOption toJSON() and fromJSON() should give consistent results """
		objA = self.testObjA
		objB = tCode.JsonTransObjPlotOption.fromJSON( objA.toJSON() )
		self.assertEqual(objA, objB)


class TestIterOfFloatIterPlotOption(unittest.TestCase):

	def setUp(self):
		self.name = "test-name"
		self.value = [ [1.3,2.5], [3.2,6.8] ]
		self.createTestObjs()

	def createTestObjs(self):
		self.testObjA = tCode.IterOfFloatIterPlotOption(self.name, self.value)
		self.testObjB = copy.deepcopy(self.testObjA)

	def testEqCmpEq(self):
		""" Two equal IterOfFloatIterPlotOption instances should compare equal """
		self.assertEqual(self.testObjA, self.testObjB)

	def testNonEqCmpNonEq_diffVals(self):
		""" Two IterOfFloatIterPlotOption with different values should compare unequal"""
		self.testObjB.value[0][1] += 0.4
		self.assertNotEqual(self.testObjA, self.testObjB)

	def testNonEqCmpNonEq_diffLenVals(self):
		""" Two IterOfFloatIterPlotOption with different length float-iters should compare unequal """
		self.testObjB.value.append( [5] )
		self.assertNotEqual(self.testObjA, self.testObjB)

	def testSerializationConsistent(self):
		""" JsonTransObjPlotOption toJSON() and fromJSON() should give consistent results """
		objA = self.testObjA
		objB = tCode.IterOfFloatIterPlotOption.fromJSON( objA.toJSON() )
		self.assertEqual(objA, objB)

if __name__ == '__main__':
	unittest.main()
