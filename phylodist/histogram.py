import collections
import operator

from phylodist.constants import *

def histogram(phylodistData):
	"""Create a histogram of occurences at taxonomy levels

	Args:
		phylodistData (pandas dataframe):
			tabular data from phylodist

	Returns:
		pandas dataframe with histogram at each taxonomy level
	"""

	taxHistDict = {}
	for i, taxLevel in enumerate(TAXONOMY_HIERARCHY):
		taxHistDict[taxLevel] = collections.defaultdict(int)

	# iterate over records again and create histogram
	for record in phylodistData:
		for i, taxLevel in enumerate(TAXONOMY_HIERARCHY):
			taxList = record[TAXONOMY_FIELD:];
			taxHistDict[taxLevel][taxList[i]] += 1
