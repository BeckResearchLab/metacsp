#!/usr/bin/env python

import pickle
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

import metadata.io

import phylodist.io
import phylodist.histogram

DATA_ROOT = '/dacb/globus'

metadataDF = metadata.io.loadFile(
    DATA_ROOT + '/metadata.tab',
    indexCols=['origin_O2', 'O2', 'week', 'replicate', 'sample', 'date', 'type'],
    verbose=True
    )

taxonomyDictTaxHist = pickle.load(
    open(DATA_ROOT + '/phylodist.pickle', 'rb')
    )

# make a stacked bar as a test
myDF = taxonomyDictTaxHist['family']
pp = PdfPages('output.pdf')
pp.savefig(
    myDF.plot(kind='bar', stacked=True);
    )
pp.close()
