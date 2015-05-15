#!/bin/env python

import pickle
import matplotlib as plt

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


