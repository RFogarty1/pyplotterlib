
import itertools as it
import json
import types

import numpy as np

from . import json_transform as jsonTransHelp
from .serialization import register as regHelp
from .serialization import json_io as jsonIoHelp

@regHelp.registerForSerialization()
class OptionsCollection(jsonTransHelp.JSONTransformInterface):
	""" An object for holding a group of options objects

	Attributes:
		opts: Allows access to individual options using dot notation and their .name attribute. E.g. *.opts.xLim.value = [1,2], for a PlotOption with name="xLim"

	"""

	def __init__(self, options=None):
		""" Initializer
		
		Args:
			options (iter of SinglePlotOptionInter):
				 
		"""
		self._options = list()
		if options is not None:
			for opt in options:
				self.addOption(opt)


	def addOption(self, inpOption):
		""" Add a SinglePlotOptionInter option to this object
		
		Args:
			inpOption (SinglePlotOptionInter):
		
		Raises:
			ValueError: If adding an SinglePlotOptionInter object with .name which is already present
 
		"""
		inpName = inpOption.name
		if inpName not in self.names:
			self._options.append(inpOption)

	def toJSON(self):
		outDict = {"class": str(self.__class__)}
		optsJSON = [x.toJSON() for x in self._options]
		outDict["payload"] = {"options":optsJSON}
		return json.dumps(outDict)


	@classmethod
	def fromJSON(cls, inpJSON):
		useDict = json.loads(inpJSON)
		optsDict = useDict["payload"]
		optionsObjs = [ jsonIoHelp.createInstanceFromJSON(x) for x in optsDict["options"] ]
		return cls(options=optionsObjs)

	@property
	def names(self):
		return sorted([x.name for x in self._options])

	@property
	def opts(self):
		sortedNames = sorted(self.names)
		sortedOpts = sorted(self._options, key=lambda x:x.name)
		return types.SimpleNamespace(**{name:obj for name,obj in it.zip_longest(sortedNames, sortedOpts)})

	def __eq__(self, other):
		if len(self.names) != len(other.names):
			return False

		optsA = sorted(self._options, key=lambda x:x.name)
		optsB = sorted(other._options, key=lambda x:x.name)

		if optsA != optsB:
			return False

		return True


#Individual plot option interface + templates below
class SinglePlotOptionInter(jsonTransHelp.JSONTransformInterface):
	""" 

	Attributes:
		name (str): The name of the option (e.g. xLim)
		value (Any type): The value for the option. (e.g. [10, 25] might be the value of xLim)

	"""
	#Should generally be overwritten to give a default value to self.name
	def __init__(self, name=None, value=None):
		self.name = str(name)
		self.value = value

	def toJSON(self):
		return json.dumps({"class":str(self.__class__), "payload":{"name":self.name, "value":self.value}})

	@classmethod
	def fromJSON(cls, inpJSON):
		useDict = json.loads(inpJSON)
		return cls( useDict["payload"]["name"], useDict["payload"]["value"] )

	def __eq__(self, other):
		if self.name != other.name:
			return False
		if self.value != other.value:
			return False

		return True


#Registered for Serialization mainly for purposes of test code
@regHelp.registerForSerialization()
class BooleanPlotOption(SinglePlotOptionInter):
	pass

@regHelp.registerForSerialization()
class StringPlotOption(SinglePlotOptionInter):
	pass


@regHelp.registerForSerialization()
class StringIterPlotOption(SinglePlotOptionInter):
	pass


@regHelp.registerForSerialization()
class IntPlotOption(SinglePlotOptionInter):
	pass

@regHelp.registerForSerialization()
class IntIterPlotOption(SinglePlotOptionInter):
	pass

@regHelp.registerForSerialization()
class IntOrIntIterPlotOption(SinglePlotOptionInter):
	pass


@regHelp.registerForSerialization()
class JsonTransObjPlotOption(SinglePlotOptionInter):

	def toJSON(self):
		if self.value is None:
			embeddedVal = None
		else:
			embeddedVal = self.value.toJSON()
		return json.dumps({"class":str(self.__class__), "payload":{"name":self.name, "value":embeddedVal}})

	@classmethod
	def fromJSON(cls, inpJSON):
		useDict = json.loads(inpJSON)
		if useDict["payload"]["value"] is None:
			value = None
		else:
			value = jsonIoHelp.createInstanceFromJSON( useDict["payload"]["value"] )
		return cls( useDict["payload"]["name"], value)



@regHelp.registerForSerialization()
class IterOfFloatIterPlotOption(SinglePlotOptionInter):
	

	def __eq__(self, other):
		if self.name != other.name:
			return False

		if (self.value is None) and (other.value is None):
			return True
		elif (self.value is None) or (other.value is None):
			return False


		if len(self.value) != len(other.value):
			return False

		for valsA, valsB in zip(self.value,other.value):
			if not _areTwoFloatItersEqual(valsA, valsB):
				return False

		return True

@regHelp.registerForSerialization()
class FloatPlotOption(SinglePlotOptionInter):

	def __eq__(self, other):
		if self.name != other.name:
			return False

		if (self.value is None) and (other.value is None):
			return True
		elif (self.value is None) or (other.value is None):
			return False

		return _areTwoFloatItersEqual([self.value], [other.value])


@regHelp.registerForSerialization()
class FloatIterPlotOption(SinglePlotOptionInter):

	#Very similar to numpyIter case
	def __eq__(self, other):

		if self.name != other.name:
			return False

		if (self.value is None) and (other.value is None):
			return True
		elif (self.value is None) or (other.value is None):
			return False

		return _areTwoFloatItersEqual(self.value, other.value)



def _areTwoFloatItersEqual(iterA, iterB):
	if len(iterA) != len(iterB):
		return False

	if not np.allclose( np.array(iterA), np.array(iterB) ):
		return False

	return True



@regHelp.registerForSerialization()
class FloatIterOrSingleFloatOption(SinglePlotOptionInter):

	def __eq__(self, other):
		#First check for None conditions
		if (self.value is None) and (other.value is None):
			return True
		elif (self.value is None) or (other.value is None):
			return False

		#Figure out if vals iterable
		aIsIter = _isIter(self.value)
		bIsIter = _isIter(other.value)

		#If not both the same type; return false
		if aIsIter is not bIsIter:
			return False

		#Run the equality check for each type
		if aIsIter:
			return _areTwoFloatItersEqual(self.value, other.value)
		else:
			if not np.allclose( np.array([self.value]), np.array([other.value]) ):
				return False

		return True


def _isIter(inpObj):
	try:
		iter(inpObj)
	except TypeError:
		return False
	else:
		return True


@regHelp.registerForSerialization()
class ObjectIterPlotOption(SinglePlotOptionInter):

	def toJSON(self):
		if self.value is None:
			outPayloads = None
		else:
			outPayloads = [ x.toJSON() for x in self.value ]

		return json.dumps({"class":str(self.__class__), "payload":{"name":self.name, "value":outPayloads}})

	@classmethod
	def fromJSON(cls, inpJSON):
		useDict = json.loads(inpJSON)
		if useDict["payload"]["value"] is None:
			objs = None
		else:
			objs = [ jsonIoHelp.createInstanceFromJSON(x) for x in useDict["payload"]["value"] ]
		return cls( useDict["payload"]["name"], objs )


@regHelp.registerForSerialization()
class ObjectTwoDimIterPlotOption(SinglePlotOptionInter):

	def toJSON(self):
		if self.value is None:
			outVal = None
		else:
			outVal = self._generateOutPayloadIfValNotNone()

		return json.dumps({"class":str(self.__class__), "payload":{"name":self.name, "value":outVal}})


	def _generateOutPayloadIfValNotNone(self):
		outVal = list()
		for rowIdx, unused in enumerate(self.value):
			currList = list()
			for colIdx, unused in enumerate(self.value[rowIdx]):
				 currList.append( self.value[rowIdx][colIdx].toJSON() )
			outVal.append(currList)
		return outVal

	@classmethod
	def fromJSON(cls, inpJSON):
		useDict = json.loads(inpJSON)
		if useDict["payload"]["value"] is None:
			objs = None
		else:
			objs = cls._generateInpPayloadIfNotNone(inpJSON)

		return cls( useDict["payload"]["name"], objs )

	@classmethod
	def _generateInpPayloadIfNotNone(self, inpJSON):
		useDict = json.loads(inpJSON)
		objs = list()
		for rowIdx, currRow in enumerate(useDict["payload"]["value"]):
			currList = [ jsonIoHelp.createInstanceFromJSON(x) for x in currRow ]
			objs.append(currList)

		return objs	


class NumpyArrayPlotOption(SinglePlotOptionInter):

	def __eq__(self, other):

		#
		if self.name != other.name:
			return False

		#
		if self.value is None:
			if other.value is None:
				return True
			else:
				return False

		#
		if self.value.shape != other.value.shape:
			return False

		if not np.allclose( self.value, other.value ):
			return False

		return True

	def toJSON(self):
		#Note np arrays arent JSON-compatible; hence need to work with them as lists
		if self.value is None:
			outVal = None
		else:
			outVal = self.value.tolist()

		return json.dumps({"class":str(self.__class__), "payload":{"name":self.name, "value":outVal}})

	@classmethod
	def fromJSON(cls, inpJSON):
		useDict = json.loads(inpJSON)
		if useDict["payload"]["value"] is None:
			outVal = None
		else:
			outVal = np.array(useDict["payload"]["value"])

		return cls( useDict["payload"]["name"], outVal )



class NumpyIterPlotOption(SinglePlotOptionInter):

	def __eq__(self, other):
		if self.name != other.name:
			return False

		#TODO: likely factor this into a function
		if (self.value is None) and (other.value is None):
			return True
		elif (self.value is None) or (other.value is None):
			return False

		if len(self.value) != len(other.value):
			return False

		for (arrA,arrB) in it.zip_longest(self.value, other.value):
			if not np.allclose( np.array(arrA), np.array(arrB) ):
				return False

		return True

	def toJSON(self):
		#Note np arrays arent JSON-compatible; hence need to work with them as lists
		if self.value is None:
			outArrays = None
		else:
			outArrays = [ np.array(x).tolist() for x in self.value ]

		return json.dumps({"class":str(self.__class__), "payload":{"name":self.name, "value":outArrays}})

	@classmethod
	def fromJSON(cls, inpJSON):
		useDict = json.loads(inpJSON)
		if useDict["payload"]["value"] is None:
			outVal = useDict["payload"]["value"]
		else:
			outVal = [np.array(x) for x in useDict["payload"]["value"]]

		return cls( useDict["payload"]["name"], outVal )

@regHelp.registerForSerialization()
class BoolNamespaceOption(SinglePlotOptionInter):

	def toJSON(self):
		outDict = self.value.__dict__
		return json.dumps({"class":str(self.__class__), "payload":{"name":self.name, "value":outDict}})

	@classmethod
	def fromJSON(cls, inpJSON):
		useDict = json.loads(inpJSON)
		return cls( useDict["payload"]["name"], types.SimpleNamespace(**useDict["payload"]["value"]) )


