import collections
import operator

import pandas as pd

from phylodist.constants import *

def computeAll(phylodistDataFrame):
	"""Create a histogram of occurences at taxonomy levels

	Args:
		phylodistData (pandas dataframe):
			tabular data from phylodist

	Returns:
		dictionary of dataframes, one for each taxonomy level
	"""

	taxHistDict = {}
	for i, taxLevel in enumerate(TAXONOMY_HIERARCHY):
		taxHistDict[taxLevel] = pd.DataFrame(
				{ 'count' : phylodistDataFrame.groupby(TAXONOMY_HIERARCHY[0:i+1]).size() }
			).sort('count', ascending=False)

	return(taxHistDict)
