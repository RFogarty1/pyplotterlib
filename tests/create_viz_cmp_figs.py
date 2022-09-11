
import os
import pyplotterlib.reg_testing.viz_diff.helpers as helpers

#Configuration variables. 
START_FOLDER = os.path.join( os.getcwd(), "viz_cmp_tests" )
CREATE_ACTUAL = True #Whether to save the actual plot (what the plot looks like with current code); Should almost always be True
CREATE_EXPECTED = False #Whether to resave the reference plot (what it SHOULD look like); Should almost always be False (mainly used when adding/modifying tests)

def main():
	testPaths = helpers.findFilesWithExt(START_FOLDER, ".py")
	kwargDict = {"saveExp":CREATE_EXPECTED, "saveAct":CREATE_ACTUAL}
	for currPath in testPaths:
		helpers.runSingleScriptFromPath(currPath, **kwargDict)


if __name__ == '__main__':
	main()

