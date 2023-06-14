
import unittest
import unittest.mock

import pyplotterlib.standard.annotations as annotationHelp
import pyplotterlib.standard.plot_commands as tCode

class TestDrawShadedAnnotationsDirectionVals(unittest.TestCase):

	def setUp(self):
		self.testComm = tCode.DrawShadedAnnotationsGeneric()
		self.plotterInstance = unittest.mock.Mock()
		self.direction = "vertical"
		self.createTestObjs()

	def createTestObjs(self):
		_shadeRange = [4,12]
		self.annotationOpt = annotationHelp.ShadedSliceAnnotation(_shadeRange, direction=self.direction)

	def _runTestFunct(self):
		self.testComm._addSingleAnnotation(self.plotterInstance, self.annotationOpt)	

	def testNoValueErrorFromStandardVal(self):
		self._runTestFunct()

	def testNoValueErrorFromUpperVal(self):
		self.direction = "horizontal".upper()
		self.createTestObjs()
		self._runTestFunct()

	def testValueErrorFromInvalidDirection(self):
		""" Test we get a ValueError for invalid values of the direction keyword """
		self.direction = "invalid value"
		self.createTestObjs()
		with self.assertRaises(ValueError):
			self._runTestFunct()



if __name__=='__main__':
	unittest.main()



