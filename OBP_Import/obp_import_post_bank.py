#!/usr/bin/env python
# -*- coding: utf-8 -*
__author__ = ['simonredfern (simon@tesobe.com)',' Jan Alexander Slabiak (alex@tesobe.com)']
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

import csv
import codecs
import bson
import os
import datetime
import re
import json

from socket import gethostname
from pymongo import Connection
from bson import son
from bson import json_util


'''
def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')
'''


def do_import():
    print ('starting import')
    connection = Connection('obp_mongod', 27017)
    db = connection.OBP005

    # Alex Path
    csv_path = '/home/akendo/PB_Umsatzauskunft_198_rows.csv'

    # Simons Path
    #csv_path = '/Volumes/not_on_your_nelly/Bank_statements/PB_Umsatzauskunft_KtoNr0580591101_04-10-2011_1624_saved.csv'


    delimiter = ';'
    quote_char = '"'

    # Need a header check, so to make sure that only transaction data get insert
    # best would be a test for a vaild date format. 
    # re : \d\d\.\d\d\.\d\d\d\d
    # This will check of date formarted lile this: 23.01.2001
    data_expression = re.compile('\d\d\.\d\d\.\d\d\d\d')
    transactionReader = csv.reader(open(csv_path, 'rb'), delimiter=delimiter, quotechar=quote_char)

    for row in transactionReader:
        # The first vaild entry has always a date, checking for it
        if data_expression.match(row[0]) == None:
            continue
        else:
            # Will now formating obp_string to json
            # We reading a Unicode File. That makes the € to a /xasd, 
            # this regual expression search for all kind of Numbers in a string.
            # Also covering + and - 
            amount = re.match("[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?", row[6])
            new_balance = re.match("[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?", row[7])
            obp_transaction_json = json.dumps({
                                      u'obp_transaction_date_start': row[0]
                                     ,u'obp_transaction_date_complete': row[1]
                                     ,u'obp_transaction_transaction_type_de': row[2]
                                     ,u'obp_transaction_comment1': row[3]
                                     ,u'obp_transaction_comment2': row[4]
                                     ,u'obp_transaction_data_blob': row[5]
                                     ,u'obp_transaction_amount': amount.group()
                                     ,u'obp_transaction_new_balance': new_balance.group()
                             }, separators=(',',':'))
            
            # Will call a dic which get decode from the BSON, so we can insert
            # the single elements not as unicode string. 
            # We inserting also some Information like time(even with tz)
            # and hostname, this should change later to Public IP etc...
            posting = son.SON({
                     'bank_account':1234567
                    ,'uploader_host': gethostname()
                    ,'insert_date': datetime.datetime.utcnow()
                    ,'obp_transaction': obp_transaction_json
                    })

        # This will print the no binary JSON, that get insert to mongodb
        # TODO: Need to create Uniq Indexes.
        # To ensure that a Transaction is always uniq
        # LINK: http://www.mongodb.org/display/DOCS/Indexes#Indexes-UniqueIndexes
        print "In the JSON is:\n%s" % posting 
        # Inserting the finisch JSON to the collection 
        collection = db.obptransactions.insert(posting)
        # plural name, no spaces -> singular no spaces model name in Lift mongo record



if __name__ == '__main__':
    do_import()
