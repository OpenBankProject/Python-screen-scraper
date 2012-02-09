#!/usr/bin/env python
# -*- coding: utf-8 -*
__doc__ = """
This is the main program.
It gets a CSV file from Postbank and then inserts it via
the Scala Lift API to the Database backend.

Dependencies: Scala API
at: https://github.com/OpenBankProject/OpenBankProject-Server
"""

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


def import_from_postbank(username, password):
    """
    Imports a csv from postbank. calls the postbank_get_csv file and
    starts the Selenium Browser (Firefox) to access Postbank.
    """
    # TODO: When no username and password is set, use the demo login.
    csv_save_path = libs.postbank_get_csv.check_for_clean_tmp()
    libs.postbank_get_csv.get_csv_with_selenium(csv_save_path, username, password)
    csv_file = libs.import_helper.preperar_csv_file(csv_save_path)
    csv_path_to = os.path.join(obp_config.TMP, 'csv/', csv_file)
    return csv_path_to


def postbank_to_obp(username, password):
    """
    Retrieves the csv from postbank and posts it into the OpenBankProject server
    """
    # TODO: Some of this functionality should probably move inside the csv parser/importer.
    #       This function should in theory only call two functions:
    #       1. get_csv_from_postbank()
    #       2. push_csv_to_obp(csv)
    #
    #       Any complexities should then be handled by those functions
    # (y.a.)
    # Getting the raw CSV file from PostBank.
    unconverted_file = import_from_postbank(username, password)
    # We need to convert it to UTF-8. Otherwise Python can't work with it.
    csv_file = libs.to_utf8.main(unconverted_file)
    # Before we can read the CSV, we remove all empty newlines.
    # Otherwise the CSV Parser stops working.
    libs.import_helper.remove_empty_lines(csv_file)
    # Now reading the file and pushing it to the Scala API
    # TODO: It would be better, when we just getting the JSON back and
    # then we can descide how to insert.
    libs.csv_importer.main(csv_file)

    # Clean up and remove all files.
    # TODO: using the tempfile library might be much more efficient/clean.
    #       (y.a.)
    libs.postbank_get_csv.check_for_clean_tmp()
    libs.import_helper.clean_up(obp_config.TMP)
    # wait 10 minutes
    sleep(10 * 60)


def main():
    # This will make sure that the password has at least 5 charachters
    # (Checks like this should probably move inside the function,
    #  althought they might not be at all necessary.
    #  Use error handling for incorrect auth instead. y.a.)
    logindata = libs.import_helper.set_bankaccount_login()
    while len(logindata[1]) != 5:
        print "Password hast to contain 5 letters"
        logindata = libs.import_helper.set_bankaccount_login()

    # TODO: Need handling of System singls to run this as a daemon.
    while True:
        try:
            postbank_to_obp(logindata[0], logindata[1])
            # TODO: Need another exeption for not getting the CSV File.
        except KeyboardInterrupt:
                raise
        except Exception, e:
            # TODO: need a cleanup as well, just to be sure no sensitive data left on the filesystem.
            print "%s:Something went wrong" % libs.import_helper.output_with_date()
            print "Error is %s" % e
            sleep(5)


if __name__ == '__main__':
    main()

