__author__ = [' Jan Alexander Slabiak (alex@tesobe.com)']
__license__ = """
  Copyright 2011 Music Pictures Ltd / TESOBE

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
from os import getcwd
import time


__doc__='''
Using Selenium RC2, install it with "pip install selenium"
need also =>selenium-2.0

This tool will take controll of a local firefox and downlaod the CSV File from PB

'''

fp = webdriver.FirefoxProfile()

# Direct = 0, Manual = 1, PAC = 2, AUTODETECT = 4, SYSTEM = 5
fp.set_preference("network.proxy.type", 0)
#fp.set_preference("browser.download.lastDir", getcwd())
fp.set_preference("browser.download.folderList",2)
fp.set_preference("browser.download.manager.showWhenStarting",False)
#fp.set_preference("browser.download.useDownloadDir",True)
#fp.set_preference("browser.download.defaultFolder",getcwd())
fp.set_preference("browser.download.dir",getcwd())
#fp.set_preference("browser.download.manager.useWindow",False)
#fp.set_preference("browser.download.manager.useWindow",False)
fp.set_preference("browser.helperApps.neverAsk.saveToDisk","text/csv")


browser = webdriver.Firefox(firefox_profile=fp) # Get local session of firefox
browser.get("https://banking.postbank.de/rai/login") # Load page
assert "Postbank Online-Banking" in browser.title
time.sleep(1)

# This will a simple login to the Demo APP of PostBank
# When we need to add some login infomation, we need to find the input fields.
# LINK: http://seleniumhq.org/docs/03_webdriver.html#getting-started-with-selenium-webdriver
# J.A.S

browser.get("https://banking.postbank.de/rai/login/wicket:interface/:0:login:demokontoLink::ILinkListener::")
browser.get("https://banking.postbank.de/rai/?wicket:bookmarkablePage=:de.postbank.ucp.application.rai.fs.UmsatzauskunftPage")
browser.get("https://banking.postbank.de/rai/?wicket:interface=:2:umsatzauskunftpanel:panel:umsatzanzeigeGiro:umsatzaktionen:csvHerunterladen::IResourceListener::&")
time.sleep(1)

# TODO: Adding some test and also check for the downloaded file.

browser.close()

