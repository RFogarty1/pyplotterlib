
import copy
import json
import types
import unittest

#import pyplotlib.core.serialization.json_io as jsonIOHelp
import pyplotterlib.core.serialization.register as regHelp

import pyplotterlib.core.plot_options as plotOptCoreHelp
import pyplotterlib.core.plot_command as plotCmdHelp

import pyplotterlib.core.plotters as tCode


_EMBED_VAL = 6

class NamespaceOptStub(plotOptCoreHelp.SinglePlotOptionInter):
	
	def __init__(self, name=None, value=None):
		self.name = "testStub" if name is None else name
		self.value = types.SimpleNamespace(embeddedVal=_EMBED_VAL) if value is None else value

	def __eq__(self, other):
		if self.name != other.name:
			return False
		if self.value.embeddedVal != other.value.embeddedVal:
			return False
		return True

@regHelp.registerForSerialization()
class SetValInOutDictCommand(plotCmdHelp.PlotCommand):

	def __init__(self):
		pass

	def execute(self, plotterInstance):
		plotterInstance._scratchSpace["outDict"]["test_output"] = plotterInstance.opts.testStub.value.embeddedVal

	def toJSON(self):
		return json.dumps({"class": str(self.__class__) ,"payload":dict()})

	#No attributes = we dont really need to do anything
	@classmethod
	def fromJSON(cls, inpJSON):
		return cls()

	def __eq__(self, other):
		if self.__class__ != other.__class__:
			return False
		return True

class TestPlotterInterface(unittest.TestCase):

	def setUp(self):
		self.optionA = NamespaceOptStub()
		self.optionB = plotOptCoreHelp.StringPlotOption(name="testStrName")
		self.optObj = plotOptCoreHelp.OptionsCollection(options=[self.optionA, self.optionB])
		self.commands = [1] #No need to use ACTUAL command objects
		self.createTestObjs()

	def createTestObjs(self):
		self.plotter = tCode.PlotterInter(self.optObj, self.commands)
		self.optsCopy = copy.deepcopy(self.optObj)

	#Note - assumes self.optObj is attached to self.plotter (as opposed to a copy of it)
	def testAddOptionsObjs(self):
		""" addOptionsObj should lead to additional options """
		expObj = self.optsCopy
		expObj.addOption( plotOptCoreHelp.BooleanPlotOption() )
		self.assertNotEqual(expObj, self.optObj)
		self.plotter.addOptionsObjs( [plotOptCoreHelp.BooleanPlotOption()] )
		self.assertEqual(expObj, self.optObj)

	def testSetOptionVals_stringChange(self):
		""" setOptionVals should modify value for a string-based option """
		self.optsCopy.opts.testStrName.value = "new-str"
		self.assertNotEqual(self.optsCopy, self.optObj)
		self.plotter.setOptionVals({"testStrName":self.optsCopy.opts.testStrName.value})
		self.assertEqual(self.optsCopy, self.optObj)

	def testSetOptionVals_NamespaceChange(self):
		""" setOptionVals should modify value for a namespace-based option """
		self.optsCopy.opts.testStub.value.embeddedVal += 2
		self.assertNotEqual(self.optsCopy, self.optObj)
		self.plotter.setOptionVals({"testStub.embeddedVal":self.optsCopy.opts.testStub.value.embeddedVal})
		self.assertEqual(self.optsCopy, self.optObj)

	def testAddCommandObjs(self):
		""" appendCommandObjs should add to the end of .commands """
		extraComms = [4,3]
		expComms = [1,4,3]
		self.assertNotEqual(expComms, self.plotter.commands)
		self.plotter.appendCommandObjs(extraComms)
		self.assertEqual(expComms, self.plotter.commands)

	def testCreateFactory_noKwargs(self):
		""" createFactory should return an identical copy (no options changed) when called with no keywords """
		newObj = self.plotter.createFactory()
		self.assertEqual(newObj._options, self.plotter._options)

	def testCreateFactory_newStrVal(self):
		""" createFactory(**kwargs) should return a copy with the relevant option values updated """
		newObj = self.plotter.createFactory( testStrName="new-str-here" )
		self.assertNotEqual( newObj._options, self.plotter._options )
		self.plotter.setOptionVals({"testStrName":"new-str-here"})
		self.assertEqual( newObj._options, self.plotter._options )

	def testCreatePlot_expectedOutput(self):
		""" createPlot should output a dictionary which can be modified by any command object """
		targCommand = SetValInOutDictCommand()
		self.plotter._commands = [targCommand]
		output = self.plotter.createPlot()
		expVal = _EMBED_VAL
		self.assertEqual(output["test_output"], expVal)

	def testCreatePlot_outputModdedByKwargs(self):
		""" createPlot should create an output which is sensitive to the value of kwargs """
		expVal = 32
		self.plotter.opts.testStub.value.embeddedVal = expVal
		self.plotter._commands = [SetValInOutDictCommand()]
		output = self.plotter.createPlot()
		self.assertEqual(output["test_output"], expVal)

	def testToAndFromJson(self):
		""" toJSON/fromJSON should be consistent for PlotterInterface """
		_currOpt = plotOptCoreHelp.StringPlotOption(name="testStrName")
		expOpts = plotOptCoreHelp.OptionsCollection(options=[_currOpt])
		expCommands = [SetValInOutDictCommand()]
		initPlotter = tCode.PlotterInter(expOpts, expCommands)
		outPlotter = tCode.PlotterInter.fromJSON( initPlotter.toJSON() )

		self.assertEqual(expCommands, outPlotter.commands)
		self.assertEqual(expOpts, outPlotter._options)

