#!/usr/bin/env python

import pip

import metadata.io

import phylodist.io
import phylodist.histogram
from phylodist.constants import TAXONOMY_HIERARCHY

DATA_ROOT = 'examples/valid'

metadataDF = metadata.io.loadFile(
    DATA_ROOT + '/metadata.tab', 
    indexCols=['origin_O2', 'O2', 'week', 'replicate', 'sample', 'date'],
    verbose=True
    )

phylos = phylodist.io.sweepFiles(
    DATA_ROOT,
    sampleNameExtractionFunction=metadata.io.defaultSampleNameExtractionFunction,
    )

sampleDictTaxHistDict = phylodist.histogram.computeAllForSamples(phylos)
taxonomyDictTaxHist = phylodist.histogram.mergeAcrossSamplesTaxLevels(
    sampleDictTaxHistDict,
    metadata=metadataDF
    )

# filter at 2.5% abundance
for taxonomyLevel in TAXONOMY_HIERARCHY:
    dF = taxonomyDictTaxHist[taxonomyLevel]
    taxonomyDictTaxHist[taxonomyLevel] = dF.where(dF >= 2.5)
    taxonomyDictTaxHist[taxonomyLevel].dropna(how='all', inplace=True)

phylodist.io.writeExcelTaxonomyDictTaxHist('output.xlsx', taxonomyDictTaxHist)

with open("requirements.txt", "w") as f:
    for dist in pip.get_installed_distributions():
        req = dist.as_requirement()
        f.write(str(req) + "\n")
