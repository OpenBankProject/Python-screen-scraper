#!/usr/bin/env python
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


from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from sys import exit
from libs.debugger import debug
import os
import time

from obp_config import TMP

TMP_SUFFIX ='csv'

__doc__='''
Using Selenium RC2, install it with "pip install selenium"
need also =>selenium-2.0

This tool will take controll of a local firefox and downlaod the CSV File from PB

TMP is in the obp_config, this is importen. No every System have a /tmp (Also related
to win32 systems) 

'''
# TODO: Adding some test and also check for the downloaded file.

if not os.path.exists(TMP):
    os.makedirs(TMP)

csv_save_path = os.path.join(TMP,TMP_SUFFIX)

if not os.path.exists(csv_save_path):
    os.makedirs(csv_save_path)



# This will a simple login to the Demo APP of PostBank
# When we need to add some login infomation, we need to find the input fields.
# LINK: http://seleniumhq.org/docs/03_webdriver.html#getting-started-with-selenium-webdriver
# J.A.S

# Setting up a Profile for Firefox.
# There a the Proxy disabled (to make sure) and the 
# that he is just download files with asking.
fp = webdriver.FirefoxProfile()
fp.set_preference("network.proxy.type", 0)
fp.set_preference("browser.download.folderList",2)
fp.set_preference("browser.download.manager.showWhenStarting",False)
fp.set_preference("browser.download.dir",csv_save_path)
# Need to set CSV to saveToDisk, else it's unknown for FF and he will ask.
fp.set_preference("browser.helperApps.neverAsk.saveToDisk","text/csv")


browser = webdriver.Firefox(firefox_profile=fp) # Get local session of firefox
#browser = webdriver.Chrome('/usr/bin/chromium') # Get local session of chrome
browser.get("https://banking.postbank.de/rai/login") # Load page
assert "Postbank Online-Banking" in browser.title

browser.get("https://banking.postbank.de/rai/login/wicket:interface/:0:login:demokontoLink::ILinkListener::")
assert "Postbank Online-Banking" in browser.title
time.sleep(2)


browser.get("https://banking.postbank.de/rai/?wicket:bookmarkablePage=:de.postbank.ucp.application.rai.fs.UmsatzauskunftPage")
time.sleep(2)
error_message = browser.find_element_by_class_name("important")
#debug()
if error_message.is_displayed == True:
    browser.get("https://banking.postbank.de/rai/login/wicket:interface/:0:login:demokontoLink::ILinkListener::")
    time.sleep(2)
    assert "Postbank Online-Banking" in browser.title
    browser.get("https://banking.postbank.de/rai/login") # Load page
    browser.get("https://banking.postbank.de/rai/login/wicket:interface/:0:login:demokontoLink::ILinkListener::")
    browser.get("https://banking.postbank.de/rai/?wicket:bookmarkablePage=:de.postbank.ucp.application.rai.fs.UmsatzauskunftPage")
    time.sleep(2)



browser.get("https://banking.postbank.de/rai/?wicket:interface=:2:umsatzauskunftpanel:panel:umsatzanzeigeGiro:umsatzaktionen:csvHerunterladen::IResourceListener::&")
time.sleep(2)
browser.close()

csv_files = os.listdir(csv_save_path)
file_count = len(csv_files) 

if file_count == 0:
    print "We didn't got the CSV file."
    exit(1)
elif file_count != 1:
    print "We did got to much files..."
    exit (10)



print csv_files[0]
# Here have the file given to the obp_importer
