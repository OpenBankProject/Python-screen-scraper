#!/usr/bin/env python
# -*- coding: utf-8 -*
__doc__ = """
This is the csv_impoter, it will read the CSV file by row. Then dump it out as JSON,
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
from debugger import logger
from scala_api_handler import insert_into_scala


sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__),
    os.path.pardir)))
from obp_config import *


# Here we'll append the Header information of the first rows in
# the CSV before reading the row transaction.
csv_header_info = []


def get_info_from_row(input_row):
    """Read rows and get the transaction data, print as JSON"""

    logger.info("Start get_info_from_row")

    # The Germans formating they Money 1.200,12 Eur. We
    # Need a English format 1200.12 Eur
    # So have to remove the dot and replace the , with a dot.
    # This will turn . to " "
    logger.debug("replace . with space")
    dotless_amount = re.sub('\.', '', input_row[6])
    dotless_new_balance = re.sub('\.', '', input_row[7])

    logger.debug("replace , with .")
    comma_to_dot_amount = re.sub(',', '.', dotless_amount)
    comma_to_dot_new_balance = re.sub(',', '.', dotless_new_balance)

    # This regular expression search for all kind of Numbers in a string.
    # Also covering + and -
    #logger.debug("")
    amount = re.match(
        "[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?",
        comma_to_dot_amount)

    new_balance = re.match(
        "[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?",
        comma_to_dot_new_balance)

    logger.debug("set this_account_holder")
    this_account_holder = csv_header_info[1]

    logger.debug("set this_account_IBAN")
    this_account_IBAN = csv_header_info[4]

    logger.debug("set this_account_number")
    this_account_number = csv_header_info[3]

    # There is still some Value inside, we need to remove
    this_account_unclean_currency = csv_header_info[5]
    this_account_currency = re.search(
        '\xe2\x82\xac',
        this_account_unclean_currency[1])

    logger.debug("set this_account_currency")

    logger.debug("set this_account_kind")
    this_account_kind = 'current'

    logger.debug("set this_account_ni")
    this_account_ni = ""  # ni = national_identifier

    logger.debug("set this_account_bank_name")
    this_account_bank_name = 'Postbank'

    # Need to switch row 4 with 5 when we're the one getting money.
    logger.debug("check that this_account_holder is not other_account_holder")
    if input_row[5].rstrip() != this_account_holder[1]:
        other_account_holder = input_row[5].rstrip()
        logger.debug("set other_account_holder")
    else:
        other_account_holder = input_row[4].rstrip()
        logger.debug("set other_account_holder")

    # I'll not print out the JSON, to ensure no sensible data get displayed.
    logger.debug("create json dump")
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

    logger.debug("Done filling json, return obp_transaction_data")
    return obp_transaction_data


def parse_row_of_csv(csv_file_to_parse):
        """Get rows from CSV file"""

        logger.info("start reading the csv file line by line")
        # This is for the separate in the CSV file
        # TODO: This should be in the obp_config
        delimiter = ';'
        quote_char = '"'
        logger.debug("Set CSV delimiter to: %s" % delimiter)
        logger.debug("Set CSV quote_char to: %s" % quote_char)

        # re : \d\d\.\d\d\.\d\d\d\d
        # This will check if date formatted like this: 23.01.2001
        logger.debug("Set regular expression to: \d\d\.\d\d\.\d\d")
        data_expression = re.compile('\d\d\.\d\d\.\d\d\d\d')
        logger.debug("start csv reader")
        transaction_reader = csv.reader(
            open(csv_file_to_parse, 'rb'),
            delimiter=delimiter,
            quotechar=quote_char)

        logger.debug("Start for loop of transaction_reader")
        for row in transaction_reader:

            # The first valid entry has always a date, checking for it.
            # When not, add this row to the csv_header_info and then continue.
            logger.debug("check for date in first row from csv")
            if data_expression.match(row[0]) == None:
                csv_header_info.append(row)
                logger.debug("append row to csv_header_info, row is: %s" % row)
                continue
            else:
                # When we have a valid date, call get_info_from_row.
                obp_transaction_dict = get_info_from_row(row)
                logger.debug("call get_info_from_row")

            # This will create a hash and return it.
            json_hash = create_hash(json_formatter(obp_transaction_dict))
            logger.debug("create json_hash from obp_transaction_dict")
            # Some debug output. So we may can see the content of the JSON
            # and the Hash.
            logger.info("The hash of the JSON is: %s" % json_hash)
            print "%s:The hash of the JSON is: %s" % (date_now_formatted(), json_hash)

            # Try to insert the hash, check for existing has first.
            # already exist. Return then True, else False
            # and this Hash was already in var/cache
            result = insert_hash_to_cache(json_hash, HASH_FILE)
            if result == True:
                result = insert_into_scala(
                    SCALA_HOST,
                    SCALA_PORT,
                    json_formatter(obp_transaction_dict))

                logger.debug("HTTP POST result is: %s" % result)
                #logger.debug("HTTP POST text from result is: %s" % result.text)
            else:
                logger.info("Transaction is already in hash file, will no inserting")
                print "%s:Transaction is already in hash file, will no inserting" % date_now_formatted()


def main(csv_file_path):
    """Will check for a valid CSV and importing it to the Scala API"""

    logger.info("Start Main")
    logger.debug("csv_file_path is: %s" % csv_file_path)
    logger.debug("Check that csv_file_path is valid path")
    check_for_existing_csv(csv_file_path)

    logger.debug("Start parse_row_of_csv")
    parse_row_of_csv(csv_file_path)


if __name__ == '__main__':
    print 'Main'
