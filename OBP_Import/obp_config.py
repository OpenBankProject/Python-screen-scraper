# -*- coding: utf-8 -*-
# Server Settings:
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
TMP= path.join(show_here(),'tmp/')

CSV_FILE_PATH = 'usr/PB_Umsatzauskunft_198_rows.csv'
HTML_FILE_PATH = 'Postbank-Online-Banking_100_days_minus_javascript_cut_down.html'


