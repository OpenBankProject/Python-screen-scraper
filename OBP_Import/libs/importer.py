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

import simplejson as json

import csv
import datetime
import re
import sys

from socket import gethostname
from bson import son
from bson import json_util
from mongodb_handler import *
from import_helper import *
from debugger import debug


sys.path.append("/home/akendo/Work/Tesobe/Pro/Git/try_out/OBP_Import")
from obp_config import *



def get_info_from_row(input_row):
    # This regual expression search for all kind of Numbers in a string.
    # Also covering + and - 
    amount = re.match("[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?", input_row[6])
    new_balance = re.match("[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?",input_row[7])
                            

    holder_name = "Music Pictures Limited"

    obp_transaction_data = json.dumps([
    {
        "this_account": {
            "holder": holder_name,
            "number": get_bank_account(),
            "kind": "",
         "bank": {
                "IBAN": "",
                "national_identifier": "",
                "name": ""
            }
        },
        "other_account": {
            "holder": input_row[4].rstrip(),
            "number": input_row[3].rstrip(),
            "kind": "",
            "bank": {
                "IBAN": "",
                "national_identifier": "",
                "name": ""
            }
        },
        "details": {
            "type_en": "",
            "type_de": input_row[2],
            "posted": input_row[0],
            "completed": input_row[1],
            "value": {
                "currency": "",
                "amount": float(amount.group())
            },
            "other_data": input_row[5]
     }
    }],sort_keys=False)

    print obp_transaction_data
    '''
    obp_transaction_dict = {
                            u'obp_transaction_date_start': 
                            ,u'obp_transaction_date_complete':
                            ,u'obp_transaction_transaction_type_de':
                            ,u'obp_transaction_comment1': 
                            ,u'obp_transaction_comment2': 
                            ,u'obp_transaction_data_blob': 
                            ,u'obp_transaction_amount': 
                            ,u'obp_transaction_new_balance':float(new_balance.group())
                            }
    #print obp_transaction_dict
    '''
    return obp_transaction_data



def parse_row_of_csv(csv_file_to_parse,collection):

        delimiter = ';'
        quote_char = '"'

        # Need a header check, so to make sure that only transaction data get insert
        # best would be a test for a vaild date format. 
        # re : \d\d\.\d\d\.\d\d\d\d
        # This will check of date formarted lile this: 23.01.2001
        data_expression = re.compile('\d\d\.\d\d\.\d\d\d\d')
        transactionReader = csv.reader(open(csv_file_to_parse, 'rb'), delimiter=delimiter, quotechar=quote_char)
    
        for row in transactionReader:
            csv_header_info = []
            # The first vaild entry has always a date, checking for it
            if data_expression.match(row[0]) == None:
                csv_header_info.append(row[0]) 
                debug()
                continue
            else:
                obp_transaction_dict = get_info_from_row(row)
                # Will now formating obp_string to json
                # We reading a Unicode File. That makes the € to a /xasd, 
                # Will call a dic which get decode from the BSON, so we can insert
                # the single elements not as unicode string. 
                # We inserting also some Information like time(even with tz)
                # and hostname, this should change later to Public IP etc...
                '''
                posting = son.SON({
                         'bank_account':
                        ,'uploader_host': gethostname()
                        ,'insert_date': datetime.datetime.utcnow()
                        ,'obp_transaction': obp_transaction_dict
                        })
                '''
            # This will print the no binary JSON, that get insert to mongodb
            # TODO: Need to create Uniq Indexes.
            # To ensure that a Transaction is always uniq
            # LINK: http://www.mongodb.org/display/DOCS/Indexes#Indexes-UniqueIndexes

            print "In the JSON is:\n%s" % obp_transaction_dict
            # Inserting the finisch JSON to the collection 
            #result = insert_into_mongodb(collection,posting) 
            # plural name, no spaces -> singular no spaces model name in Lift mongo record


def main(CSV_input):

    check_for_existing_csv(CSV_input)

    connection = connect_to_mongod(MONGODB_SERVER,MONGODB_SERVER_PORT)
    database = connect_to_mongod_db(connection,MONGODB_DATABASE)
    collection = mongodb_to_collection(database,MONGODB_COLLECTION)
    parse_row_of_csv(CSV_input,collection)


if __name__ == '__main__':
    main('/home/akendo/Work/Tesobe/Pro/Git/try_out/OBP_Import/tmp/PB_Umsatzauskunft_KtoNr9999999999_24-01-2012_1612.csv')
