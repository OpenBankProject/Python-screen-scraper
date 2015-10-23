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
    Copyright (C) 2011-2015, TESOBE / Music Pictures Ltd

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Email: contact@tesobe.com
    TESOBE / Music Pictures Ltd
    Osloerstrasse 16/17
    Berlin 13359, Germany
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
