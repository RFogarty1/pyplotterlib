
import copy
import json

import matplotlib.pyplot as plt

from . import json_transform as jsonTransHelp
from .serialization import json_io as jsonIoHelp

class PlotterInter(jsonTransHelp.JSONTransformInterface):

	#NOTE: This is really here mainly for testing + better demonstrating the interface
	#It SHOULD NOT be called directly by users
	def __init__(self, optsObj, commandObjs):
		self._options = optsObj
		self._commands = commandObjs
		self._scratchSpace = dict()

	def createPlot(self, **kwargs):
		useFactory = self.createFactory(**kwargs)
		useFactory._scratchSpace["outDict"] = dict()

		for command in self.commands:
			command.execute(useFactory)

		return useFactory._scratchSpace["outDict"]

	def createFactory(self, **kwargs):
		""" Returns a copy of self, with all options in **kwargs updated on the copy. Essentially a shorthand for newObj=copy.deepcopy(x); newObj.setOptionVals(kwargs)
		
		Args:
			kwargs: Keys correspond to those in self.opts (i.e. in the options object)
				 
		Returns
			outPlotter (PlotterInter): A copy of this object, with any requested option values updated
	 
		"""
		outPlotter = copy.deepcopy(self)
		outPlotter.setOptionVals(copy.deepcopy(kwargs)) #Don't want list kwargs to be modified in place; hence second copy
		return outPlotter


	def addOptionsObjs(self, optionsObjs):
		""" Add options to the plotter._options object. This is what generally holds things such as plotData and xLabel for example
		
		Args:
			optionObjs(iter of SinglePlotOptionInter):
				 
		"""
		for optObj in optionsObjs:
			self._options.addOption(optObj)

	def appendCommandObjs(self, commandObjs):
		""" Appends commands to the plotter
		
		Args:
			(iter of PlotCommand):
				 
		"""
		self._commands.extend(commandObjs)


	def setOptionVals(self, optVals):
		""" Set a group of options at once
		
		Args:
			optVals (dict): Keys are the names of each option. Can be found in self._options.names. Values are what to set them to. 
		
		Notes:
			i) If an option takes a namespace as its value, you can use dot-notation to change only a property of the namespace. e.g. {"showBorder.top":True} would set the .top attribute of showBorder to True 
		 
		"""


		if optVals is None:
			return None
		
		for key in optVals:
			currAttrKeys = key.split(".")
			currObj = getattr(self._options.opts, currAttrKeys[0])
			if len(currAttrKeys)==1:
				setattr(currObj, "value", optVals[key])
			else:
				currObj = getattr(currObj, "value")
				for idx,attrSubKey in enumerate(currAttrKeys[1:],start=1):
					if idx==len(currAttrKeys)-1:
						setattr(currObj, attrSubKey, optVals[key])
					else:
						raise NotImplementedError("Only allowed one nested namespace for now")

	#This makes it easier to directly alter the values on the options object
	@property
	def opts(self):
		return self._options.opts

	@property
	def optionNames(self):
		return self._options.names

	@property
	def commands(self):
		return self._commands

	def toJSON(self):
		commsJSON = [x.toJSON() for x in self._commands]
		optsJSON = self._options.toJSON()

		outDict = {"class": str(self.__class__),
		           "payload":{"options":optsJSON,
		                      "commands":commsJSON}}
		return json.dumps(outDict)

	@classmethod
	def fromJSON(cls, inpJSON):
		useDict = json.loads(inpJSON)
		optionsObj = jsonIoHelp.createInstanceFromJSON(useDict["payload"]["options"])
		commandObjs = [ jsonIoHelp.createInstanceFromJSON(x) for x in useDict["payload"]["commands"] ]

		return cls(optionsObj, commandObjs)

	def __eq__(self, other):
		if self._options != other._options:
			return False

		if len(self._commands) != len(other._commands):
			return False

		if self._commands != other._commands:
			return False

		return True


class SingleGraphPlotter(PlotterInter):

	def createPlot(self, axHandle=None, **kwargs):
		""" Creates a plot for a single graph, optionally using the supplied axis handle
		
		Args:
			axHandle (matplotlib axis handle): Optionally supply a handle to the axis you want to plot on. Otherwise a full figure will be created; supplying the axHandle allows multiple plots on a single figure
			kwargs: Names are those in self.opts, values are the values you want to set (they override current values for this function call)
				 
		Returns
			outDict (dict): Contents depend on the specific plotter used
	 
		"""
		useFactory = self.createFactory(**kwargs)
		useFactory._scratchSpace["outDict"] = dict()
		if axHandle is not None:
			useFactory._scratchSpace["axHandle"] = axHandle
			plt.sca(axHandle)

		for command in self.commands:
			command.execute(useFactory)

		return useFactory._scratchSpace["outDict"]


class MultiGraphPlotter(PlotterInter):

	def createPlot(self, axHandles=None, **kwargs):
		""" Combines multiple SingleGraphPlotter instances to create a grid of graphs
		
		Args:
			axHandle (iter of matplotlib axis handle): If handles are provided then plots are made on these axes; useful if you want to build the plotting grid with an external library (e.g. directly in matplotlib).
			kwargs: Names are those in self.opts, values are the values you want to set (they override current values for this function call)
				 
		Returns
			outDict (dict): Contents depend on the specific plotter used
	 
		"""
		useFactory = self.createFactory(**kwargs)
		useFactory._scratchSpace["outDict"] = dict()
		if axHandles is not None:
			useFactory._scratchSpace["axHandles"] = axHandles
			plt.sca(axHandle)

		for command in self.commands:
			command.execute(useFactory)

		return useFactory._scratchSpace["outDict"]

