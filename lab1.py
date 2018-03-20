# -*- coding: utf-8 -*-
from xml.dom.minidom import parse
import unittest
import sys
import os
from mutagen.id3 import ID3


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
        parser = LabImpl()
        # work
        files = parser.getFiles(file)
        # test
        self.assertEqual(files, expected)
        # cleanup
        os.remove(file)

    def testFilterM3(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))

        files = [
            'file://%s/music/Eminem–LoseYourself.mp3' % current_dir,
            'file://%s/music/Muse–Psycho.mp3' % current_dir,
            'file://%s/music/Imagine_Dragon–Demons.mp3' % current_dir,
            'file://%s/music/Red_Hot_Chili_Peppers_-_Snow.mp3' % current_dir,
            ]

        expected = [
            'file://%s/music/Muse–Psycho.mp3' % current_dir,
            'file://%s/music/Imagine_Dragon–Demons.mp3' % current_dir,
            'file://%s/music/Red_Hot_Chili_Peppers_-_Snow.mp3' % current_dir,
            ].sort()
        
        parser = LabImpl()

        result = parser.filterMP3(files, 'Rock').sort()
        self.assertEqual(result, expected)

        


class LabImpl:

    def getFiles(self, file):
        xml = parse(file)
        nodes = xml.getElementsByTagName('file')
        files = [node.childNodes[0].data for node in nodes]
        return files

    def filterMP3(self,listMP3,genre):
        result = []
        for nameMP3 in listMP3:
            if (nameMP3[:4]!="file"):
                mp3 = urllib2.urlopen(nameMP3)
                mp3_content = mp3.read()
                output = open('__tmp__','w')
                output.write(mp3_content)
                output.close()
                
                # filter genre
                if (ID3('__tmp__')['TCON'].text[0].encode('utf-8') == genre):
                    result.append(genre)  
            else:
                if (ID3(nameMP3[7:])['TCON'].text[0].encode('utf-8') == genre):
                    result.append(genre)
        return result

if __name__ == '__main__':
    unittest.main()
