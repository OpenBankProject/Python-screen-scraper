#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement
#from debugger import debug

import os
import sys
import codecs
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
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
Some code parts coming from stackoverflow .
LINK: http://stackoverflow.com/questions/191359/how-to-convert-a-file-to-utf-8-in-python
"""


source_formats = ['windows-1252']
target_format = 'utf-8'
output_dir = TMP


def convertFile(file_name):
    """Will convert a file to UTF-8"""
    for format in source_formats:
        try:
            with codecs.open(file_name, 'rU', format) as source_file:
                write_conversion(source_file)
                return
        except UnicodeDecodeError:
            pass

    print("Error: failed to convert '" + file_name + "'.")


def write_conversion(file):
    with codecs.open(output_dir + '/' + file_name, 'w', target_format) as target_file:
        for line in file:
            target_file.write(line)


def spilt_path(unclean_path_to_file):
    """First check for a real path, else return None, filename."""
    if os.path.exists(unclean_path_to_file) == True:
        return os.path.split(unclean_path_to_file)
    else:
        return None, unclean_path_to_file


def main(file):
    """Will convert a file to UTF-8 and return the Path + File"""

    # Get the current working directory.
    here = os.getcwd()
    #Need the file_name to set globe, so that other functions can access to it.
    global file_name
    # Spite the Input into file_path and file_name.
    file_path = spilt_path(file)[0]
    file_name = spilt_path(file)[1]

    # Try to get into the file_path, if exist
    try:
        os.chdir(file_path)
    except IOError, e:
        print e

    # Now convert it
    convertFile(file_name)
    # going back to orgin folder
    os.chdir(here)
    return os.path.join(output_dir, file_name)


if __name__ == '__main__':
    print "__main__"
