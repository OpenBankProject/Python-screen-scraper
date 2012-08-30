#!/bin/env python
# -*- coding: utf-8 -*-

"""Test GLS.de website using Selenium.

First Selenium Remote Control must be started like this:

    java -jar selenium-server-standalone-2.24.1.jar

Run this to see a list of options:

    java -jar selenium-server-standalone-2.24.1.jar -h

See also:

    http://www.bitmotif.com/selenium/selenium-remote-control-for-java-a-tutorial/
"""


import sys
import time
import getpass
import random
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException, 
    ElementNotVisibleException)


__author__ = "Dinu Gherman"
__date__ = "2012-07-19"
__copyright__ = "Apache2"


# change as needed...
KN = "6666700"
PIN = "13579"
ACC = "123456789"


# create Firefox profile, unclear how useful this really is
fp = webdriver.FirefoxProfile()
fp.set_preference("network.proxy.type", 0)
fp.set_preference("browser.download.folderList", 2)
fp.set_preference("browser.download.manager.showWhenStarting", False)
fp.set_preference("browser.download.dir", "/Users/dinu/Downloads")
# Need to set CSV to saveToDisk, else it's unknown to FF and it will ask for it
# (doesn't seem to work)
#fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-unknown-content-type")
fp.set_preference("webdriver.firefox.bin", "...")  # ?


class TestGLS(unittest.TestCase):
    """Test accessing some pieces of an online GLS account.

    Run only one of the tests, like this:
        python test_gls_tesobe.py TestGLS.test1
        python test_gls_tesobe.py TestGLS.test2
    not both, like this:
        python test_gls_tesobe.py TestGLS
    which will raise an WebDriverException (#TODO).
    """

    def setUp(self):
        # goto login page
        url = "https://internetbanking.gad.de/ptlweb/WebPortal?bankid=4967&modus=demo"
        self.login_page = url
        self.browser = browser = webdriver.Firefox(firefox_profile=fp)
        # move Firefox window as far away as possible (a corner still visible)
        self.browser.set_window_position(10000, 10000)
        browser.get(self.login_page)
        self.assert_("GLS Gemeinschaftsbank eG" in browser.title)

    def _login(self, kn, pin):
        "Log into the website."

        browser = self.browser
        browser.find_element_by_id("kontonummer").send_keys(kn)
        browser.find_element_by_id("pin").send_keys(pin)
        browser.find_element_by_id("button_login").click()
        time.sleep(0.5)
        # now we are on the overview page (Finanzübersicht)

    def test1(self):
        "Print overview statement."

        self._login(KN, PIN)

        self.browser.find_element_by_link_text("Finanzübersicht").click()

        # this will raise sometimes, for totally mysterious reasons:
        # NoSuchElementException: Message: u'Unable to locate element:
        #   {"method":"class name","selector":"gad-overview-group"}'
        #import pdb; pdb.set_trace()
        elem = self.browser.find_element_by_class_name("gad-overview-group")

        lines = elem.text.split("\n")
        i = 1
        while len(lines[i:i + 3]) >= 3:
            print ", ".join(lines[i:i + 3])
            i += 3

    def test2(self):
        "Download CSV files for all transactions."

        browser = self.browser

        self._login(KN, PIN)

        # goto transactions page (Umsätze)
        elem = browser.find_element_by_link_text("Umsätze & Kontoauszüge")
        elem.cli

        # select desired account number
        select_elem = browser.find_element_by_name("idKontoGewaehlt")
        path = "option[text()[contains(.,'%s')]]" % ACC
        option = select_elem.find_element_by_xpath(path)
        option.click()

        # export data as CSV, one file per page, and jump to next page...
        while True:
            elem = browser.find_element_by_link_text("Exportieren")
            elem.click()
            try:
                name = "gad-pagination-link-next"
                elem = browser.find_element_by_class_name(name)
                elem.click()
            except ElementNotVisibleException:
                break

    def tearDown(self):
        self.browser.close()


if __name__ == "__main__":
    unittest.main()
