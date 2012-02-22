# -*- coding: utf-8 -*
__doc__ = """
This is a bundle of functions that will help during the import process.
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
from debugger import logger


def date_now_formatted():
    """
    Print out nice formatted dates.
    In following order:  Day, Month Year, Hour:Minute:Second
    """

    logger.debug("setting nicely formatted datetime")
    return datetime.datetime.now().strftime('[%d, %h %Y, %H:%M:%S]')


def check_for_existing_csv(csv_file_path):
    """
    This function will check that the csv file exists.
    TODO:
        Increase the detail of this check, to ensure there
        really is a CSV file.
    """

    logger.debug("checking if csv_file_path %s exists" % csv_file_path)
    if os.path.exists(csv_file_path) == False:
        print "ERROR! - NO CSV FILE!"
        logger.error("ERROR! - NO CSV FILE!")
        raise

    else:
        logger.debug("csv_file_path %s exist" % csv_file_path)


def json_formatter(json): #E.S. maybe a better name would be format_json?
    """
    This is needed for the API! The API can't handle[ and ].
    This will remove the first [ and the last ] of the JSON.
    """

    logger.debug("removing [ and ] from json")
    return re.sub(r'^\[|\]$', ' ', json)


def remove_empty_lines(file):
    """
    There is a problem reading the CSV File with a empty
    newline, so this will remove it.
    This edits the file in place and does not save it.
    """

    #Don't remove the print statement, else everything will be removed!
    logger.debug("starting for loop to remove newlines")
    for lines in fileinput.FileInput(file, inplace=1):
        lines = lines.strip()
        if lines == '':
            continue
        print lines


def check_and_return_csv_file_name(path_to_saved_csv):
    """
    Check that there is only one csv file, and then return it.
    """

    logger.debug("check and return filename")
    #logger.debug("path_to_saved_csv is: %s" % path_to_saved_csv)
    #We expect that in the folder is only one file:
    csv_folder = os.listdir(path_to_saved_csv)
    # We expect only one file in this folder
    file_count = len(csv_folder)
    logger.debug("File count in csv_folder: %s" % file_count)

    if file_count == 0:
        logger.error("ERROR - We didn't get the CSV file.")
        print "ERROR - We didn't get the CSV file."
    elif file_count != 1:
        logger.error("ERROR - We found too many files.")
        print "ERROR - We found too many files."

    logger.debug("return csv_folder")
    return csv_folder[0]


def currency_sign_to_text(currency_sign):
    """
    This will convert the currency sign to ISO 4217 currency codes.
    TODO: Add more currencies.
    #E.S. This will get tricky as it depends on locale. For example $
    #E.S. can be USD, CAD, AUD, etc.
    """

    logger.debug("looking up key: %s" % currency_sign)
    currency_sign_text_dic = {'\xe2\x82\xac': 'EUR'}
    logger.debug("returning value: %s text currency" % currency_sign_text_dic[currency_sign])
    return currency_sign_text_dic[currency_sign]


def convert_date(date_to_convert):
    """This will convert a German formatted date(17.0.1.2012) to UTC Time."""
    #E.S. It's probably better to find a library to do this than to use regexes.
    # Will replace the dots of the date with a space.
    # Then split it into 3 parts.
    new_form = re.sub('\.', ' ', date_to_convert)
    logger.debug("replace . with ' ' in date_to_convert")

    date_parts = new_form.split()
    logger.debug("split date_to_convert: %s" % date_to_convert)

    # Getting now the single date, day, month and year
    day = date_parts[0]
    logger.debug("Setting day")

    month = date_parts[1]
    logger.debug("setting month")

    year = date_parts[2]
    logger.debug("setting year")

    # We can't set the exact date as we only have the day, month, and year,
    # so we'll just set it to midnight.
    zero_time = datetime.time(0, 0, 0)
    logger.debug("setting time to midnight")

    to_convert = datetime.date(
        int(year),
        int(month),
        int(day))
    logger.debug("Merge single date items together in to_convert")

    datetime.datetime.combine(to_convert, zero_time)
    logger.debug("convert to_convert to datetime object")

    # Will return UTC Date with GMT+1 option.
    logger.debug("return UTC formatted datetime")
    return datetime.datetime.strftime(to_convert, "%Y-%m-%dT%H:%M:%S.001Z")


def check_hash(hash_to_check):
    """Checks the hash for the correct size"""

    logger.debug("Checking length of hash")
    if len(hash_to_check) != 128:
        logger.critiacl("Value does not have enough characters for a hash")
        print "Value does not have enough characters for a hash!"
        raise
    else:
        logger.debug("Hash length is fine, returning hash_to_check: %s" % hash_to_check)
        return hash_to_check


def create_hash(value_to_hash):
    """This will create a hash and return it"""

    logger.info("Creating hash with sha512")
    data_hash = hashlib.sha512(value_to_hash).hexdigest()
    logger.debug("created hash is in hexdigest: %s" % data_hash)
    return check_hash(data_hash)


def check_for_existing_cache(cache_file):
    """This will check for a existing cache_file"""

    logger.debug("checking for existing cache_file: %s" % cache_file)
    if os.path.exists(cache_file) == False:
        print "ERROR! - NO CACHE FILE!"
        logger.error("ERROR! - NO CACHE FILE!")
        raise

    else:
        logger.debug("cache file exist")


def check_existing_hashs(hash_to_check, file):
    """
    Will open a file and read it.
    line by line it will compare it with the input hash
    Return true when it hit something
    """
    #E.S. Confusingly named function? Should it be hash_exists?
    logger.debug("checking for existing hash")
    valid_hash = check_hash(hash_to_check)
    logger.debug("check for valid hash, hash is: %s" % valid_hash)

    logger.debug("Checking for existing cache_file")
    check_for_existing_cache(file)

    logger.debug("opening cache file readonly: %s" % file)
    with open(file, 'r') as file_where_hash_is:
        logger.debug("looping through the cache file")
        for saved_hashes in file_where_hash_is.readlines():
            logger.debug("line is: %s" % saved_hashes.strip())
            logger.debug("Comparing valid_hash with line from cache file")
            if valid_hash == saved_hashes.strip():
                logger.debug("Found valid_hash, returning True")
                return True


def insert_hash_to_cache(hash_to_insert, file):
    """Will insert the Hash_input into the file, if it isn't already there"""

    logger.debug("start insert_hash")
    logger.debug("check for valid_hash")
    valid_hash = check_hash(hash_to_insert)
    logger.debug("read cache file for existing hash")
    if check_existing_hashs(valid_hash, file) != True:
        logger.debug("Opening cache file, appending")
        file_to_write = open(file, 'a')
        logger.debug("writing hash to file, hash is: %s" % valid_hash)
        file_to_write.write(valid_hash + '\n')
        logger.debug("closing cache file")
        file_to_write.close()
        logger.debug("returning True")
        return True
    else:
        logger.info("Hash already inserted")
        return False


def set_bank_account_login():
    """
    This will ask for a username and Password.
    The password will be retrieved via getpass lib.
    Requires the password length to be at least 5 characters.
    """

    # Getting the login name from a raw_input.
    logger.info("get username")
    username = raw_input("Username: ")
    logger.debug("username is set")

    # Now getting the password via getpass lib.
    logger.info("get password")
    password = getpass.getpass()
    logger.debug("password has set")

    # We know from the Web Page that we need at least 5 characters.
    # This will check for the right length of the password.
    logger.debug("start while loop")
    while len(password) < 5:
        logger.error("Password was not 5 character long")
        print "Password has to contain at least 5 letters"
        password = getpass.getpass()
        logger.debug("Password has set")

    logger.debug("Will return username: %s ,password is set" % username)
    # Return username and password.
    return username, password


def show_here():
    """Showing current working directory."""

    logger.debug("return current working directory")
    return os.getcwd()


def clean_up(path_to_clean):
    """This function will clean up all files from tmp/"""

    here = show_here()
    logger.debug("here is: %s" % here)

    os.chdir(path_to_clean)
    logger.debug("changing to path_to_clean: %s" % path_to_clean)

    logger.debug("for loop on every element in dir")
    for item in os.listdir(path_to_clean):
        logger.debug("checking that item is not a folder")
        if os.path.isdir(item) == False:
            logger.debug("item is not a dir")
            logger.debug("deleting item: %s" % item)
            os.remove(item)

    logger.debug("chdir to here: %s" % here)
    os.chdir(here)
