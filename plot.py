#!/usr/bin/env python

import pickle
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd

import metadata.io

import phylodist.io
import phylodist.histogram

DATA_ROOT = '/dacb/globus'

print('loading pickles and other saved data')

"""not necessary as these are bound index levels
metadataDF = metadata.io.loadFile(
    DATA_ROOT + '/metadata.tab',
    indexCols=['origin_O2', 'O2', 'week', 'replicate', 'sample', 'date', 'type'],
    verbose=True
    )
"""

taxonomyDictTaxHist = pickle.load(
    open(DATA_ROOT + '/phylodist.pickle', 'rb')
    )

print('done')

sns.set(font="monospace")

# make a stacked bar as a test
df = taxonomyDictTaxHist['class']
with PdfPages('output.pdf') as pdf:
    fig = plt.figure()
    """super ugly
    df.transpose().plot(kind='bar', stacked=True)
    plt.xlabel('Samples')
    plt.ylabel('% of population')
    """
    # color palette for cells
    cmap = sns.color_palette('YlGnBu', 10)
    # column color palette for time
    weekPalette = sns.color_palette('Greens', n_colors=len(df.columns.get_level_values('week').unique()))
    weekLut = dict(zip(map(str, df.columns.get_level_values('week').unique()), weekPalette))
    colColors = pd.Series(df.columns.get_level_values('week')).map(weekLut)
    # fillna is required or sns.clustermap seg faults
    df.fillna(0, inplace=True)
    sns.clustermap(df, method="average", figsize=(13, 13), col_colors=colColors, cmap=cmap)
    pdf.savefig()
    plt.close()
