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
import obp_config  

from socket import gethostname
from pymongo import Connection
from bson import son
from bson import json_util
from libs.mongodb_handler import insert_into_mongodb



def get_bank_account():
    return 123456


def get_info_from_row(input_row):
    # This regual expression search for all kind of Numbers in a string.
    # Also covering + and - 
    amount = re.match("[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?", input_row[6])
    new_balance = re.match("[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?",input_row[7])
    obp_transaction_dict = {
                            u'obp_transaction_date_start': input_row[0]
                            ,u'obp_transaction_date_complete':input_row[1]
                            ,u'obp_transaction_transaction_type_de':input_row[2]
                            ,u'obp_transaction_comment1': input_row[3].rstrip()
                            ,u'obp_transaction_comment2': input_row[4].rstrip()
                            ,u'obp_transaction_data_blob': input_row[5]
                            ,u'obp_transaction_amount': amount.group()
                            ,u'obp_transaction_new_balance': new_balance.group()
                            }
    return obp_transaction_dict


def parse_row_of_csv(csv_file_to_parse):

        delimiter = ';'
        quote_char = '"'

        # Need a header check, so to make sure that only transaction data get insert
        # best would be a test for a vaild date format. 
        # re : \d\d\.\d\d\.\d\d\d\d
        # This will check of date formarted lile this: 23.01.2001
        data_expression = re.compile('\d\d\.\d\d\.\d\d\d\d')
        transactionReader = csv.reader(open(csv_file_to_parse, 'rb'), delimiter=delimiter, quotechar=quote_char)
    
        for row in transactionReader:
            # The first vaild entry has always a date, checking for it
            if data_expression.match(row[0]) == None:
                continue
            else:
                obp_transaction_dict = get_info_from_row(row)
                # Will now formating obp_string to json
                # We reading a Unicode File. That makes the € to a /xasd, 
                # Will call a dic which get decode from the BSON, so we can insert
                # the single elements not as unicode string. 
                # We inserting also some Information like time(even with tz)
                # and hostname, this should change later to Public IP etc...
                posting = son.SON({
                         'bank_account':get_bank_account()
                        ,'uploader_host': gethostname()
                        ,'insert_date': datetime.datetime.utcnow()
                        ,'obp_transaction': obp_transaction_dict
                        })

            # This will print the no binary JSON, that get insert to mongodb
            # TODO: Need to create Uniq Indexes.
            # To ensure that a Transaction is always uniq
            # LINK: http://www.mongodb.org/display/DOCS/Indexes#Indexes-UniqueIndexes
            print "In the JSON is:\n%s" % posting 
            # Inserting the finisch JSON to the collection 
            #result = insert_into_mongodb(posting) 
            # plural name, no spaces -> singular no spaces model name in Lift mongo record


def main():
    print ('starting import')
    connection = Connection('obp_mongod', 27017)
    db = connection.OBP005

    # Alex Path
    csv_path = '/home/akendo/PB_Umsatzauskunft_198_rows.csv'

    # Simons Path
    #csv_path = '/Volumes/not_on_your_nelly/Bank_statements/PB_Umsatzauskunft_KtoNr0580591101_04-10-2011_1624_saved.csv'

    parse_row_of_csv(csv_path)


if __name__ == '__main__':
    main()
