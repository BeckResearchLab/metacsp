#!/usr/bin/python

import pip

import metadata.io

import phylodist.io
import phylodist.histogram

DATA_ROOT = 'examples/valid'

metadataDF = metadata.io.loadFile(
    DATA_ROOT + '/metadata.tab', indexCol=0, verbose=True
    )

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
