import sys
import collections
import operator

import numpy as np
import matplotlib.pyplot as plt
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
		# first, let's compute a count column using the size aggregate of a groupby
		taxHistDict[taxLevel] = pd.DataFrame(
				{
					'count'    : phylodistDataFrame.groupby(TAXONOMY_HIERARCHY[0:i+1]).size()
				}
			).sort('count', ascending=False)
		# next, append the percent column
		taxHistDict[taxLevel]['percent'] = taxHistDict[taxLevel].apply(lambda x: 100*x/float(x.sum()))

	return(taxHistDict)

def computeAllForSamples(phylodistSweepDict):
	"""Create histograms of occurences at taxonomy levels for
		all entries in a sample sweep dictionary

	Args:
		phylodistSweepDict (dict): dictionary of phylodistDataFrames for
			all samples

	Returns:
		dictionary of dictionary of dataframes, one for each taxonomy level
			per sample
	"""

	sys.stdout.write("computing histograms across taxonomy hierarchy for samples")
	sampleDictTaxHistDict = {}
	for key in phylodistSweepDict.keys():
		sys.stdout.write(".")
		sys.stdout.flush()
		sampleDictTaxHistDict[key] = computeAll(phylodistSweepDict[key])
	print("done")

	return(sampleDictTaxHistDict)

def plotForSamples(sampleDictTaxHistDict, taxonomyLevel):
	"""Create a stacked bar chart for the taxonomy abundance percentages
		for a specific taxonomic level

	Args:
		sampleDictTaxHistDict (dict): dictionary of phylodistDataFrames for
			all samples
		taxonomyLevel (str): taxonomy level to use in chart

	Returns:
		? figure or nothing ? undecided
	"""
	
	if (not taxonomyLevel in TAXONOMY_HIERARCHY):
		raise ValueError

	samples = len(sampleDictTaxHistDict)
	if (samples < 1):
		raise ValueError

	first = True
	for sample in sampleDictTaxHistDict.keys():
		if (first):
			tmpDF = sampleDictTaxHistDict[sample][taxonomyLevel].drop('count', 1)
			mergedPhylodistHist = tmpDF.rename(
					columns = { 'percent' : sample }
				)
		else:
			tmpDF = sampleDictTaxHistDict[sample][taxonomyLevel].drop('count', 1)
			tmpDF.rename(
					columns = { 'percent' : sample },
					inplace = True
				)
			mergedPhylodistHist = pd.merge(mergedPhylodistHist, tmpDF,
					how="outer", left_index=True, right_index=True
				)
		first = False

	plot = mergedPhylodistHist.T.plot(kind='bar', stacked=True, legend=False)
	fig = plot.get_figure()
	fig.savefig("output.png")
