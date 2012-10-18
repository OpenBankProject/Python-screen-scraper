#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement
#from debugger import debug

import os
import codecs


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


def convert_file(file, utf8_file, source_format, target_format):
    """Will convert a file to UTF-8"""

    with codecs.open(file, 'rU', source_format) as source_file:
        write_to(source_file, utf8_file, target_format)


def write_to(source_file, utf8_file, target_format):
    with codecs.open(utf8_file, 'w', target_format) as target_file:
        for line in source_file:
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

    source_format = 'windows-1252'
    target_format = 'utf-8'

    # Spite the Input into file_path and file_name.
    file_path = spilt_path(file)[0] # "/home/obp/.../tmp/csv"
    file_name = spilt_path(file)[1] # "XYZ.csv"

    file_utf8 = file_name.split(".")[0] + "_utf8.csv" # "XYZ_utf8.csv"

    # Try to get into the file_path, if exist
    try:
        os.chdir(file_path)
    except IOError, e:
        print e

    # Now convert it
    convert_file(file_name, file_utf8, source_format, target_format)
    # going back to orgin folder
    os.remove(file_name)
    os.chdir(here)
    return os.path.join(file_path, file_utf8)


if __name__ == '__main__':
    print "__main__"
