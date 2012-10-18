    #!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = [' Jan Alexander Slabiak (alex@tesobe.com)']
__license__ = """
  Copyright 211 Music Pictures Ltd / TESOBE

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

__doc__ = """
Using Selenium RC2, install it with "pip install selenium"
need also =>selenium-2.0

This tool will take control of a local Firefox and download the CSV file from PB.
TMP is in the obp_config, this is important. Not every system has a /tmp (also related
to win32 systems)

I disabled the obp_logger, because the webdriver of selenium used it as well and printed
out sensible data. I wasn't able to control this behavior of selenium.
Have to find a fix for this!
J.A.S
"""


import os
import time

from obp_config import TMP, TMP_CSV_SUFFIX
from libs.import_helper import check_for_clean_folder
from selenium import webdriver
from debugger import obp_logger, debug
from selenium.common.exceptions import (NoSuchElementException,
    ElementNotVisibleException)

from selenium.webdriver.support.ui import Select

#gls_main_url_login_page = "https://internetbanking.gad.de/ptlweb/WebPortal?bankid=4967&modus=demo
gls_main_url_value_page = "https://internetbanking.gad.de/ptlweb/WebPortal?timeout=4967&applId=obaban&frame=content&wp_token_obaban=1364634655&event=anzeigenKontoUmsatzUebersicht&idEuroKontoGewaehlt=0"
gls_main_url_value_download = "https://internetbanking.gad.de/ptlweb/WebPortal?timeout=4967&applId=obaban&frame=content&wp_token_obaban=291125145&event___export=Link"


def gls_get_csv_with_selenium(gls_main_url_login_page, path_to_save_csv, username, password):
    """Getting CSV file via Firefox, controlled by Selenium webdriver"""
    # TODO: When no username and password is set, use the demo login.
    # Clean up the OBP temp folder (delete all csv files there).
    # LINK: http://seleniumhq.org/docs/03_webdriver.html#getting-started-with-selenium-webdriver
    obp_logger.info("Starting gls_get_csv")
    obp_logger.info("Setting csv_folder...")

    # Check for existing and empty tmp
    check_for_clean_folder(path_to_save_csv)

    csv_save_path = os.path.join(os.getcwd(), path_to_save_csv, TMP_CSV_SUFFIX)
    obp_logger.debug("csv_folder is: %s" % csv_save_path)

    check_for_clean_folder(csv_save_path)

    obp_logger.info("Start Selenium")
    obp_logger.debug("csv_save_path: %s" % csv_save_path)
    obp_logger.debug("username is set")
    obp_logger.debug("password is set")

    # Setting up a Profile for Firefox.
    # Proxy is disabled and download files without asking.
    obp_logger.info("Setup Firefox Profile")
    fp = webdriver.FirefoxProfile()

    obp_logger.debug("webdriver firefox")
    fp.set_preference("network.proxy.type", 0)
    obp_logger.debug("network.proxy.type 0")
    fp.set_preference("browser.download.folderList", 2)
    obp_logger.debug("browser.download.fold 2")

    fp.set_preference("browser.download.manager.showWhenStarting", False)
    obp_logger.debug("browser.download.manager.showWhenStarting False")
    fp.set_preference("browser.download.dir", csv_save_path)
    obp_logger.debug("browser.download.dir %s" % csv_save_path)

    # Need to set CSV to saveToDisk, else it's unknown to FF and it will ask for it
    #fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-unknown-content-type")

    obp_logger.info("Start Firefox")
    browser = webdriver.Firefox(firefox_profile=fp)  # Get local session of firefox

    obp_logger.debug("Open URL: %s" % gls_main_url_login_page)
    browser.get(gls_main_url_login_page)  # Load page
    assert "GLS Gemeinschaftsbank eG Online-Filiale" in browser.title

    #selenium.set_browser_log_level("error")

    # Here we will insert the username and password:
    # find the element that's name attribute is nutzername and kennwort
    obp_logger.info("Inserting Username and Password to Login")
    obp_logger.debug("searching for login box")

    inputElement_username = browser.find_element_by_name("sBAuthentifizierungInpVO.nrKonto")
    obp_logger.debug("searching for password box")
    inputElement_password = browser.find_element_by_name("sBAuthentifizierungInpVO.stringPin")

    # send Username and Password
    obp_logger.debug("Inserting username into login box: %s " % username)
    inputElement_username.clear()
    inputElement_username.send_keys(username)

    obp_logger.debug("Inserting password into login box")
    inputElement_password.clear()
    inputElement_password.send_keys(password)

    # submit the Username and Password to GLS.
    obp_logger.info("submitting login_data to login")

    # Find login button, submit() function is not working, using click() instead.
    login_button = browser.find_element_by_class_name("gad-button-bg-left")
    login_button.click()
    assert "GLS Gemeinschaftsbank eG Online-Filiale" in browser.title

    # This opens the main page for accounts, and checks the name.
    # Call the Transaction Page
    #browser.refresh()
    time.sleep(0.5)
    obp_logger.debug("Open URL: %s" % gls_main_url_value_page)
    browser.find_element_by_partial_link_text(username).click()

    #browser.get(gls_main_url_value_page)
    assert "GLS Gemeinschaftsbank eG Online-Filiale" in browser.title

    gls_main_url_value_download = browser.find_element_by_link_text("Exportieren").get_attribute('href')

    obp_logger.debug("Open URL: %s" % gls_main_url_value_download)
    browser.get(gls_main_url_value_download)
    # Call the CSV Link.
    # Warning!
    # The Postbank uses a :page counter, and when the URL doesn't have the right page counter it will return
    # an error message.
    #browser.get(gls_main_url_value_download)

    obp_logger.info("closing Firefox")
    browser.close()
    # TODO:
    #       Need to return a file name.
    return csv_save_path


def main():
    obp_logger.info("Start main")
    check_for_clean_folder()
    get_csv_with_selenium(TMP)
    obp_logger.info("Done main")


if __name__ == '__main__':
    main()
