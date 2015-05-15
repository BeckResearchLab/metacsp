import os
import csv
import string

import pandas as pd

from phylodist.constants import (
    EXPECTED_RECORD_LENGTH, TAXONOMY_FIELD, EXPECTED_TAXONOMY_LENGTH,
    PHYLODIST_HEADER, PHYLODIST_FILE_SUFFIX, IMG_DATA_DIRECTORY_NAME,
    TAXONOMY_HIERARCHY
)


def loadFile(filename, verbose=False):
    """Load a phylodist file and return a pandas dataframe

    Args:
        filename (str): path to a phylodist file
        verbose (bool): if True will display information on the
            number of records found, silent otherwise

    Returns:
        pandas dataframe with records
    """

    # type checking
    if not isinstance(verbose, bool):
        raise TypeError('verbose argument must be a boolean')

    # read the tab delimited file in
    data = list(csv.reader(open(filename, 'rb'), delimiter='\t'))
    if verbose:
        print('found {0:d} records in file {1}'.format(
            len(data),
            filename
            ))

    # process records for sanity checking number of records
    #  and parse out the taxonomy string
    row = 0
    for record in data:
        row = row + 1
        # check the record length against the expected value
        thisRecLen = len(record)
        if thisRecLen != EXPECTED_RECORD_LENGTH:
            raise ValueError(
                'unexpected record length on row {0:d}' +
                ' found {1:d} and expected {2:d}'.format(
                    row, thisRecLen, EXPECTED_RECORD_LENGTH
                    )
                )
        # parse the taxonomy string
        taxString = record[TAXONOMY_FIELD]
        taxList = string.split(taxString, ";")
        taxListLen = len(taxList)
        if taxListLen != EXPECTED_TAXONOMY_LENGTH:
            raise ValueError(
                'unexpected taxonomy length found on row {0:d}' +
                ' found {1} and expected {2}'.format(
                    row, taxListLen, EXPECTED_TAXONOMY_LENGTH
                    )
                )
        # replace the taxonomy string with the list in our record
        record.pop(TAXONOMY_FIELD)
        record.extend(taxList)

    phylodistDataFrame = pd.DataFrame(
        data, columns=PHYLODIST_HEADER + TAXONOMY_HIERARCHY
    )

    return phylodistDataFrame


def sweepFiles(rootDir, sampleNameExtractionFunction=None):
    """Walk a directory looking for phylodist files and load them

    Args:
        rootDir (str): the base directory from which to begin a walk
        sampleNameExtractionFunction (function): a function to use on
            the directory path to extract a key to use in the dictionary

    Returns:
        dictionary of pandas data frames with key of directory name
            containing the IMG data directory and value of phylodistDataFrames
    """
    if sampleNameExtractionFunction is None:
        sampleNameExtractionFunction = defaultSampleNameExtractionFunction

    if not os.path.isdir(rootDir):
        raise IOError('{0} is not a directory'.format(rootDir))

    print(
        'scanning {0} for files ending with {1}'.format(
            rootDir,
            PHYLODIST_FILE_SUFFIX
            )
        )

    phylodistSweepDict = {}
    for dirName, subdirList, fileList in os.walk(rootDir):
        baseDir = string.split(dirName, '/')[-1]
        if baseDir != IMG_DATA_DIRECTORY_NAME:
            continue
        # this is a directory that contains the IMG data directory
        # look for a file ending in the phylodist suffix
        for filename in fileList:
            suffix = string.split(filename, ".")[-1]
            if suffix != PHYLODIST_FILE_SUFFIX:
                continue
            # valid phylodist file, let's load it!
            phylodistDataFrame = loadFile(dirName + "/" + filename)
            # parse the key using the user supplied function
            sampleKey = sampleNameExtractionFunction(dirName + "/" + filename)
            # add the key to the dictionary with the data frame
            phylodistSweepDict[sampleKey] = phylodistDataFrame
            print(
                'found {0:d} rows for sample {1}'.format(
                    len(phylodistDataFrame.index), sampleKey
                    )
                )

    print('found {0:d} files'.format(len(phylodistSweepDict)))

    return phylodistSweepDict


def defaultSampleNameExtractionFunction(path):
    """Parse a sample ID to use as a dictionary key in samples
        Uses text in the first [] block it finds.  E.g.
        directory_path_with[aSampleKey]in_it/some_subdir/file
        would return aSampleKey

    Args:
        path (str): file path from which to extract the sample key

    Returns
        string containing the parsed sample key
    """
    return string.split(string.split(path, '[')[1], ']')[0]


def writeExcelTaxonomyDictTaxHist(filename, taxonomyDictTaxHist):
    """Save a dictionary of taxonomy histograms that has
        been merged across samples into an Excel workbook using
        one sheet per taxonomy level

    Args:
        filename (str): the output filename, should end in .xlsx
        taxonomyDictTaxHist (dict): a dictionary of taxonomy levels
            where each entry is a pandas DataFrame with the merged
            sample data.  This is generated from
            phylodist.histogram.mergeAcrossSamplesTaxLevels

    Returns:
        True
    """

    writer = pd.ExcelWriter(filename)
    for taxonomyLevel in taxonomyDictTaxHist.keys():
        taxonomyDictTaxHist[taxonomyLevel].to_excel(
            writer,
            sheet_name=taxonomyLevel,
            float_format='%.2f',
            header=True,
            index=True,
            merge_cells=True
            )
    writer.save()

    return True
