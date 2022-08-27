
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


def readPlotterFromFile(inpPath):
	""" Reads in a plotter instance from a JSON file
	
	Args:
		inpPath (str): Path to the file. This should have been generated with "writePlotterToFile"
			 
	Returns
		outPlotter (PlotterInter): The instance stored in the file. 
 
	"""
	with open(inpPath, "rt") as f:
		inpStr = f.read()
	return jsonIO.createInstanceFromJSON(inpStr)

