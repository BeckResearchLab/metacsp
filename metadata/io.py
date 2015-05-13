import os
import pandas as pd

from metadata.constants import (
    SAMPLE_TYPE
)


def loadFile(filename, indexCol=None, verbose=False):
    """Load a tab delimited metadata file and return pandas data frame

    Args:
        filename (str): path to a phylodist file
        indexCol (int): column to use as an index
        verbose (bool): if True will display information on the
            number of records found, silent otherwise

    Returns:
        pandas dataframe with metadata records
    """

    # type / value checking
    if not isinstance(filename, str):
        raise TypeError('filename argument must be a str')
    if os.path.isdir(filename):
        raise IOError('filename {0} is a directory'.format(filename))

    if not isinstance(indexCol, int):
        raise TypeError('indexCol must be an integer')

    if not isinstance(verbose, bool):
        raise TypeError('verbose argument must be a boolean')

    # read the tsv
    metadataDataFrame = pd.read_csv(
        filename,
        index_col=indexCol,
        delimiter='\t'
        )
    if verbose:
        print('found {0:d} records in file {1:s}'.format(
            len(metadataDataFrame), filename
            ))

    return metadataDataFrame


def defaultSampleNameExtractionFunction(path):
    """Parse a sample ID to use as a dictionary key in samples
    For a long path, extract out the sample type (metagenome vs.
    metatranscriptome) and the oxygen level (at start of expt.)
    and the week along the time course.

    Args:
        path (str): file path from which to extract the sample key

    Returns
        string containing the parsed sample key
    """

    # find a valid sample type
    sampleType = None
    for key in SAMPLE_TYPE.keys():
        if key in path:
            sampleType = SAMPLE_TYPE[key]
            sampleTypeKey = key
            break
    if sampleType is None:
        raise ValueError('unable to find valid sample type in path')

    # use the location of the sample type to find other pieces
    pathSplit = path.split('_')
    sampleIDIndex = pathSplit.index(sampleTypeKey)
    # sample type is the next field in the path
    sampleID = pathSplit[sampleIDIndex + 1]
    # the oxygen value is next
    sampleO2Tmp = pathSplit[sampleIDIndex + 2]
    sampleO2 = sampleO2Tmp[0]
    # finally, the week is extracted from the oxygen field
    sampleWeek = sampleO2Tmp[3:]

    return '{0}{1}{2}_{3}'.format(
        sampleType, sampleID, sampleO2, sampleWeek
        )
