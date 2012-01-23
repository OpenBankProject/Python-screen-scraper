# -*- coding: utf-8 -*
import os
import sys

def get_bank_account():
    #TODO: This have to get the Bank Account Number
    # This should may place somewhere else.. 
    return 123456


def check_for_existing_csv(input_file):
    # This function will check first for a real csv file.
    # Else expect an external input. This will get check too.
    # Start with the config file 
    if os.path.exists(input_file) ==  False:
        sys.exit(255)


def preperar_csv_file():
    # This will prepare the download file from postbank.
    # it will move it to the 


def show_here():
    return os.getcwd()
