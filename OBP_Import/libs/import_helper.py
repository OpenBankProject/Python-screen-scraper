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


#from postbank_get_csv import check_for_clean_tmp
#from debugger import debug

def output_with_date():
    # This will return a nice formated Date, for log like date output
    return datetime.date.today().strftime('[%d, %h %Y,%H:%M:%S]')
    
    

def get_bank_account():
    #TODO: This have to get the Bank Account Number
    # This should may place somewhere else.. 
    return 123456


def check_for_existing_csv(csv_file_path):
    # This function will check first for a real csv file.
    # Else expect an external input. This will get check too.
    # Start with the config file 
    # TODO: Check for a real CSV FIle in more Detail
    if os.path.exists(csv_file_path) ==  False:
        print "ERROR!"
        print "NO CSV FILE!"
        sys.exit(255)


def json_formatter(json):
    # This is needed for the API!
    # This will remove the first [ and the last ].
    return re.sub(r'^\[|\]$', ' ', json)


def remove_empty_lines(file):
    # There is a problem reading the CSV File with a empty
    # newline, so this will remove it. 
    # This example, found on:
    # LINK: http://ubuntuforums.org/showthread.php?t=302914
    # This edits the file in place and does not save.
    for lines in fileinput.FileInput(file, inplace=1):    
        lines = lines.strip()
        if lines == '': 
            continue



def check_and_return_csv_file_name(path_to_saved_csv):
    # This will return the path + filename to the CSV_file
    # This function is a little bit misleading.
    # Else add the right function to it.
    # it will move it to the tmp folder.

    #We expect that in the folder is only one file:
    csv_folder = os.listdir(path_to_saved_csv)
    # We expect only one file in this folder
    file_count = len(csv_folder) 

    if file_count == 0:
        # TODO Add logging.
        print "ERROR - We didn't get the CSV file."
        exit(1)
    elif file_count != 1:
        print "ERROR - We found too many files."
        exit (10)

    return csv_folder[0]

def currency_sign_to_text(currency_sign):
    # This will return the text currency.
    # TODO Add more currencies to it. 
    currency_sign_text_dic = { '\xe2\x82\xac':'EUR'}
    return currency_sign_text_dic[currency_sign]


def convert_date(date_to_convert):
    # Input date from german: "17.01.2011"
    new_form = re.sub('\.',' ',date_to_convert)
    date_parts = new_form.split()

    day = date_parts[0]
    mounth = date_parts[1]
    year = date_parts[2]

    zero_time = datetime.time(0,0,0)
    to_convert = datetime.date(
        int(year),
        int(mounth),
        int(day))
    datetime.datetime.combine(to_convert,zero_time)
    return datetime.datetime.strftime(to_convert, "%Y-%m-%dT%H:%M:%S.001Z")


def check_hash(HASH_CHECK):
    """Ceck for a leng of a Hash"""
    if len(HASH_CHECK) != 128:
        print "Value has not enough charar for a Hash!"
        raise
    else:
        return HASH_CHECK


def create_hash(VALUE_TO_HASH):
    """This will create a hash and return it"""
    data_hash = hashlib.sha512(VALUE_TO_HASH).hexdigest()
    return check_hash(data_hash)


def check_existing_hash(HASH_TO_CHECK,FILE):
    """Will open a file and read it. 
    line by line it will compre it with the Input hash
    Return true when it hit something"""
    valid_hash = check_hash(HASH_TO_CHECK)
    with open(FILE,'r') as file_where_hash_is:
        for saved_hashes in file_where_hash_is.readlines():
            if valid_hash == saved_hashes.strip():
                return True




def inserting_hash(HASH_TO_INSERT,FILE):
    """WIll try to insert the Hash_input into the file, if not exist"""
    valid_hash = check_hash(HASH_TO_INSERT)
    if check_existing_hash(valid_hash,FILE) != True:
        file_to_write = open(FILE,'a')
        file_to_write.write(valid_hash + '\n')
        file_to_write.close()
        return True
    else:
        return False
    


def set_bank_account_login():
    """THis will ask for a Username and Password.
    Password will get via getpass lib.
    return the Username,Password"""
    Username  = raw_input("Username: ")
    Pasword = getpass.getpass()
    # We know from the Webpage that we need at least 5 charater,
    # reutrn error when password doesn't contain 5 chararters
    return Username,Pasword
 

def show_here():
    """Showing curreny working dir"""
    return os.getcwd()


def clean_up(INPUT):
    """This function will clean up in the end all files from tmp/"""
    #check_for_clean_tmp()
    here = show_here ()
    os.chdir(INPUT)
    for item in os.listdir(INPUT):
        if os.path.isdir(item) == False:
            os.remove(item)

    os.chdir(here) 


