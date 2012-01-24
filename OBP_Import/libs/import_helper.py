# -*- coding: utf-8 -*
import os
import sys
import re
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


def show_here():
    return os.getcwd()


