import os
import sys
import csv
import string

import pandas as pd

from phylodist.constants import *

def loadFile(filename, verbose=False):
	"""Load a phylodist file and return a pandas dataframe

	Args:
		filename (str): path to a phylodist file
		verbose (bool): if True will display information on the
			number of records found, silent otherwise

	Returns:
		pandas dataframe with records
	"""

	# type checking
	if (not isinstance(verbose, bool)):
		raise(TypeError)

	# read the tab delimited file in
	data = list(csv.reader(open(filename, 'rb'), delimiter='\t'))
	if (verbose):
		print("found " + str(len(data)) + " records in file " + filename)

	# process records for sanity checking number of records
	#  and parse out the taxonomy string
	row = 0
	for record in data:
		row = row + 1
		# check the record length against the expected value
		thisRecLen = len(record)
		if (thisRecLen != EXPECTED_RECORD_LENGTH):
			print("unexpected record length found on row " + str(row) + 
				" found " + str(thisRecLen) + " and expected " + 
				str(EXPECTED_RECORD_LENGTH))
			sys.exit(1)
		# parse the taxonomy string
		taxString = record[TAXONOMY_FIELD]
		taxList = string.split(taxString, ";")
		taxListLen = len(taxList)
		if (taxListLen != EXPECTED_TAXONOMY_LENGTH):
			print("unexpected taxonomy length found on row " + str(row) + 
				" found " + str(taxListLen) + " and expected " + 
				str(EXPECTED_TAXONOMY_LENGTH))
			sys.exit(1)
		# replace the taxonomy string with the list in our record
		record.pop(TAXONOMY_FIELD)
		record.extend(taxList)

	phylodistDataFrame = pd.DataFrame(data, columns=PHYLODIST_HEADER + TAXONOMY_HIERARCHY)

	return(phylodistDataFrame)

def sweepFiles(rootDir, keyExtractionFunction = None):
	"""Walk a directory looking for phylodist files and load them

	Args:
		rootDir (str): the base directory from which to begin a walk
		keyExtractionFunction (function): a function to use on the directory
			path to extract a key to use in the dictionary

	Returns:
		dictionary of pandas data frames with key of directory name
			containing the IMG data directory and value of phylodistDataFrames
	"""
	if (keyExtractionFunction is None):
		keyExtractionFunction = defaultKeyExtractionFunction

	if (not os.path.isdir(rootDir)):
		raise(IOError)

	print("scanning " + rootDir + " for files ending with ." + PHYLODIST_FILE_SUFFIX)

	phylodistSweepDict = {}
	for dirName, subdirList, fileList in os.walk(rootDir):
		baseDir = string.split(dirName, "/")[-1]
		if (baseDir != IMG_DATA_DIRECTORY_NAME):
			continue
		# this is a directory that contains the IMG data directory
		# look for a file ending in the phylodist suffix
		for filename in fileList:
			suffix = string.split(filename, ".")[-1]
			if (suffix != PHYLODIST_FILE_SUFFIX):
				continue
			# valid phylodist file, let's load it!
			phylodistDataFrame = loadFile(dirName + "/" + filename)
			# parse the key using the user supplied function
			sampleKey = keyExtractionFunction(dirName + "/" + filename)
			# add the key to the dictionary with the data frame
			phylodistSweepDict[sampleKey] = phylodistDataFrame
			print("found " + str(len(phylodistDataFrame.index)) + " rows for sample " + sampleKey)

	return(phylodistSweepDict)

def defaultKeyExtractionFunction(path):
	"""Parse a sample ID to use as a dictionary key in samples
		Uses text in the first [] block it finds.  E.g.
		directory_path_with[aSampleKey]in_it/some_subdir/file
		would return aSampleKey

	Args:
		path (str): file path from which to extract the sample key

	Returns
		string containing the parsed sample key
	"""
	return string.split(string.split(path, "[")[1], "]")[0]
