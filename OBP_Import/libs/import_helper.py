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
import simplejson
import gnupg
from debugger import obp_logger, debug


def date_now_formatted():
    """
    Print out nice formatted dates.
    In following order:  Day, Month Year, Hour:Minute:Second
    """

    obp_logger.debug("setting nicely formatted datetime")
    return datetime.datetime.now().strftime('[%d, %h %Y, %H:%M:%S]')


def check_for_existing_csv(csv_file_path):
    """
    This function will check that the csv file exists.
    TODO:
        Increase the detail of this check, to ensure there
        really is a CSV file.
    """

    obp_logger.debug("checking if csv_file_path %s exists" % csv_file_path)
    if os.path.exists(csv_file_path) == False:
        print "ERROR! - NO CSV FILE!"
        obp_logger.error("ERROR! - NO CSV FILE!")
        raise IOError
    else:
        obp_logger.debug("csv_file_path %s exist" % csv_file_path)


def check_for_clean_folder(check_path):
    """Check for an empty folder. Else create it."""

    obp_logger.info("Check for empty and exists folder")
    obp_logger.debug("Check that %s exists" % check_path)
    if os.path.exists(check_path) != True:
        obp_logger.debug("%s no there, create it")
        os.makedirs(check_path)

    # Check for an empty folder
    obp_logger.debug("Check for empty folder")
    if len(os.listdir(check_path)) != 0:
        obp_logger.debug("Getting length of items in %s" % check_path)
        obp_logger.debug("Try to remove items in check_path")
        for item in os.listdir(check_path):
            item_to_remove = os.path.join(check_path, item)
            obp_logger.debug("Item is %s" % item_to_remove)
            try:
                os.remove(item_to_remove)
            except OSError, e:
                obp_logger.warn("Can't remove %s" % e)


def json_formatter(json):
    """
    This will remove the first [ and the last ] of the JSON.
    """

    obp_logger.debug("removing [ and ] from json")
    return re.sub(r'^\[|\]$', ' ', json)


def remove_empty_lines(file):
    """
    There is a problem reading the CSV File with a empty
    newline, so this will remove it.
    This edits the file in place and does not save it.
    """

    #Don't remove the print statement, else everything will be removed!
    obp_logger.debug("starting for loop to remove newlines")
    for lines in fileinput.FileInput(file, inplace=1):
        lines = lines.strip()
        if lines == '':
            continue
        print lines


def check_and_return_csv_file_name(path_to_saved_csv):
    """
    Check that there is only one csv file, and then return it.
    """

    obp_logger.debug("check and return filename")
    #obp_logger.debug("path_to_saved_csv is: %s" % path_to_saved_csv)
    #We expect that in the folder is only one file:
    csv_folder = os.listdir(path_to_saved_csv)
    # We expect only one file in this folder
    file_count = len(csv_folder)
    obp_logger.debug("File count in csv_folder: %s" % file_count)

    if file_count == 0:
        obp_logger.error("ERROR - We didn't get the CSV file.")
        print "ERROR - We didn't get the CSV file."
    elif file_count != 1:
        obp_logger.error("ERROR - We found too many files.")
        print "ERROR - We found too many files."

    obp_logger.debug("return csv_folder")
    return csv_folder[0]


def currency_sign_to_text(currency_sign):
    """
    This will convert the currency sign to ISO 4217 currency codes.
    TODO: Add more currencies.
    #E.S. This will get tricky as it depends on locale. For example $
    #E.S. can be USD, CAD, AUD, etc.
    """

    obp_logger.debug("looking up key: %s" % currency_sign)
    currency_sign_text_dic = {'\xe2\x82\xac': 'EUR'}
    obp_logger.debug("returning value: %s text currency" % currency_sign_text_dic[currency_sign])
    return currency_sign_text_dic[currency_sign]


def convert_date(date_to_convert):
    """This will convert a German formatted date(17.0.1.2012) to UTC Time."""
    #E.S. It's probably better to find a library to do this than to use regexes.
    # Will replace the dots of the date with a space.
    # Then split it into 3 parts.
    new_form = re.sub('\.', ' ', date_to_convert)
    obp_logger.debug("replace . with ' ' in date_to_convert")

    date_parts = new_form.split()
    obp_logger.debug("split date_to_convert: %s" % date_to_convert)

    # Getting now the single date, day, month and year
    day = date_parts[0]
    obp_logger.debug("Setting day")

    month = date_parts[1]
    obp_logger.debug("setting month")

    year = date_parts[2]
    obp_logger.debug("setting year")

    # We can't set the exact date as we only have the day, month, and year,
    # so we'll just set it to midnight.
    zero_time = datetime.time(0, 0, 0)
    obp_logger.debug("setting time to midnight")

    to_convert = datetime.date(
        int(year),
        int(month),
        int(day))
    obp_logger.debug("Merge single date items together in to_convert")

    datetime.datetime.combine(to_convert, zero_time)
    obp_logger.debug("convert to_convert to datetime object")

    # Will return UTC Date with GMT+1 option.
    obp_logger.debug("return UTC formatted datetime")
    return datetime.datetime.strftime(to_convert, "%Y-%m-%dT%H:%M:%S.001Z")


def check_hash(hash_to_check):
    """Checks the hash for the correct size"""

    obp_logger.debug("Checking length of hash")
    if len(hash_to_check) != 128:
        obp_logger.critiacl("Value does not have enough characters for a hash")
        print "Value does not have enough characters for a hash!"
        raise
    else:
        obp_logger.debug("Hash length is fine, returning hash_to_check: %s" % hash_to_check)
        return hash_to_check


def create_hash(value_to_hash):
    """This will create a hash and return it"""

    obp_logger.info("Creating hash with sha512")
    data_hash = hashlib.sha512(value_to_hash).hexdigest()
    obp_logger.debug("created hash is in hexdigest: %s" % data_hash)
    return check_hash(data_hash)


def check_for_existing_cache(cache_file):
    """This will check for a existing cache_file"""

    obp_logger.debug("checking for existing cache_file: %s" % cache_file)
    if os.path.exists(cache_file) == False:
        print "ERROR! - NO CACHE FILE!"
        obp_logger.error("ERROR! - NO CACHE FILE!")
        raise

    else:
        obp_logger.debug("cache file exist")


def check_existing_hashs(hash_to_check, file):
    """
    Will open a file and read it.
    line by line it will compare it with the input hash
    Return true when it hit something
    """
    #E.S. Confusingly named function? Should it be hash_exists?
    obp_logger.debug("checking for existing hash")
    valid_hash = check_hash(hash_to_check)
    obp_logger.debug("check for valid hash, hash is: %s" % valid_hash)

    obp_logger.debug("Checking for existing cache_file")
    check_for_existing_cache(file)

    obp_logger.debug("opening cache file readonly: %s" % file)
    with open(file, 'r') as file_where_hash_is:
        obp_logger.debug("looping through the cache file")
        for saved_hashes in file_where_hash_is.readlines():
            obp_logger.debug("line is: %s" % saved_hashes.strip())
            obp_logger.debug("Comparing valid_hash with line from cache file")
            if valid_hash == saved_hashes.strip():
                obp_logger.debug("Found valid_hash, returning True")
                return True


def insert_hash_to_cache(hash_to_insert, file):
    """Will insert the Hash_input into the file, if it isn't already there"""

    obp_logger.debug("start insert_hash")
    obp_logger.debug("check for valid_hash")
    valid_hash = check_hash(hash_to_insert)
    obp_logger.debug("read cache file for existing hash")
    if check_existing_hashs(valid_hash, file) != True:
        obp_logger.debug("Opening cache file, appending")
        file_to_write = open(file, 'a')
        obp_logger.debug("writing hash to file, hash is: %s" % valid_hash)
        file_to_write.write(valid_hash + '\n')
        obp_logger.debug("closing cache file")
        file_to_write.close()
        obp_logger.debug("returning True")
        return True
    else:
        obp_logger.info("Hash already inserted")
        return False


def set_bank_account_login():
    """
    This will ask for a username and Password.
    The password will be retrieved via getpass lib.
    Requires the password length to be at least 5 characters.
    """

    # Getting the login name from a raw_input.
    obp_logger.info("getting account number")
    username = raw_input("Account Number: ")
    obp_logger.debug("account number is set")

    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        pinfile = sys.argv[1]
        obp_logger.info("switching to 'encrypted PIN' mode")
        print "trying to use file '%s' as encrypted PIN container" % pinfile
        passphrase = getpass.getpass("Enter passphrase for file: ")
        gpg = gnupg.GPG()
        decrypted = str(gpg.decrypt_file(open(pinfile), passphrase=passphrase)).strip()
        if decrypted:
          password = decrypted
        else:
          print "sorry, decryption failed"
          sys.exit(1)
    else:
        if len(sys.argv) > 1: # ... but sys.argv[1] is not a file
            print "'%s' is not a proper file, falling back to password mode" % sys.argv[1]
        # Now getting the password via getpass lib.
        obp_logger.info("get password")
        password = getpass.getpass()
        obp_logger.debug("Password has set")

        # We know from the Web Page that we need at least 5 characters.
        # This will check for the right length of the password.
        obp_logger.debug("start while loop")
        while len(password) < 5:
            obp_logger.error("Password was not 5 character long")
            print "Password has to contain at least 5 letters"
            password = getpass.getpass()
            obp_logger.debug("Password has set")

    obp_logger.debug("Will return username: %s ,password is set" % username)
    # Return username and password.
    return username, password


def show_here():
    """Showing current working directory."""

    obp_logger.debug("return current working directory")
    return os.getcwd()


def clean_up(path_to_clean):
    """This function will clean up all files from tmp/"""

    here = show_here()
    obp_logger.debug("here is: %s" % here)

    os.chdir(path_to_clean)
    obp_logger.debug("changing to path_to_clean: %s" % path_to_clean)

    obp_logger.debug("for loop on every element in dir")
    for item in os.listdir(path_to_clean):
        obp_logger.debug("checking that item is not a folder")
        if os.path.isdir(item) == False:
            obp_logger.debug("item is not a dir")
            obp_logger.debug("deleting item: %s" % item)
            os.remove(item)

    obp_logger.debug("chdir to here: %s" % here)
    os.chdir(here)
