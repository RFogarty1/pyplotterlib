
""" Module for dealing with objects containing details of various annotations (used to specify details of how to annotate plots) """

from ..core import json_transform as jsonTransHelp
from ..core.serialization import register as serializationReg

@serializationReg.registerForSerialization()
class TextAnnotation(jsonTransHelp.JSONTransformInterface):
	""" Object representing data for a simple text annotation on a plot (which can include an arrow too)

	Attributes:
		textVal (str): String to write
		textPos (float,float): The position of the text. By default should be in terms of the x/y data.
		arrowPos (float,float): The position of the arrow head. By default should be in terms of the x/y data
		arrowCoordSys (str): The co-ordinate system for the arrow (default is 'data')
		textCoordSys (str): The co-ordinate system for the text (default is 'data')
		arrowPropHooks (dict): Dict of options for passing to arrowprops in matplotlib .annotate method
		annotateMplHooks (dict): Dict of options for keyword/value pairs to pass to matplotlib .annotate method. Generally will be for things like controlling the font. 
		fontSize (int): Size of the font

	Note:
		Commands use matplotlib.pyplot.annotate as the backend. Thus, options documented there largely map to this object:
		https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.annotate.html

	"""

	def __init__(self, textVal=None, textPos=None, arrowPos=None, arrowCoordSys='data', textCoordSys='data',
	             arrowPropHooks=None, annotateMplHooks=None, fontSize=None):
		""" Initializer
		
		Args:
			textVal (str): String to write
			textPos (float,float): The position of the text. By default should be in terms of the x/y data.
			arrowPos (float,float): The position of the arrow head. By default should be in terms of the x/y data
			arrowCoordSys (str): The co-ordinate system for the arrow (default is 'data')
			textCoordSys (str): The co-ordinate system for the text (default is 'data')
			arrowPropHooks (dict): Dict of options for passing to arrowprops in matplotlib .annotate method
			annotateMplHooks (dict): Dict of options for keyword/value pairs to pass to matplotlib .annotate method. Generally will be for things like controlling the font. 
			fontSize (int): Size of the font
 
		"""
		self.textVal = textVal
		self.textPos = textPos
		self.arrowPos = arrowPos
		self.arrowCoordSys = arrowCoordSys
		self.textCoordSys = textCoordSys
		self.arrowPropHooks = arrowPropHooks
		self.annotateMplHooks = annotateMplHooks
		self.fontSize = fontSize

	def _getPayloadDict(self):
		outDict = {"textVal":self.textVal, "textPos":self.textPos, "arrowPos":self.arrowPos,
		           "arrowCoordSys":self.arrowCoordSys, "textCoordSys":self.textCoordSys,
		           "arrowPropHooks":self.arrowPropHooks, "annotateMplHooks":self.annotateMplHooks,
		           "fontSize":self.fontSize}
		return outDict
	
	def toJSON(self):
		return json.dumps({"class":str(self.__class__), "payload":self._getPayloadDict()})

	@classmethod
	def fromJSON(cls, inpJSON):
		useDict = json.loads(inpJSON)
		return cls( **useDict["payload"] )

