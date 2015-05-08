#!/usr/bin/python

import phylodist.io
import phylodist.histogram

#phylos = phylodist.io.sweepFiles("/dacb/globus")
phylos = phylodist.io.sweepFiles("examples/valid")
sampleDictTaxHistDict = phylodist.histogram.computeAllForSamples(phylos)
taxonomyDictTaxHist = phylodist.histogram.mergeAcrossSamplesTaxLevels(sampleDictTaxHistDict)

phylodist.histogram.plotForSamples(taxonomyDictTaxHist['class'])

#print(sampleDictTaxHistDict['exampleSample']['kingdom'])
#print(sampleDictTaxHistDict['exampleSample']['phylum'])

#print(taxHistograms['kingdom'])
#print(taxHistograms['phylum'])
#print(taxHistograms['class'])
#print(taxHistograms['order'])
#print(taxHistograms['family'])
