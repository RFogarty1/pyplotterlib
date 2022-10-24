
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


class FromPlotterMixin():

	@classmethod
	def fromPlotter(cls, inpPlotter):
		""" Create the plotter using options from inpPlotter.
		
		Args:
			inpPlotter: (PlotterInter) Should generally be the same type as the target, though doesnt have to be (see Notes for behaviour details).
		
		Returns:
			outPlotter: (PlotterInter)


		Notes:
			a) We dont explicitly copy anything by default. So a SimpleNamespace option-value on outPlotter will point to the same object as on inpPlotter. You may wish to use copy.deepcopy(outPlotter) for safety.
			b) outPlotter will set every relevant option it finds on inpPlotter. If an option is ONLY on inpPlotter, it will be ignored. If an option is ONLY on outPlotter, the default value will be used.
			c) w.r.t. point b); note that some options with the same name (e.g. "plotData") may mean different things on different plotters. Thus, care should be exercised if type(inpPlotter) does not match type(outPlotter)

		 
		"""
		outPlotter = cls()
		sharedOptNames = set(inpPlotter.optionNames).intersection(outPlotter.optionNames)

		optDict = dict()
		for optName in sharedOptNames:
			currVal = getattr(inpPlotter.opts,optName).value
			optDict[optName] = currVal

		outPlotter.setOptionVals(optDict)

		return outPlotter


def _getAxisEdges(inpAx):
	startX, startY, xLength, yLength = inpAx.get_position().bounds
	endX, endY = startX+xLength, startY+yLength
	return startX, startY, endX, endY



