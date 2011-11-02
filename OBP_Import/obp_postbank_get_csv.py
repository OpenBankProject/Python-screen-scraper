from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from os import getcwd
import time



'''
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

browser.get("https://banking.postbank.de/rai/login/wicket:interface/:0:login:demokontoLink::ILinkListener::")
browser.get("https://banking.postbank.de/rai/?wicket:bookmarkablePage=:de.postbank.ucp.application.rai.fs.UmsatzauskunftPage")
browser.get("https://banking.postbank.de/rai/?wicket:interface=:2:umsatzauskunftpanel:panel:umsatzanzeigeGiro:umsatzaktionen:csvHerunterladen::IResourceListener::&")
time.sleep(1)
browser.close()

