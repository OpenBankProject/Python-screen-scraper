# -*- coding: utf-8 -*-
# Server Settings:
__author__ = ['Jan Alexander Slabiak (alex@tesobe.com)']
__license__ = """
  Copyright 2011 Music Pictures Ltd / TESOBE

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
from libs.import_helper import show_here
from os import path
MONGODB_SERVER='obp_mongod'
MONGODB_SERVER_PORT=27017


#MongoDB Setting
MONGODB_DATABASE='OBP006'
MONGODB_COLLECTION='obptransactions'

OBP_VERSION='0.0.1'

# Files:
# The Folder where the CSV file get saved
SAVEDIR=''
TMP = path.join(show_here(),'tmp/')

CSV_FILE_PATH = 'usr/PB_Umsatzauskunft_198_rows.csv'
HTML_FILE_PATH = 'Postbank-Online-Banking_100_days_minus_javascript_cut_down.html'


SCALA_HOST='192.168.1.83'
SCALA_PORT='5588'
