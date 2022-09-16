
import os
import subprocess
import pyplotterlib.reg_testing.viz_diff.helpers as helpers

START_FOLDER = os.path.join( os.getcwd(), "..", "Examples", "for_doc_pages")


def main():
	testPaths = helpers.findFilesWithExt(START_FOLDER, ".ipynb")
	convertNotebooks(testPaths)
	pyPaths = helpers.findFilesWithExt(START_FOLDER, ".py")
	removeCommentLinesFromConvertedNotebooks(pyPaths)

	for currPath in pyPaths:
		helpers.runSingleScriptFromPath(currPath)


def convertNotebooks(inpPaths):
	for currPath in inpPaths:
		currComm = "jupyter nbconvert --to script {}".format(currPath)
		subprocess.check_call(currComm, shell=True)


def removeCommentLinesFromConvertedNotebooks(inpPaths):
	for currPath in inpPaths:
		_reWriteWithCommentsRemoved(currPath)

def _reWriteWithCommentsRemoved(inpPath):
	with open(inpPath,"rt") as f:
		inpText = f.readlines()

	outText = [x for x in inpText if not x.startswith('#')]

	with open(inpPath,"wt") as f:
		f.writelines(outText)

#jupyter nbconvert --to script [YOUR_NOTEBOOK].ipynb
#

if __name__ == '__main__':
	main()

