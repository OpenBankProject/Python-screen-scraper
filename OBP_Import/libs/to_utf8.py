#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement

import os
import codecs
from obp_config import TMP

__author__ = [' Jan Alexander Slabiak (alex@tesobe.com)']
__license__ = """
  Copyright 211 Music Pictures Ltd / TESOBE

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
"""

__doc__ = """
This program will convert a latin1 file to UTF-8.

"""



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


def spilt_path(unclean_input):
    # First check for a real path, else return None,filename
    if os.path.exists(unclean_input) ==  True:
        return os.path.split(unclean_input)
    else:
        return None,unclean_input



def main(input_file):
    # Get pwd
    here = os.getcwd()
    global fileName
    filePath = spilt_path(input_file)[0]
    fileName = spilt_path(input_file)[1]
    
    # Try to get into the filePath, if exist
    try:
        os.chdir(filePath)
    except: IOError


    convertFile(fileName)
    os.chdir(here)
    return os.path.join(TMP,fileName)


if __name__ == '__main__':
    print "__main__"
