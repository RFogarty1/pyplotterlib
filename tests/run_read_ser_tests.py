
import os

import pyplotterlib.reg_testing.shared as regTestHelp

#Configuration variables. 
START_FOLDER = os.path.join( os.getcwd(), "read_serialization_tests" )


def main():
	testPaths = regTestHelp.findFilesWithExt(START_FOLDER, ".py")
	kwargDict = {}
	for currPath in testPaths:
		currSubPath = os.path.relpath(currPath, start=START_FOLDER)
		print("Running {}".format(currSubPath))
		regTestHelp.runSingleScriptFromPath(currPath, **kwargDict)


if __name__ == '__main__':
	main()

