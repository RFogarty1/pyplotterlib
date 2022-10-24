
import argparse

from ...standard import plotters as ppl

#import pyplotterlib.standard.plotters as ppl

def parseStdCommandLineArgs():
	""" Used to parse the standard expected command line arguments. Call a relevant script with --help to see their description
	
	"""
	parser = argparse.ArgumentParser(description="Create a specific plot and save a figure")
	parser.add_argument("--expName", default="expected-plotter.json", help="Filename for the expected plot")
	parser.add_argument("--saveExp", default="False", help="Whether to save the expected plotter to file (True means save; False means dont). This essentially recreates the reference point with the current version; thus, it should only be used for a new test or if serialization is changed in a way that purposely breaks backwards compatability")
	outArgs = parser.parse_args()

	def strToBool(inpStr):
		return inpStr.lower() in ["true"]

	outArgs.saveExp = strToBool(outArgs.saveExp)
	return outArgs

def runStandardTest(cmdLineArgs, expPlotter):
	if cmdLineArgs.saveExp:
		ppl.writePlotterToFile(expPlotter, cmdLineArgs.expName)


	ppl.readPlotterFromFile(cmdLineArgs.expName, reInitPlotter=False)
	actPlotter = ppl.readPlotterFromFile(cmdLineArgs.expName, reInitPlotter=True)

	assert expPlotter==actPlotter


