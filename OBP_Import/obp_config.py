# -*- coding: utf-8 -*-
# Server Settings:
__author__ = ['Jan Alexander Slabiak (alex@tesobe.com)']
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
This file sets some importer options:X
Here you are able to set the Host and Port configuration of
your Database or API.
"""


#from libs.import_helper import show_here
from libs.debugger import obp_logger
from os import path
from os import getcwd
# Currently unused but approved.
MONGODB_SERVER = 'obp_mongod'
MONGODB_SERVER_PORT = 27017


#MongoDB Setting
# Name of the Database and the Mongo Collection.
# How to setup a MongoDB:
# LINK: http://www.mongodb.org/display/DOCS/Quickstart
MONGODB_DATABASE = 'OBP006'
MONGODB_COLLECTION = 'obptransactions'

# The importer version
OBP_VERSION = '0.0.1'

# Files:
# The folder where the CSV file gets saved
SAVEDIR = ''
TMP = path.join(getcwd(), 'tmp/')
TMP_CSV_SUFFIX = "csv"

# This can be used to specify a local CSV file.
# TODO: When this file is define. Don't run the postbank_importer
CSV_FILE_PATH = 'usr/PB_Umsatzauskunft_198_rows.csv'
# There is also the alternative of using a HTML file. This
# would get parsed with BeautifulSoup and insert to the MongoDB

HTML_FILE_PATH = ''

# This sets the hostname and port of the Scala API.
SCALA_HOST = 'localhost'  # xE.S : better to call this API_HOST?
SCALA_PORT = '8080'  # E.S : better to call this API_PORT?

# Defines a file where the sha512 hashes of transactions get saved. The hash
# values are used to detect transactions that have already been imported.
HASH_FILE = 'var/cache'


# Logger Settings
# Define Path and Debug level.

LOGGER_NAME = "ImportLogger"
LOGGER_LEVEL = "DEBUG"
LOGGER_TIME_FORMAT = '[%d %h %Y - %H:%M:%S]'