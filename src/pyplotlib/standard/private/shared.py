
import json
from ...core.serialization import json_io as jsonIoHelp


class FromJsonMixin():

	@classmethod
	def fromJSON(cls, inpJSON):
		useDict = json.loads(inpJSON)
		outObj = cls()
		optionsObj = jsonIoHelp.createInstanceFromJSON(useDict["payload"]["options"])
		commandObjs = [ jsonIoHelp.createInstanceFromJSON(x) for x in useDict["payload"]["commands"] ]

		outObj._options = optionsObj
		outObj._commands = commandObjs
		return outObj



def _getAxisEdges(inpAx):
	startX, startY, xLength, yLength = inpAx.get_position().bounds
	endX, endY = startX+xLength, startY+yLength
	return startX, startY, endX, endY



