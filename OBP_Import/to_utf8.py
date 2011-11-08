#!/usr/bin/env python

from __future__ import with_statement

import os
import sys
import codecs


sourceFormats = ['windows-1252']
#sourceFormats = ['iso-8859-15']
targetFormat = 'utf-8'
outputDir = '/tmp'
#INPUT_FILE = 'test_example_latin1.csv'


def convertFile(fileName):
    print("Converting '" + fileName + "'...")
    for format in sourceFormats:
        try:
            with codecs.open(fileName, 'rU', format) as sourceFile:
                writeConversion(sourceFile)
                print('Done.')
                return
        except UnicodeDecodeError:
            pass

    print("Error: failed to convert '" + fileName + "'.")


def writeConversion(file):
    with codecs.open(outputDir + '/' + fileName, 'w', targetFormat) as targetFile:
        for line in file:
            targetFile.write(line)

def main(input_file):
    global fileName
    fileName = input_file
    convertFile(fileName)

if __name__ == '__main__':
    print "__main__"
