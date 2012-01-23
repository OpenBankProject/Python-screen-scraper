#!/usr/bin/env python
# -*- coding: utf-8 -*

import os
import libs.to_utf8
import obp_import_post_bank
import obp_config

def import_from_postbank_testuser():
    # This don't work in the moment, the PostBank 
    # has problem workin with FF. Using anoher Webbrowser are
    # unwell support by Selneium. Else we have to use M$ IE7+
    # This i'll not do! 
    # J.A.S
    #import obp_postbank_get_csv
    print 'Error'
    #csv_file = os.path.join(obp_postbank_get_csv.csv_save_path,obp_postbank_get_csv.csv_files[0])
    return None

    
def main():
    # We can't import in the moment any test CSV, have to call them by hand.
    csv_file = obp_config.CSV_FILE_PATH
    libs.to_utf8.main(csv_file)
    obp_import_post_bank.main(csv_file)




if __name__ == '__main__':
    main()

