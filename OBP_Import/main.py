#!/usr/bin/env python
# -*- coding: utf-8 -*

__author__ = [' Jan Alexander Slabiak (alex@tesobe.com)']
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
import obp_config
import libs.to_utf8
import libs.postbank_get_csv
import libs.import_helper
import libs.csv_importer

from time import sleep


def import_from_postbank(Username,Password):

    csv_save_path = libs.postbank_get_csv.check_for_clean_tmp()    
    libs.postbank_get_csv.get_csv_with_selenium(csv_save_path,Username,Password)
    csv_file = libs.import_helper.preperar_csv_file(csv_save_path)
    csv_path_to = os.path.join(obp_config.TMP,'csv/',csv_file)
    return csv_path_to


def postbank_to_obp(Username,Password):
    # Getting the raw CSV file from PB.
    unconverted_file = import_from_postbank(Username,Password)
    # We need to convert it to UTF-8, else Python can't work with it.
    csv_file = libs.to_utf8.main(unconverted_file)
    # Before we can read the CSV, we remove all empty newlines, else the
    # CSV Parser stops working.
    libs.import_helper.remove_empty_lines(csv_file)
    # Now reading the file and push it to the Scala API
    # TODO: It would be better, when we just getting the JSON back and 
    # then we can descide how to insert. 
    libs.csv_importer.main(csv_file)

    libs.postbank_get_csv.check_for_clean_tmp()
    libs.import_helper.clean_up(obp_config.TMP)
    # After that wait 10 minutes
    sleep((10*60))


def main():
    # This will make sure that the passwor has the 5 let
    logindata = libs.import_helper.set_bankaccount_login()
    while len(logindata[1]) != 5 :
        print "Password hast to contain 5 letters"
        logindata = libs.import_helper.set_bankaccount_login()
    
    while True:
        try:
            postbank_to_obp(logindata[0],logindata[1])
        except KeyboardInterrupt:
                raise
        except:        
            print  "%s:Something went wrong" % libs.import_helper.output_with_date()



if __name__ == '__main__':
    main()

