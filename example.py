#!/usr/bin/python

import pandas as pd

import phylodist.io
import phylodist.histogram

import metadata.io

mdDF = metadata.io.loadFile('examples/metadata.tab', indexCol=0, verbose=True)

phylos = phylodist.io.sweepFiles(
    "/dacb/globus",
    sampleNameExtractionFunction=metadata.io.defaultSampleNameExtractionFunction
    )
#phylos = phylodist.io.sweepFiles("examples/valid")
sampleDictTaxHistDict = phylodist.histogram.computeAllForSamples(phylos)
taxonomyDictTaxHist = phylodist.histogram.mergeAcrossSamplesTaxLevels(sampleDictTaxHistDict)

#phylodist.histogram.plotForSamples(taxonomyDictTaxHist['class'])

writer = pd.ExcelWriter('output.xlsx')
for taxonomyLevel in taxonomyDictTaxHist.keys():
    taxonomyDictTaxHist[taxonomyLevel].to_excel(writer, taxonomyLevel)
writer.save()

#print(sampleDictTaxHistDict['exampleSample']['kingdom'])
#print(sampleDictTaxHistDict['exampleSample']['phylum'])

#print(taxHistograms['kingdom'])
#print(taxHistograms['phylum'])
#print(taxHistograms['class'])
#print(taxHistograms['order'])
#print(taxHistograms['family'])

#import pip
#with open("requirements.txt", "w") as f:
#    for dist in pip.get_installed_distributions():
#        req = dist.as_requirement()
#        f.write(str(req) + "\n")
