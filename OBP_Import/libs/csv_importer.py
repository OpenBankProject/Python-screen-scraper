#!/usr/bin/env python
# -*- coding: utf-8 -*
__doc__ = """
This is the csv_importer. It will read the CSV file by row and then dump it out as JSON,
via simplejson. This json output will be hashed and save into var/cache.
Then check, if the hash may already exist. When not it's inserting the JSON via
HTTP PUT to the API.
"""
__author__ = ['simonredfern (simon@tesobe.com)', 'Jan Alexander Slabiak (alex@tesobe.com)']
__license__ = """
  Copyright 2011/2012 Music Pictures Ltd / TESOBE

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
import re
import sys
import os
import simplejson as json

from import_helper import *
from debugger import obp_logger, debug
from scala_api_handler import insert_into_scala


sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__),
    os.path.pardir)))
from obp_config import *


# Here we'll append the Header information of the first rows in
# the CSV before reading the row transaction.
obp_logger.debug("Create empty csv_header_info list.")
csv_header_info = []

obp_logger.debug("Create empty transaction_chunks list.")
transaction_chunks_list = []


def get_info_from_row(input_row):
    """Read rows and get the transaction data, print as JSON"""

    obp_logger.info("Start get_info_from_row")

    # The Germans format money like 1.200,12 Eur. We
    # need a English format, i.e. 1200.12 Eur
    # So have to remove the dot and replace the , with a dot.
    # This will turn . to ""
    obp_logger.debug("replace . with empty string")
    dotless_amount = re.sub('\.', '', input_row[6])
    dotless_new_balance = re.sub('\.', '', input_row[7])

    obp_logger.debug("replace , with .")
    comma_to_dot_amount = re.sub(',', '.', dotless_amount)
    comma_to_dot_new_balance = re.sub(',', '.', dotless_new_balance)

    # This regular expression searches for all kind of numbers in a string.
    # Also covering + and -
    #obp_logger.debug("")
    amount = re.match(
        "[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?",
        comma_to_dot_amount)

    new_balance = re.match(
        "[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?",
        comma_to_dot_new_balance)

    obp_logger.debug("set this_account_holder")
    this_account_holder = csv_header_info[1]

    obp_logger.debug("set this_account_IBAN")
    this_account_IBAN = csv_header_info[4]

    obp_logger.debug("set this_account_number")
    this_account_number = csv_header_info[3]

    # There is still some value inside that we need to remove
    this_account_unclean_currency = csv_header_info[5]
    this_account_currency = re.search(
        '\xe2\x82\xac',
        this_account_unclean_currency[1])

    obp_logger.debug("set this_account_currency")

    obp_logger.debug("set this_account_kind")
    this_account_kind = 'current'

    obp_logger.debug("set this_account_ni")
    this_account_ni = ""  # ni = national_identifier

    obp_logger.debug("set this_account_bank_name")
    this_account_bank_name = 'Postbank'

    # Need to use row 4 if we're sending money,
    # and row 5 when we're getting money.
    obp_logger.debug("check that this_account_holder is not other_account_holder")
    if input_row[5].rstrip() != this_account_holder[1]:
        other_account_holder = input_row[5].rstrip()
        obp_logger.debug("set other_account_holder")
    else:
        other_account_holder = input_row[4].rstrip()
        obp_logger.debug("set other_account_holder")

    # Don't print out the JSON, to ensure no sensitive data gets displayed.
    obp_logger.debug("create json dump")
    obp_transaction_data = json.dumps([
    {
    "obp_transaction": {
        "this_account": {
            "holder": this_account_holder[1],
            "number": this_account_number[1],
            "kind": this_account_kind,
         "bank": {
                "IBAN": this_account_IBAN[1],
                "national_identifier": this_account_ni,
                "name": this_account_bank_name
            }
        },
        "other_account": {
            "holder": other_account_holder,
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
                "$dt": convert_date(input_row[0])  # Have to set to $dt so Scala can work with it.
                },
            "completed": {
                "$dt": convert_date(input_row[1])  # Have to set to $dt so Scala can work with it.
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
    }], sort_keys=False)

    obp_logger.debug("Done filling json, returning obp_transaction_data")
    return obp_transaction_data


def parse_row_of_csv(csv_file_to_parse):
        """Gets rows from CSV file"""

        obp_logger.info("start reading the csv file line by line")
        # This is to set the separators in the CSV file
        # TODO: This should be in the obp_config
        delimiter = ';'
        quote_char = '"'
        obp_logger.debug("Set CSV delimiter to: %s" % delimiter)
        obp_logger.debug("Set CSV quote_char to: %s" % quote_char)

        # re : \d\d\.\d\d\.\d\d\d\d
        # This will check if date is formatted like this: 23.01.2001
        obp_logger.debug("Set regular expression to: \d\d\.\d\d\.\d\d")
        data_expression = re.compile('\d\d\.\d\d\.\d\d\d\d')
        obp_logger.debug("starting csv reader")
        transaction_reader = csv.reader(
            open(csv_file_to_parse, 'rb'),
            delimiter=delimiter,
            quotechar=quote_char)

        obp_logger.debug("Start of for loop of transaction_reader")
        for row in transaction_reader:

            # The first valid entry always has a date: check for it.
            # If it doesn't exist, add this row to the csv_header_info and then continue.
            obp_logger.debug("checking for date in first row from csv")
            if data_expression.match(row[0]) == None:
                csv_header_info.append(row)
                obp_logger.debug("append row to csv_header_info, row is: %s" % row)
                continue
            else:
                # When we have a valid date, call get_info_from_row.
                obp_transaction_dict = get_info_from_row(row)

                obp_logger.debug("call get_info_from_row")

            # This will create a hash and return it.
            json_hash = create_hash(json_formatter(obp_transaction_dict))
            obp_logger.debug("create json_hash from obp_transaction_dict")
            # Some debug output. So that we may can see the content of the JSON
            # and the hash.
            obp_logger.info("The hash of the JSON is: %s" % json_hash)
            print "%s:The hash of the JSON is: %s" % (date_now_formatted(), json_hash)

            # Insert the hash into the cache. If it worked (the hash did not yet exist)
            # send it to the API.
            is_inserted_to_cache = insert_hash_to_cache(json_hash, HASH_FILE)
            if is_inserted_to_cache == True:
                #print json_formatter(json_formatter(obp_transaction_dict))
                transaction_chunks_list.append(json_formatter(obp_transaction_dict))
            else:
                obp_logger.info("Transaction is already in hash file, not returned")
                #print "%s:Transaction is already in hash file, not returned" % date_now_formatted()

        return transaction_chunks_list


def main(csv_file_path):
    """Will check for a valid CSV and import it to the Scala API"""

    obp_logger.info("Start Main:")
    obp_logger.debug("csv_file_path is: %s" % csv_file_path)
    obp_logger.debug("Check that csv_file_path is valid path.")
    check_for_existing_csv(csv_file_path)

    obp_logger.debug("Start parse_row_of_csv")
    transaction_chunks_to_insert = parse_row_of_csv(csv_file_path)

    obp_logger.debug("Start inserting to API.")
    api_respone_result = insert_into_scala(
        SCALA_HOST,
        SCALA_PORT,
        json_formatter(', '.join(transaction_chunks_to_insert))
        )

    print json.dumps(transaction_chunks_to_insert)
    obp_logger.debug("HTTP POST api_respone_result is: %s" % api_respone_result)
    #obp_logger.debug("HTTP POST text from api_respone_result is: %s" % api_respone_result.text)

if __name__ == '__main__':
    print 'Main'
