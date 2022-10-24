
import os
import pathlib

from ..core.serialization import json_io as jsonIO

def writePlotterToFile(inpPlotter, inpPath):
	""" Writes a plotter instance to a file
	
	Args:
		inpPlotter (PlotterInter): Really any instance with a toJSON and fromJSON method should work
		inpPath (str): Path to the output file
			 
	Returns
		 Nothing; but writes data to inpPath
 
	"""
	outJSON = inpPlotter.toJSON()

	#Create directory if needed
	outDir = os.path.split(inpPath)[0]
	pathlib.Path(outDir).mkdir(parents=True, exist_ok=True)
	with open(inpPath,"wt") as f:
		f.write(outJSON)


def readPlotterFromFile(inpPath, reInitPlotter=False):
	""" Reads in a plotter instance from a JSON file
	
	Args:
		inpPath (str): Path to the file. This should have been generated with "writePlotterToFile"
		reInitPlotter (Bool): If True we reinitialize the plotter using its current definition. See notes below for more on the meaning for this. True is likely the most sensible value to use, but False is the default due to backwards-comptability/consistency reasons.

	Notes (reInitPlotter):
		This option exists to give flexibility in dealing with plotters written using previous versions. Setting to True will likely be best usually.
		False: In this case, the read plotter will act as similarly as possible to the one which was written; this includes not having any options which were introduced in subsequent versions.
		True: In this case we use recreate the plotter with the current definition. .createPlot() will still VERY likely act the same between minor versions (its a bug if not), but it will also be possible to set newly introduced options on the output plotter.
			 
	Returns
		outPlotter (PlotterInter): The instance stored in the file. 
 
	"""
	with open(inpPath, "rt") as f:
		inpStr = f.read()

	outPlotter = jsonIO.createInstanceFromJSON(inpStr)

	if reInitPlotter:
		outPlotter = outPlotter.fromPlotter(outPlotter)

	return outPlotter

