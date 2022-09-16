
import matplotlib.pyplot as plt

import pyplotterlib.core.plot_command as pltCmdCoreHelp
import pyplotterlib.core.plot_options as pltOptCoreHelp
import pyplotterlib.core.serialization.register as serRegHelp

import pyplotterlib.standard.plotters as ppl

#Create the plotter itself
@serRegHelp.registerForSerialization()
class ExtendedLinePlotter(ppl.LinePlotter):

	def __init__(self, **kwargs):
		super().__init__() #Generates instance with same functionality as Parent class
		self.addOptionsObjs([VertLinePlotOption()])
		self.setOptionVals(kwargs)

		#I COULD just append the command, but will put it earlier for demo-reasons
		outCommands = self._commands
		outCommands.insert(-2, DrawVertLine()) #Now the third last command
		self._commands = outCommands


#Create option object
@serRegHelp.registerForSerialization()
class VertLinePlotOption(pltOptCoreHelp.FloatPlotOption):
    def __init__(self,name=None, value=None):
        self.name = "vertLinePos"
        self.value = value

#Create command object. Note that neither _name or _description are strictly required
@serRegHelp.registerForSerialization()
class DrawVertLine(pltCmdCoreHelp.PlotCommand):
    def __init__(self):
        self._name = "drawVertLine"
        self._description = "Draws a vertical line at a position given by the vertLinePos option"
    
    def execute(self, plotterInstance):
        linePos = getattr(plotterInstance.opts,"vertLinePos").value
        if linePos is None:
            return None
        plt.gca().axvline(x=linePos)




