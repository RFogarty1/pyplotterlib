
import json

from . import json_transform as jsonTransHelp

class PlotCommand(jsonTransHelp.JSONTransformInterface):
	""" Class representing a command to apply when creating a plot (e.g. "change the x-limit" might be an example)

	Attributes:
		name (str): Descriptive Name of the command
		description (str): Description of what the command does

	"""

	@property
	def name(self):
		return self._name

	@property
	def description(self):
		return self._description

	def execute(self, plotterInstance):
		""" Executes the command on the current plot, likely using options/data stored in plotterInstance
		
		Args:
			plotterInstance (PlotterInter):
				 
		"""
		raise NotImplementedError("")

	#name/description will generally be hard-coded into the initializer;
	def toJSON(self):
		outDict = {"class": str(self.__class__), "payload": {} }
		return json.dumps(outDict)

	@classmethod
	def fromJSON(cls, inpJSON):
		return cls() #Should almost ALWAYS be called without any values passed


	def __eq__(self, other):

		if self.toJSON() != other.toJSON():
			return False

		return True

