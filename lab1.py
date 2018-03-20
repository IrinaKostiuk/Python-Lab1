# -*- coding: utf-8 -*-
from xml.dom.minidom import parse
import unittest
import sys
import os
from mutagen.id3 import ID3
import re
import urllib2


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
        expected = [
            'file1.html',
            'file2.html',
            'test file.htm',
            ]
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
            'https://www.mfiles.co.uk/mp3-downloads/moonlight-movement1.mp3',
            ]

        expected = [
            'file://%s/music/Muse–Psycho.mp3' % current_dir,
            'file://%s/music/Imagine_Dragon–Demons.mp3' % current_dir,
            'file://%s/music/Red_Hot_Chili_Peppers_-_Snow.mp3' % current_dir,
            ].sort()

        parser = LabImpl()

        result = parser.filterMP3(files, 'Rock').sort()
        self.assertEqual(result, expected)

    def testGetMP3(self):
        # init
        current_dir = os.path.dirname(os.path.realpath(__file__))
        file1 = '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>file1</title>
            </head>
            <body>
                 <a href="file://{0}/file2.html"></a>
            </body>
            </html>
            '''.format(current_dir)
        file2 = '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>file2</title>
            </head>
            <body>
                <a href="file://{0}/music/Eminem–LoseYourself.mp3"></a>
                <a href="file://{0}/music/Muse–Psycho.mp3"></a>
            </body>
            </html>
            '''.format(current_dir)
        file3 = '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>file3</title>
            </head>
            <body>
                <a href="file://{0}/music/Imagine_Dragon–Demons.mp3"></a>
            </body>
            </html>
            '''.format(current_dir)
        file4 = '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>file4</title>
            </head>
            <body>
                <a href="file://{0}/file1"></a>
                <a href="file://{0}/file3"></a>
            <a href="file://{0}/music/Red_Hot_Chili_Peppers_-_Snow.mp3"></a>
            </body>
            </html>
            '''.format(current_dir)
        test_files = [
            file1,
            file2,
            file3,
            file4,
            ]
        i = 1
        for f in test_files:
            file = open('file%d.html' % i, 'w')
            i = i + 1
            file.write(f)
            file.close()
        files = [
            'file://%s/file1.html' % current_dir,
            'file://%s/file3.html' % current_dir,
            ]
        expected1 = [
            'file://%s/music/Eminem–LoseYourself.mp3' % current_dir,
            'file://%s/music/Muse–Psycho.mp3' % current_dir,
            'file://%s/music/Imagine_Dragon–Demons.mp3' % current_dir,
            'file://%s/music/Red_Hot_Chili_Peppers_-_Snow.mp3' % current_dir,
            ].sort()
        expected2 = [
            'file://%s/music/Eminem–LoseYourself.mp3' % current_dir,
            'file://%s/music/Muse–Psycho.mp3' % current_dir,
            'file://%s/music/Imagine_Dragon–Demons.mp3' % current_dir,
            ].sort()
        parser = LabImpl()
        # work
        result1 = parser.getMP3(files, 3).sort()
        result2 = parser.getMP3(files, 1).sort()
        # test
        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)
        # cleanup
        for f in test_files:
            i = i - 1
            os.remove('file%d.html' % i)


class LabImpl:

    def getFiles(self, file):
        xml = parse(file)
        nodes = xml.getElementsByTagName('file')
        files = [node.childNodes[0].data for node in nodes]
        return files

    def filterMP3(self, listMP3, genre):
        result = []
        for nameMP3 in listMP3:
            if (nameMP3[:4] != "file"):
                mp3 = urllib2.urlopen(nameMP3)
                mp3_content = mp3.read()
                output = open('__tmp__', 'w')
                output.write(mp3_content)
                output.close()

                # filter genre
                if (ID3('__tmp__')['TCON'].text[0].encode('utf-8') == genre):
                    result.append(genre)
            else:
                if (ID3(nameMP3[7:])['TCON'].text[0].encode('utf-8') == genre):
                    result.append(genre)
        return result

    def getMP3(self, files, depth):

        def collect(file, level):
            visited.append(file)
            url = urllib2.urlopen(file)
            content = url.read()
            if (level < depth):
                for f in file_pattern.findall(content):
                    if (f not in visited):
                        collect(f[6:-1], level + 1)
            for mp3 in mp3_pattern.findall(content):
                result.append(mp3[6:-1])

        file_pattern = re.compile(r'href="[^"]+\.x?html?"')
        mp3_pattern = re.compile(r'href="[^"]+\.mp3"')
        result = []
        visited = []
        for file in files:
            collect(file, 0)
        return list(set(result))

if __name__ == '__main__':
    unittest.main()
