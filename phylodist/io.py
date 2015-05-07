import sys
import csv
import string

from phylodist.constants import *

def loadFile(filename):
	"""Load a phylodist file and return a pandas dataframe

	Args:
		filename (str): path to a phylodist file

	Returns:
		pandas dataframe with records
	"""

	# read the tab delimited file in
	data = list(csv.reader(open(filename, 'rb'), delimiter='\t'));
	print("found " + str(len(data)) + " records in file " + filename);

	# process records for sanity checking number of records
	#  and parse out the taxonomy string
	row = 0
	for record in data:
		row = row + 1;
		# check the record length against the expected value
		thisRecLen = len(record);
		if (thisRecLen != EXPECTED_RECORD_LENGTH):
			print("unexpected record length found on row " + str(row) + 
				"; found " + str(thisRecLen) + " and expected " + 
				str(EXPECTED_RECORD_LENGTH));
			sys.exit(1);
		# parse the taxonomy string
		taxString = record[TAXONOMY_FIELD];
		taxList = string.split(taxString, ";");
		taxListLen = len(taxList)
		if (taxListLen != EXPECTED_TAXONOMY_LENGTH):
			print("unexpected taxonomy length found on row " + str(row) + 
				"; found " + str(taxListLen) + " and expected " + 
				str(EXPECTED_TAXONOMY_LENGTH));
			sys.exit(1);
		# replace the taxonomy string with the list in our record
		record.pop(TAXONOMY_FIELD);
		record.extend(taxList);

	return(data)
