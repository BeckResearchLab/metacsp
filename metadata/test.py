import unittest

import io


class test_LoadFile(unittest.TestCase):

    def test_loadFile_filenameType(self):
        with self.assertRaises(TypeError):
            io.loadFile(42, indexCol=0)

    def test_loadFile_indexColType(self):
        with self.assertRaises(TypeError):
            io.loadFile('examples/metadata.tab', indexCol='1')

    def test_loadFile_verboseType(self):
        with self.assertRaises(TypeError):
            io.loadFile('filename', verbose=42)

    def test_loadFile_nonExistentFile(self):
        with self.assertRaises(IOError):
            io.loadFile('file_does_not_exist', indexCol=0)

    def test_loadFile_directoryNotFile(self):
        with self.assertRaises(IOError):
            io.loadFile('examples', indexCol=0)


class test_defaultSampleNameExtractionFunction(unittest.TestCase):

    def test_defaultSampleNameExtractionFunction_value(self):
        self.assertEquals(
            io.defaultSampleNameExtractionFunction(
                'Methane_oxidation_as_a_community_function__' +
                'defining_partnerships_and_strategies_through_' +
                'sequencing_metagenomes_and_metatranscriptomes_of_' +
                'laboratory_manipulated_microcosms__Lake_Washington' +
                '_sediment_Metagenome_7_HOW4_[LakWasMeta7_HOW4]'
            ),
            'mg7H_4'
        )
        self.assertEquals(
            io.defaultSampleNameExtractionFunction(
                'Methane_oxidation_as_a_community_function__' +
                'defining_partnerships_and_strategies_through_' +
                'sequencing_metagenomes_and_metatranscriptomes_of_' +
                'laboratory_manipulated_microcosms__Lake_Washington' +
                '_sediment_Metatranscriptome_7_HOW4_[LakWasMeta7_HOW4]'
            ),
            'mt7H_4'
        )

    def test_defaultSampleNameExtractionFunction_invalid(self):
        with self.assertRaises(ValueError):
            io.defaultSampleNameExtractionFunction('invalid')
