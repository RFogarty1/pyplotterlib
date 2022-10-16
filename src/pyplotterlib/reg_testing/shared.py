
import os
import subprocess

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

