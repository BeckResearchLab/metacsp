#!/usr/bin/python

# this might be converted to tests one day

import phylodist.io
import phylodist.histogram

phylodistDataFrame = phylodist.io.loadFile("examples/example.phylodist");
taxHistograms = phylodist.histogram.computeAll(phylodistDataFrame);

#print(taxHistograms['kingdom']);
#print(taxHistograms['phylum'])
#print(taxHistograms['class'])
print(taxHistograms['order'])
#print(taxHistograms['family'])
