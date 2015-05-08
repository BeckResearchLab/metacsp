import unittest

import io

class TestIO(unittest.TestCase):
	
	def test_loadFile_filenameType(self):
		# test non-string filename raises an error
		with self.assertRaises(TypeError):
			io.loadFile(42)

	def test_loadFile_verboseType(self):
		# test non-bool verbose raises an error
		with self.assertRaises(TypeError):
			io.loadFile("filename", 42)

	def test_loadFile_nonExistentFile(self):
		# test a non-existent file raises an error
		with self.assertRaises(IOError):
			io.loadFile("file_does_not_exist")

	def test_loadFile_directoryNotFile(self):
		# test a directory instead of file raises an error
		with self.assertRaises(IOError):
			io.loadFile("examples")

if __name__ == '__main__':
	unittest.main()
