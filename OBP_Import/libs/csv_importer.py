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
from debugger import *
from scala_api_handler import insert_into_scala


sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__),
    os.path.pardir)))
from obp_config import *


# Here we'll append the Header information of the first rows in
# the CSV before reading the row transaction.
obp_logger.debug("Create empty csv_header_info list.")
csv_header_info = []


def get_posted_date(bank, row):
    if bank == "POSTBANK":
        return convert_date(row[0])
    elif bank == "GLS":
        return convert_date(row[1])
    else:
        raise ValueError("Bank no supported")


def get_completed_date(bank, row):
    if bank == "POSTBANK":
        return convert_date(row[1])
    elif bank == "GLS":
        return convert_date(row[2])
    else:
        raise ValueError("Bank no supported")


def get_this_account_holder(bank, header):
    if bank == "POSTBANK":
        return header[1][1]
    elif bank == "GLS":
        # We can't find the Name of the Holder in the CSV. Hard coded this for now.
        return GLS_BANK_OWERNER
    else:
        raise ValueError("Bank no supported")


def get_this_account_number(bank, row, header):
    if bank == "POSTBANK":
        return header[3][1]
    elif bank == "GLS":
        return row[0]
    else:
        raise ValueError("Bank no supported")


def get_account_currency(bank, row, header):
    obp_logger.debug("set this_account_currency")
    if bank == "POSTBANK":
        this_account_unclean_currency = header[5]
        # warning: EUR-only solution
        return re.search(
            '\xe2\x82\xac',
            this_account_unclean_currency[1]).group()
    elif bank == "GLS":
        return row[-1]


def get_acccout_ammout(bank, row):
    if bank == "POSTBANK":
        obp_logger.debug("replace . with empty string")
        dotless_new_balance = re.sub('\.', '', row[7])
        comma_to_dot_new_balance = re.sub(',', '.', dotless_new_balance)

        new_balance = re.match(
        "[+-]?((\d+(\.\d*)1?)|\.\d+)([eE][+-]?[0-9]+)?",
        comma_to_dot_new_balance)
        return new_balance.group()
    elif bank == "GLS":
        dotless_new_balance = re.sub('\.', '', row[-3])
        comma_to_dot_new_balance = re.sub(',', '.', dotless_new_balance)
        new_balance = re.match(
        "[+-]?((\d+(\.\d*)1?)|\.\d+)([eE][+-]?[0-9]+)?",
        comma_to_dot_new_balance)
        return new_balance.group()
    else:
        raise ValueError("Bank no supported")


def get_acccout_balance(bank, row):
    if bank == "POSTBANK":
        return row[-1]
    elif bank == "GLS":
        dotless_new_balance = re.sub('\.', '', row[-2])
        comma_to_dot_new_balance = re.sub(',', '.', dotless_new_balance)
        new_balance = re.match(
        "[+-]?((\d+(\.\d*)1?)|\.\d+)([eE][+-]?[0-9]+)?",
        comma_to_dot_new_balance)
        return new_balance.group()
    else:
        raise ValueError("Bank no supported")


def get_this_acccount_kind():
    obp_logger.debug("set this_account_kind")
    return "current"


def get_this_account_bank_IBAN(bank, header):
    obp_logger.debug("set this_account_IBAN")
    if bank == "POSTBANK":
        return header[4][1]
    elif bank == "GLS":
        return ""
    else:
        raise ValueError("Bank not supported")


def get_other_account_holder(bank, row, header):
    if bank == "POSTBANK":
        obp_logger.debug("check that this_account_holder is not other_account_holder")
        if row[5].rstrip() != get_this_account_holder(bank, header)[1]:
            return row[5].rstrip()
            obp_logger.debug("set other_account_holder")
        else:
            return row[4].rstrip()
            obp_logger.debug("set other_account_holder")
    elif bank == "GLS":
        return ""
    else:
        raise ValueError("Bank not supported")


def get_transaction_type_de(BANK, row):
    if BANK == "POSTBANK":
        return row[2]
    elif BANK == "GSL":
        return ""
    else:
        raise ValueError("Bank not supported")


def get_other_account_number(bank, row):
    if bank == "POSTBANK":
        return row[3].rstrip()
    elif bank == "GLS":
        return ""
    else:
        raise ValueError("Bank not supported")


def get_other_data(bank, row):
    if bank == "POSTBANK":
        return row[5]
    elif bank == "GLS":
        return ""
    else:
        raise ValueError("Bank not supported")


def get_type_de(bank, row):
    if bank == "POSTBANK":
        return row[2]
    elif bank == "GLS":
        return ""
    else:
        raise ValueError("Bank not supported")


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
    #this_account_holder = csv_header_info[1]

    obp_logger.debug("set this_account_number")
    #this_account_number = csv_header_info[3]

    # There is still some value inside that we need to remove

    obp_logger.debug("set this_account_ni")
    this_account_ni = ""  # ni = national_identifier

    obp_logger.debug("set this_account_bank_name")
    this_account_bank_name = BANK

    # Need to use row 4 if we're sending money,
    # and row 5 when we're getting money.

    # Don't print out the JSON, to ensure no sensitive data gets displayed.
    obp_logger.debug("create json dump")
    obp_transaction_data = json.dumps([
    {
    "obp_transaction": {
        "this_account": {
            "holder": get_this_account_holder(BANK, csv_header_info),
            "number": get_this_account_number(BANK, input_row, csv_header_info),
            "kind": get_this_acccount_kind(),
         "bank": {
                "IBAN": get_this_account_bank_IBAN(BANK, csv_header_info),
                "national_identifier": this_account_ni,
                "name": this_account_bank_name
            }
        },
        "other_account": {
            "holder": get_other_account_holder(BANK, input_row, csv_header_info),
            "number": get_other_account_number(BANK, input_row),
            "kind": "",
            "bank": {
                "IBAN": "",
                "national_identifier": "",
                "name": ""
            }
        },
        "details": {
            "type_en": "",
            "type_de": get_type_de(BANK, input_row),
            "posted": {
                "$dt": get_posted_date(BANK, input_row)
                },
            "completed": {
                "$dt": get_completed_date(BANK, input_row)  # Have to set to $dt so Scala can work with it.
                },
            "new_balance":{
                "currency": get_account_currency(BANK, input_row, csv_header_info),
                "amount": get_acccout_balance(BANK, input_row)
                },
            "value": {
                "currency": get_account_currency(BANK, input_row, csv_header_info),
                "amount": get_acccout_ammout(BANK, input_row)
            },
            "other_data": get_other_data(BANK, input_row)
            }
    }
    }], sort_keys=False)

    obp_logger.debug("obp_transaction_data is %s" % obp_transaction_data)
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

        obp_logger.debug("Create empty transaction_chunks list.")
        transaction_chunks_list = []

        # re : \d\d\.\d\d\.\d\d\d\d
        # This will check if date is formatted like this: 23.01.2001
        obp_logger.debug("Set regular expression to: \d\d\.\d\d\.\d\d")
        data_expression = re.compile('\d\d\.\d\d\.\d\d\d\d')
        number_expression = re.compile("[0-9]")
        obp_logger.debug("starting csv reader")
        transaction_reader = csv.reader(
            open(csv_file_to_parse, 'rb'),
            delimiter=delimiter,
            quotechar=quote_char)

        obp_logger.debug("Start of for loop of transaction_reader")
        if BANK == "POSTBANK":
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

                obp_logger.debug("Decode obp_transaction_dict and append to transaction_chunks_list")
                # Append the last filled JSON as decode python list to the transaction_chunks_list.
                # It needs to decode the JSON, else the later JSON will be messy.
                # It has to ensure, that not too many [ ] are in the list.
                transaction_chunks_list.append(json.loads(json_formatter(obp_transaction_dict)))

            return transaction_chunks_list

        elif BANK == "GLS":
            for row in transaction_reader:
                obp_logger.debug("checking for date in first row from csv")
                if number_expression.match(row[0]) is None:
                    continue
                else:
                    # When we have a valid date, call get_info_from_row.
                    obp_transaction_dict = get_info_from_row(row)
                    obp_logger.debug("call get_info_from_row")

                obp_logger.debug("Decode obp_transaction_dict and append to transaction_chunks_list")
                # Append the last filled JSON as decode python list to the transaction_chunks_list.
                # It needs to decode the JSON, else the later JSON will be messy.
                # It has to ensure, that not too many [ ] are in the list.
                transaction_chunks_list.append(json.loads(json_formatter(obp_transaction_dict)))

            return transaction_chunks_list
        else:
            raise ValueError("Bank no supported")


def main(csv_file_path):
    """Will check for a valid CSV and import it to the Scala API"""

    obp_logger.info("Start Main:")
    obp_logger.debug("csv_file_path is: %s" % csv_file_path)
    obp_logger.debug("Check that csv_file_path is valid path.")
    check_for_existing_csv(csv_file_path)

    obp_logger.debug("Start parse_row_of_csv")
    transaction_chunks_to_insert = parse_row_of_csv(csv_file_path)

    obp_logger.debug("Start inserting to API.")
    # Encode the transaction_chunks_to_insert and insert it to the API.
    api_respone_result = insert_into_scala(
        API_HOST,
        API_HOST_PORT,
        json.dumps(transaction_chunks_to_insert)
        )

    obp_logger.debug("HTTP POST api_respone_result is: %s" % api_respone_result)
    #obp_logger.debug("HTTP POST text from api_respone_result is: %s" % api_respone_result.text)

if __name__ == '__main__':
    print 'Main'
