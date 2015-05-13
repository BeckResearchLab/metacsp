#!/usr/bin/python

import metadata.io

import phylodist.io
import phylodist.histogram

DATA_ROOT = '/dacb/globus'

metadataDF = metadata.io.loadFile(
    DATA_ROOT + '/metadata.tab', indexCol=0, verbose=True
    )

phylodistSampleDict = phylodist.io.sweepFiles(
    DATA_ROOT,
    sampleNameExtractionFunction=metadata.io.defaultSampleNameExtractionFunction
    )

sampleDictTaxHistDict = phylodist.histogram.computeAllForSamples(
    phylodistSampleDict
    )

taxonomyDictTaxHist = phylodist.histogram.mergeAcrossSamplesTaxLevels(
    sampleDictTaxHistDict
)

writer = pd.ExcelWriter('output.xlsx')
for taxonomyLevel in taxonomyDictTaxHist.keys():
    taxonomyDictTaxHist[taxonomyLevel].to_excel(writer, taxonomyLevel)
writer.save()
