# -*- coding: utf-8 -*
import os
import sys
import re
import fileinput
import getpass

#from postbank_get_csv import check_for_clean_tmp
#from debugger import debug

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
    for item in os.listdir(obp_config.TMP):
        os.remove(item)
    


