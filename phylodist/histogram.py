import sys

import pandas as pd

from phylodist.constants import (
	TAXONOMY_HIERARCHY
)


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
				'count': phylodistDataFrame.groupby(TAXONOMY_HIERARCHY[0:i + 1]).size()
			}
		).sort('count', ascending=False)
		# next, append the percent column
		taxHistDict[taxLevel]['percent'] = taxHistDict[taxLevel].apply(
			lambda x: 100 * x / float(x.sum())
		)

	return taxHistDict


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

	return sampleDictTaxHistDict


def validateSampleDictTaxHistDict(sampleDictTaxHistDict):
	"""Sanity check a sampleDictTaxHistDict
		Primarily used by merge functions

	Args:
		sampleDictTaxHistDict (dict): dictionary of phylodistDataFrames for
			all samples

	Returns:
		nothing, raises errors on sanity failures
	"""
	if not isinstance(sampleDictTaxHistDict, dict):
		raise TypeError("argument sampleDictTaxHistDict should be a dict")
	samples = len(sampleDictTaxHistDict)
	if samples < 1:
		raise ValueError(
			"argument sampleDictTaxHistDict must have at least one entry"
		)


def mergeAcrossSamplesTaxLevels(sampleDictTaxHistDict):
	"""Create a dictionary of data frames that are merged at taxonomy
		levels.  The key into this dictionary is the taxonomy level.

	Args:
		sampleDictTaxHistDict (dict): dictionary of phylodistDataFrames for
			all samples

	Returns:
		a new dictionary with keys for eah taxonomy level containing
			a merged ataframe with histograms from all samples
	"""
	validateSampleDictTaxHistDict(sampleDictTaxHistDict)

	taxonomyDictTaxHist = {}
	for taxonomyLevel in TAXONOMY_HIERARCHY:
		taxonomyDictTaxHist[taxonomyLevel] = mergeAcrossSamples(
			sampleDictTaxHistDict, taxonomyLevel
		)

	return taxonomyDictTaxHist


def mergeAcrossSamples(sampleDictTaxHistDict, taxonomyLevel):
	"""Create a single data frame by merging all samples for a given
		taxonomy level

	Args:
		sampleDictTaxHistDict (dict): dictionary of phylodistDataFrames for
			all samples
		taxonomyLevel (str): taxonomy level to use in chart

	Returns:
		a single merged data frame with all of the samples' data
	"""
	if taxonomyLevel not in TAXONOMY_HIERARCHY:
		raise ValueError("taxonomy level ' + taxonomyLevel + ' is not recognized")

	validateSampleDictTaxHistDict(sampleDictTaxHistDict)

	first = True
	for sample in sampleDictTaxHistDict.keys():
		if first:
			tmpDF = sampleDictTaxHistDict[sample][taxonomyLevel].drop('count', 1)
			mergedPhylodistHist = tmpDF.rename(
				columns={'percent': sample}
			)
		else:
			tmpDF = sampleDictTaxHistDict[sample][taxonomyLevel].drop('count', 1)
			tmpDF.rename(
				columns={'percent': sample},
				inplace=True
			)
			mergedPhylodistHist = pd.merge(
				mergedPhylodistHist, tmpDF,
				how="outer", left_index=True, right_index=True
			)
		first = False

	return mergedPhylodistHist


def plotForSamples(mergedPhylodistHist):
	"""Create a stacked bar chart for the taxonomy abundance percentages
		from a merged phylodist histogram

	Args:
		mergedPhylodistHist (data frame): single table with taxonomy as levels
			and samples as columns
			all samples
		taxonomyLevel (str): taxonomy level to use in chart

	Returns:
		? figure or nothing ? undecided
	"""
	plot = mergedPhylodistHist.T.plot(kind='bar', stacked=True, legend=False)
	fig = plot.get_figure()
	fig.savefig("output.png")
