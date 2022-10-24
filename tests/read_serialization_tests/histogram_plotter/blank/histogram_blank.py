
import argparse

import pyplotterlib.standard.plotters as ppl

import pyplotterlib.reg_testing.read_serialization_test.helpers as readSerHelp

def main():
	cmdLineArgs = readSerHelp.parseStdCommandLineArgs()
	expPlotter = ppl.HistogramPlotter()
	readSerHelp.runStandardTest(cmdLineArgs, expPlotter)


if __name__ == '__main__':
	main()






