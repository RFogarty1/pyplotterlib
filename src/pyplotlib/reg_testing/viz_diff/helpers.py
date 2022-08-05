
import argparse
import os
import subprocess

import matplotlib.pyplot as plt

def parseStdCommandLineArgs():
	""" Used to parse the standard expected command line arguments. Call a relevant script with --help to see their description
	
	"""
	parser = argparse.ArgumentParser(description="Create a specific plot and save a figure")
	parser.add_argument("--expName", default="expected-plot-vizdiff", help="Filename for the expected plot")
	parser.add_argument("--actName", default="actual-plot-vizdiff", help="Filename for the actual plot")
	parser.add_argument("--saveExp", default="False", help="Whether to save the plot as the expected answer as well as the actual answer (pass True to save it, anything else to not save it)")
	parser.add_argument("--saveAct", default="True", help="Save the plot as the actual answer; default is True, but can pass \"false or any other string to negate it")
	outArgs = parser.parse_args()

	def strToBool(inpStr):
		return inpStr.lower() in ["true"]

	outArgs.saveExp = strToBool(outArgs.saveExp)
	outArgs.saveAct = strToBool(outArgs.saveAct)
	return outArgs

def createAndSavePlotForPlotter(inpPlotter, kwargDict=None, saveExp=False, saveAct=True, expName="expected-plot-vizdiff", actName="actual-plot-vizdiff"):
	kwargDict = {} if kwargDict is None else kwargDict
	inpPlotter.createPlot(**kwargDict)
	outFigure = plt.gcf()
	if saveExp:
		outFigure.savefig(expName + ".png", format="png")
	if saveAct:
		outFigure.savefig(actName + ".png", format="png")


def runSingleScriptFromPath(inpPath, **kwargs):
	os.chdir(os.path.split(inpPath)[0])
	kwargStr = " ".join(["--{} {}".format(key,val) for key,val in kwargs.items()])
	subprocess.check_call(["python3 {} {}".format(inpPath,kwargStr)], shell=True)


def findFilesWithExt(startPath, ext):
	outPaths = list()
	for relPath, dirs, files in os.walk(startPath):
		for file in files:
			if file.endswith(ext):
				currPath = os.path.abspath( os.path.join(startPath, relPath, file) )
				outPaths.append( os.path.normpath(currPath) )
	return outPaths


