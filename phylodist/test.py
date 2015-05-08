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

if __name__ == '__main__':
	unittest.main()
