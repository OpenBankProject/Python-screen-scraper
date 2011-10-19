#!/usr/bin/env python
# -*- coding: utf-8 -*-
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


from pymongo import Connection


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
    import re
    print ('starting import')
    connection = Connection('obp_mongod', 27017)
    db = connection.obp_imports


    csv_path = '/home/akendo/PB_Umsatzauskunft_198_rows.csv'
    delimiter = ';'
    quote_char = '"'

    # Need a header check, so to make sure that only transaction data get insert
    # best would be a test for a vaild date format. 
    # re : \d\d\.\d\d\.\d\d\d\d
    data_expression = re.compile('\d\d\.\d\d\.\d\d\d\d')

    
    transactionReader = csv.reader(open(csv_path, 'rb'), delimiter=delimiter, quotechar=quote_char)

    for row in transactionReader:
        #import pdb;pdb.set_trace()
        # The first vaild entry has always a date, checking for it
        if data_expression.match(row[0]) == None:
            continue
        else:
            obp_transaction_row = {  'obp_transaction_date_start': row[0]
                                    ,'obp_transactions_date_complete': row[1]
                                    ,'get_obp_transaction_type_de': row[2]
                                    ,'obp_transaction_data_blob': row[5]
                                    ,'obp_transaction_amount':row[6]
                                    ,'obp_transaction_new_balance':row[7]}
       
            print obp_transaction_row
        #import pdb;pdb.set_trace()
        #collection = db.post_bank_musicpictures.insert(obp_transaction_row)



if __name__ == '__main__':
    do_import()
