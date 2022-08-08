
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

#Registered for Serialization mainly for purposes of test code
@regHelp.registerForSerialization()
class BooleanPlotOption(SinglePlotOptionInter):

	def __eq__(self, other):
		if self.name != other.name:
			return False
		if self.value != other.value:
			return False

		return True

	def toJSON(self):
		return json.dumps({"class":str(self.__class__), "payload":{"name":self.name, "value":self.value}})

	@classmethod
	def fromJSON(cls, inpJSON):
		useDict = json.loads(inpJSON)
		return cls( useDict["payload"]["name"], useDict["payload"]["value"] )

#Behavior should be identical to the Boolean
@regHelp.registerForSerialization()
class StringPlotOption(BooleanPlotOption):
	pass


@regHelp.registerForSerialization()
class StringIterPlotOption(BooleanPlotOption):
	pass


@regHelp.registerForSerialization()
class IntPlotOption(BooleanPlotOption):
	pass

@regHelp.registerForSerialization()
class IntIterPlotOption(BooleanPlotOption):
	pass



@regHelp.registerForSerialization()
class FloatIterPlotOption(SinglePlotOptionInter):

	#Very similar to numpyIter case
	def __eq__(self, other):

		if self.name != other.name:
			return False

		if len(self.value) != len(other.value):
			return False

		if not np.allclose( np.array(self.value), np.array(other.value) ):
			return False

		return True

	#TODO: this is the standard toJSON/fromJSON; should factor out into a mixin or into SinglePlotOptionInter
	def toJSON(self):
		return json.dumps({"class":str(self.__class__), "payload":{"name":self.name, "value":self.value}})

	@classmethod
	def fromJSON(cls, inpJSON):
		useDict = json.loads(inpJSON)
		return cls( useDict["payload"]["name"], useDict["payload"]["value"] )


@regHelp.registerForSerialization()
class FloatIterOrSingleFloatOption(SinglePlotOptionInter):

	def __eq__(self, other):
		return True

	def toJSON(self):
		raise NotImplementedError("")

	@classmethod
	def fromJSON(cls, inpJSON):
		raise NotImplementedError("")


class ObjectIterPlotOption(SinglePlotOptionInter):

	def __eq__(self, other):
		raise NotImplementedError("")

	def toJSON(self):
		raise NotImplementedError("")

	@classmethod
	def fromJSON(cls, inpJSON):
		raise NotImplementedError("")

class NumpyIterPlotOption(SinglePlotOptionInter):

	def __eq__(self, other):
		if self.name != other.name:
			return False

		if len(self.value) != len(other.value):
			return False

		for (arrA,arrB) in it.zip_longest(self.value, other.value):
			if not np.allclose( np.array(arrA), np.array(arrB) ):
				return False

		return True

	def toJSON(self):
		#Note np arrays arent JSON-compatible; hence need to work with them as lists
		outArrays = [ np.array(x).tolist() for x in self.value ]
		return json.dumps({"class":str(self.__class__), "payload":{"name":self.name, "value":outArrays}})

	@classmethod
	def fromJSON(cls, inpJSON):
		useDict = json.loads(inpJSON)
		return cls( useDict["payload"]["name"], [np.array(x) for x in useDict["payload"]["value"]] )




