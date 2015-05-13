import unittest

import io


class test_LoadFile(unittest.TestCase):

    def test_loadFile_filenameType(self):
        with self.assertRaises(TypeError):
            io.loadFile(42)

    def test_loadFile_verboseType(self):
        with self.assertRaises(TypeError):
            io.loadFile("filename", 42)

    def test_loadFile_nonExistentFile(self):
        with self.assertRaises(IOError):
            io.loadFile("file_does_not_exist")

    def test_loadFile_directoryNotFile(self):
        with self.assertRaises(IOError):
            io.loadFile("examples")

    def test_loadFile_incorrectFieldCount(self):
        with self.assertRaises(ValueError):
            io.loadFile("examples/invalid/badRecordLength.phylodist")

    def test_loadFile_incorrectTaxFieldCount(self):
        with self.assertRaises(ValueError):
            io.loadFile("examples/invalid/badTaxRecordLength.phylodist")

    def test_loadFile_exampleValues(self):
        # check the length
        pdDF = io.loadFile(
            "examples/valid/example[exampleSample]/IMG_Data/example.phylodist",
            verbose=True
        )
        self.assertEquals(len(pdDF.index), 59476)
        # spot check row 98's locus_tag
        self.assertEquals(pdDF.at[97, 'locus_tag'], "Ga0066528_1383641")


class test_defaultSampleNameExtractionFunction(unittest.TestCase):

    def test_defaultSampleNameExtractionFunction_value(self):
        self.assertEquals(
            io.defaultSampleNameExtractionFunction(
                "examples/valid/example[exampleSample]/" +
                "IMG_Data/example.phylodist"
            ),
            "exampleSample"
        )


class test_sweepFiles(unittest.TestCase):

    def test_sweepFiles_fileNotDirectory(self):
        with self.assertRaises(IOError):
            io.sweepFiles("phylodist/test.py")

    def test_sweepFiles_nonExistentDir(self):
        with self.assertRaises(IOError):
            io.sweepFiles("directory_does_not_exist")

    def test_sweepFiles_directoryType(self):
        with self.assertRaises(TypeError):
            io.sweepFiles(42)

    def test_sweepFiles_values(self):
        pdSD = io.sweepFiles("examples")
        # check the length of the dictionary
        self.assertEquals(len(pdSD), 2)
        # verify the sample key names are correct
        for key in pdSD.keys():
            self.assertIn(key, ["exampleSample", "anotherExampleSample"])
        # spot check specific values in the dictionary's data frame
        self.assertEquals(
            pdSD['exampleSample'].at[97, 'locus_tag'], "Ga0066528_1383641"
        )
        self.assertEquals(
            pdSD['anotherExampleSample'].at[1013, 'locus_tag'],
            "Ga0066521_1490921"
        )

if __name__ == '__main__':
    unittest.main()
