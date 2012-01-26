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
import re
import sys

from import_helper import *
from debugger import debug
from scala_api_handler import insert_into_scala

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from obp_config import *

csv_header_info = []


def get_info_from_row(input_row):
    # This regual expression search for all kind of Numbers in a string.
    # Also covering + and - 
    # Before we have to remove any dot
    dotless_amount = re.sub('\.','',input_row[6])
    dotless_new_balance = re.sub('\.','',input_row[7])

    comma_to_dot_amount = re.sub(',','.',dotless_amount)
    comma_to_dot_new_balance= re.sub(',','.',dotless_new_balance)
        
    amount = re.match("[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?", comma_to_dot_amount)
    new_balance = re.match("[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?",comma_to_dot_new_balance)
                            

    this_account_name = csv_header_info[1]
    this_account_IBAN = csv_header_info[4]
    this_account_number = csv_header_info[3]
    # There is still some Value inside, we need to remove
    this_account_unclean_currency = csv_header_info[5]
    this_account_currency = re.search('\xe2\x82\xac',this_account_unclean_currency[1])
    this_account_kind = 'current'
    this_account_ni = "" # ni = national_identifier
    this_account_bank_name = 'Postbank'

    debug()

    obp_transaction_data = json.dumps([
    {
    "obp_transaction":{ 
        "this_account": {
            "holder": this_account_name[1],
            "number": this_account_number[1],
            "kind": this_account_kind,
         "bank": {
                "IBAN": this_account_IBAN[1],
                "national_identifier": this_account_ni,
                "name": this_account_bank_name
            }
        },
        "other_account": {
            "holder": input_row[5].rstrip(), 
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
            "posted": {
                "$dt": convert_date(input_row[0])
                },
            "completed": {
                "$dt": convert_date(input_row[1])
                },
            "new_balance":{
                "currency": currency_sign_to_text(this_account_currency.group()),
                "amount": new_balance.group()
                },
            "value": {
                "currency": currency_sign_to_text(this_account_currency.group()),
                "amount": amount.group()
            },
            "other_data": input_row[5]
            }
    }
    }],sort_keys=False)

    return obp_transaction_data



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
                csv_header_info.append(row) 

                continue
            else:
                obp_transaction_dict = get_info_from_row(row)
            
            print "In the JSON is:\n%s" % json_out_correter(obp_transaction_dict)
            result = insert_into_scala(SCALA_HOST,SCALA_PORT,json_out_correter(obp_transaction_dict))
            print result
            print result.text




def main(CSV_input):
    # Will first check for file. 
    check_for_existing_csv(CSV_input)
    parse_row_of_csv(CSV_input)


if __name__ == '__main__':
    print 
