
import json

from . import register as regHelp

def createInstanceFromJSON(inpJSON):
	""" Creates an instance from a json string input
	
	Args:
		inpJSON (str): JSON format, which will have been generated from a .toJSON() instance method. "class" key will map to the required class
			 
	Returns
		outInstance (JSONTransformInterface): Instance of the class in "class" key
 
	"""
	useDict = json.loads(inpJSON)
	useCls = regHelp._SERIALIZATION_REGISTER[ useDict["class"] ]
	return useCls.fromJSON(inpJSON)



