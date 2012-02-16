# -*- coding: utf-8 -*
__doc__ = """
This is a bundle of function that will help during the import process.
"""
__author__ = ['Jan Alexander Slabiak (alex@tesobe.com)']
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


import os
import sys
import re
import fileinput
import getpass
import datetime
import hashlib


def date_now_formatted():
    """
    Print out nice formatted dates.
    In following order:  Day, Month Year, Hour:Minute:Second
    """

    return datetime.datetime.now().strftime('[%d, %h %Y, %H:%M:%S]')


def check_for_existing_csv(csv_file_path):
    """
    This function will check that the csv file exist.
    TODO:
        Increas the detail of this check, to vaild for
        a true CSV file.
    """

    if os.path.exists(csv_file_path) == False:
        print "ERROR! - NO CSV FILE!"
        sys.exit(255)


def json_formatter(json):
    """
    This is needed for the API! The API can't handle[ and ].
    This will remove the first [ and the last ] of the JSON.
    """

    return re.sub(r'^\[|\]$', ' ', json)


def remove_empty_lines(file):
    """
    There is a problem reading the CSV File with a empty
    newline, so this will remove it.
    This edits the file in place and does not save.
    """

    #Don't remove the print statement, else everything will be removed!
    for lines in fileinput.FileInput(file, inplace=1):
        lines = lines.strip()
        if lines == '':
            continue
        print lines


def check_and_return_csv_file_name(path_to_saved_csv):
    """
    This will check for the right numbers of file then
    return the filename to the CSV_file. Correct is exactly 1.
    """

    #We expect that in the folder is only one file:
    csv_folder = os.listdir(path_to_saved_csv)
    # We expect only one file in this folder
    file_count = len(csv_folder)

    if file_count == 0:
        # TODO Add logging.
        print "ERROR - We didn't get the CSV file."
    elif file_count != 1:
        print "ERROR - We found too many files."

    return csv_folder[0]


def currency_sign_to_text(currency_sign):
    """
    This will return the text currency.
    TODO: Add more currencies to it.
    """

    currency_sign_text_dic = {'\xe2\x82\xac': 'EUR'}
    return currency_sign_text_dic[currency_sign]


def convert_date(date_to_convert):
    """This will convert a German formatted date(17.0.1.2012) to UTC Time."""

    # Will replace the dots of the date with a space. Then split it into 3 parts.
    new_form = re.sub('\.', ' ', date_to_convert)
    date_parts = new_form.split()

    # Getting now the single date, day, month and year
    day = date_parts[0]
    month = date_parts[1]
    year = date_parts[2]

    # We can't see the exact date. setting it to midnight.
    zero_time = datetime.time(0, 0, 0)
    to_convert = datetime.date(
        int(year),
        int(month),
        int(day))
    datetime.datetime.combine(to_convert, zero_time)
    # Will return UTC Date with GMT+1 option.
    return datetime.datetime.strftime(to_convert, "%Y-%m-%dT%H:%M:%S.001Z")


def check_hash(hash_check):
    """Check for a that Hash has the right size."""

    if len(hash_check) != 128:
        print "Value has not enough character for a Hash!"
        raise
    else:
        return hash_check


def create_hash(value_to_hash):
    """This will create a hash and return it"""

    data_hash = hashlib.sha512(value_to_hash).hexdigest()
    return check_hash(data_hash)


def check_existing_hash(hash_to_check, file):
    """
    Will open a file and read it.
    line by line it will compare it with the Input hash
    Return true when it hit something
    """

    valid_hash = check_hash(hash_to_check)
    with open(file, 'r') as file_where_hash_is:
        for saved_hashes in file_where_hash_is.readlines():
            if valid_hash == saved_hashes.strip():
                return True


def inserting_hash(hash_to_insert, file):
    """Will try to insert the Hash_input into the file, if not exist"""

    valid_hash = check_hash(hash_to_insert)
    if check_existing_hash(valid_hash, file) != True:
        file_to_write = open(file, 'a')
        file_to_write.write(valid_hash + '\n')
        file_to_write.close()
        return True
    else:
        return False


def set_bank_account_login():
    """
    This will ask for a username and Password.
    The  password will get via getpass lib.
    """

    username = raw_input("Username: ")
    password = getpass.getpass()
    # We know from the Web Page that we need at least 5 character.
    return username, password


def show_here():
    """Showing current working directory."""

    return os.getcwd()


def clean_up(path_to_clean):
    """This function will clean up in the end all files from tmp/"""

    here = show_here()
    os.chdir(path_to_clean)
    for item in os.listdir(path_to_clean):
        if os.path.isdir(item) == False:
            os.remove(item)

    os.chdir(here)
