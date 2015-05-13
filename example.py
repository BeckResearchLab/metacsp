#!/usr/bin/python

import pip

import metadata.io

import phylodist.io
import phylodist.histogram

DATA_ROOT = 'examples/valid'

metadataDF = metadata.io.loadFile(
    DATA_ROOT + '/metadata.tab', 
    indexCols=['origin_O2', 'O2', 'week', 'replicate', 'sample'],
    #indexCols=[2, 3, 4, 5, 0],
    verbose=True
    )

print metadataDF

phylos = phylodist.io.sweepFiles(
    DATA_ROOT
    )

sampleDictTaxHistDict = phylodist.histogram.computeAllForSamples(phylos)
taxonomyDictTaxHist = phylodist.histogram.mergeAcrossSamplesTaxLevels(sampleDictTaxHistDict)

print(sampleDictTaxHistDict['exampleSample']['kingdom'])

phylodist.histogram.plotForSamples(taxonomyDictTaxHist['class'])

with open("requirements.txt", "w") as f:
    for dist in pip.get_installed_distributions():
        req = dist.as_requirement()
        f.write(str(req) + "\n")
