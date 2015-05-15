#!/bin/env python

import metadata.io

import phylodist.io
import phylodist.histogram

DATA_ROOT = '/dacb/globus'

metadataDF = metadata.io.loadFile(
    DATA_ROOT + '/metadata.tab',
    indexCols=['origin_O2', 'O2', 'week', 'replicate', 'sample', 'date', 'type'],
    verbose=True
    )

phylodistSampleDict = phylodist.io.sweepFiles(
    DATA_ROOT,
    sampleNameExtractionFunction=metadata.io.defaultSampleNameExtractionFunction
    )

sampleDictTaxHistDict = phylodist.histogram.computeAllForSamples(
    phylodistSampleDict
    )

taxonomyDictTaxHist = phylodist.histogram.mergeAcrossSamplesTaxLevels(
    sampleDictTaxHistDict,
    metadata=metadataDF
)

# filter at 2.5% abundance
for taxonomyLevel in TAXONOMY_HIERARCHY:
    dF = taxonomyDictTaxHist[taxonomyLevel]
    taxonomyDictTaxHist[taxonomyLevel] = dF.where(dF >= 2.5)
    taxonomyDictTaxHist[taxonomyLevel].dropna(how='all', inplace=True)


phylodist.io.writeExcelTaxonomyDictTaxHist(
    DATA_ROOT + '/phylodist.xlsx',
    taxonomyDictTaxHist
    )
