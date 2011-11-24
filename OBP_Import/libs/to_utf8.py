#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement

import os
import sys
import codecs
from obp_config import TMP


sourceFormats = ['windows-1252']
#sourceFormats = ['iso-8859-15']
targetFormat = 'utf-8'
#outputDir = '/tmp'
outputDir = TMP
#INPUT_FILE = 'test_example_latin1.csv'


def convertFile(fileName):
    for format in sourceFormats:
        try:
            with codecs.open(fileName, 'rU', format) as sourceFile:
                writeConversion(sourceFile)
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
    return os.path.join(TMP,fileName)

if __name__ == '__main__':
    print "__main__"
