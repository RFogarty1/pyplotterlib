
import json
import unittest

import pyplotlib.core.serialization.register as regHelp

import pyplotlib.core.serialization.json_io as tCode

#Create some stubs with the expected interface
@regHelp.registerForSerialization()
class SingleLevelValidStub():
	
	def __init__(self, inpVal):
		self.inpVal = inpVal

	def toJSON(self):
		return json.dumps({"class": str(self.__class__), "payload":{"inpVal":self.inpVal}})

	@classmethod
	def fromJSON(cls, inpJSON):
		useDict = json.loads(inpJSON)
		return cls(useDict["payload"]["inpVal"])

	def __eq__(self, other):
		if self.inpVal != other.inpVal:
			return False
		return True

@regHelp.registerForSerialization()
class TwoLevelValidStub():
	
	def __init__(self, inpVal, singleLevelStub):
		self.inpVal = inpVal
		self.singleLevelStub = singleLevelStub

	def toJSON(self):
		secondLevelJSON = self.singleLevelStub.toJSON()
		return json.dumps({"class": str(self.__class__), "payload":{"inpVal":self.inpVal, "singleLevelStub": secondLevelJSON}})

	@classmethod
	def fromJSON(cls, inpJSON):
		useDict = json.loads(inpJSON)
		singleLevelStub = tCode.createInstanceFromJSON( useDict["payload"]["singleLevelStub"] )
		return cls(useDict["payload"]["inpVal"], singleLevelStub)

	def __eq__(self, other):
		if self.inpVal != other.inpVal:
			return False
		if self.singleLevelStub != other.singleLevelStub:
			return False
		return True


class TestCreateInstanceFromJSON(unittest.TestCase):

	def setUp(self):
		self.inpValA = 4
		self.inpValB = 6
		self.createTestObjs()

	def createTestObjs(self):
		self.singleLevelA = SingleLevelValidStub(self.inpValA)
		self.twoLevelA = TwoLevelValidStub(self.inpValB, self.singleLevelA)

	def testExpectedSingleLevelStub(self):
		""" Test createInstanceFromJSON gives expected object for stub with one level of toJSON/fromJSON """
		expObj = self.singleLevelA
		actObj = tCode.createInstanceFromJSON( self.singleLevelA.toJSON() )
		self.assertEqual(expObj, actObj)

	def testExpectedTwoLevelStub(self):
		""" Test createInstanceFromJSON gives expected object for stub with two levels of toJSON/fromJSON """
		expObj = self.twoLevelA
		actObj = tCode.createInstanceFromJSON( self.twoLevelA.toJSON() )
		self.assertEqual(expObj, actObj)
