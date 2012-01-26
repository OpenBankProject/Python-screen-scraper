# -*- coding: utf-8 -*
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
from debugger import debug

def get_bank_account():
    #TODO: This have to get the Bank Account Number
    # This should may place somewhere else.. 
    return 123456


def check_for_existing_csv(input_file):
    # This function will check first for a real csv file.
    # Else expect an external input. This will get check too.
    # Start with the config file 
    if os.path.exists(input_file) ==  False:
        print "ERROR!"
        print "NO CSV FILE!"
        sys.exit(255)


def json_out_correter(JSON_to_print):
    # This will remove the first [ and the last ].
    return re.sub(r'^\[|\]$', ' ', JSON_to_print)


def remove_empty_lines(INPUT):
    # There is a problem reading the CSV File with a empty
    # newline, so this will remove it. 
    # This example, found on:
    # http://ubuntuforums.org/showthread.php?t=302914
    for lines in fileinput.FileInput(INPUT, inplace=1):    
        lines = lines.strip()
        if lines == '': 
            continue
        print lines



def preperar_csv_file(path_to_saved_csv):
    # This will prepare the download file from postbank.
    # it will move it to the tmp folder. Then it will be 
    # converted to a UTF-8 csv file. 

    #We expect that in the folder is only one file:
    csv_folder = os.listdir(path_to_saved_csv)
    file_count = len(csv_folder) 

    if file_count == 0:
        print "We didn't got the CSV file."
        exit(1)
    elif file_count != 1:
        print "We did got to much files..."
        exit (10)

    return csv_folder[0]

def currency_sign_to_text(currency_sign):
    # This will return the text currney.
    currency_sing_text_dic = { '\xe2\x82\xac':'EUR'}
    return currency_sing_text_dic[currency_sign]


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
    if len(HASH_CHECK) != 128:
        print "No hash"
        raise
    else:
        return HASH_CHECK


def create_hash(VALUE_TO_HASH):
    # This will create a hash and return it
    data_hash = hashlib.sha512(VALUE_TO_HASH).hexdigest()
    return check_hash(data_hash)


def check_existing_hash(HASH_TO_CHECK,FILE):
    valid_hash = check_hash(HASH_TO_CHECK)
    print 'check_existing_hash: valid_hash is:',valid_hash
    with open(FILE,'r') as file_where_hash_is:
        for saved_hashes in file_where_hash_is.readlines():
            print saved_hashes
            if valid_hash == saved_hashes.strip():

                print valid_hash
                print saved_hashes
                return True




def inserting_hash(HASH_TO_INSERT,FILE):
    print "validing Hash"
    valid_hash = check_hash(HASH_TO_INSERT)
    print "Hash is",valid_hash
    if check_existing_hash(valid_hash,FILE) != True:
        file_to_write = open(FILE,'a')
        print "Opening file"
        file_to_write.write(valid_hash + '\n')
        print "Wirting to file with",valid_hash
        file_to_write.close()
        print "Close file"
    


def set_bankaccount_login():
    # THis will return the Username,Password
    Username  = raw_input("Username: ")
    Pasword = getpass.getpass()
    # We know from the Webpage that we need at least 5 charater,
    # reutrn error when password doesn't contain 5 chararters
    return Username,Pasword
 

def show_here():
    return os.getcwd()


def clean_up(INPUT):
    # This function will clean up in the end all files from tmp/
    #check_for_clean_tmp()
    for item in os.listdir(INPUT):
        os.remove(item)
    


