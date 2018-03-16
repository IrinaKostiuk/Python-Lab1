from xml.dom.minidom import parse
import unittest
import sys
import os


class LabTest(unittest.TestCase):

    def testParseXml(self):
        # initialize
        xml = '''
            <root>
                <files>
                    <file>file1.html</file>
                    <file>file2.html</file>
                    <file>test file.htm</file>
                </files>
            </root>
            '''
        expected = ['file1.html', 'file2.html', 'test file.htm']
        file = '__tmp__'
        with open(file, 'w') as f:
            f.write(xml)
        parser = LabImpl(file)
        # work
        files = parser.getFiles()
        # test
        self.assertEqual(files, expected)
        # cleanup
        os.remove(file)


class LabImpl:

    def __init__(self, file):
        self.file = file

    def getFiles(self):
        xml = parse(self.file)
        nodes = xml.getElementsByTagName('file')
        files = [node.childNodes[0].data for node in nodes]
        return files


if __name__ == '__main__':
    unittest.main()
