#!/usr/bin/env python
# -*- coding: utf-8 -*
__doc__ = """
Basic tests of all functionality. It will test for the
right configuration and options, the DB backend and the API.
"""
__author__ = ['simonredfern (simon@tesobe.com)', ' Jan Alexander Slabiak (alex@tesobe.com)']
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
#import csv
#import bson
import unittest
#import obp_config
#import libs.to_utf8
#import libs.transactions
#import libs.postbank_get_csv
import SimpleHTTPServer
import SocketServer
import threading
#import errno


#from bson import son
#from pymongo import Connection
#from socket import gethostbyname
#from libs.debugger import debug
from threading import *
from simplejson import dumps
from obp_config import TMP
from libs.to_utf8 import main as utf8_main
from libs.scala_api_handler import *
from shutil import copy
from libs.import_helper import *


# This will start checking Database
# Drop, Create, Insert, Tables Style ,Drop
# Using the testcase assertisNot instead of assertEqual,
# http://docs.python.org/library/unittest.html#deprecated-aliases


class ThreadClass(threading.Thread):
    """
        Will start a single thread of the SimpleHTTPServer.
        TODO:
        Using the BaseHTTPServer, the SimpleHTTPServer can't handle POST/PUT
        request.
        http://docs.python.org/library/basehttpserver.html#module-BaseHTTPServer
    """
    def run(self):
        Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        httpd = SocketServer.TCPServer(("", 8888), Handler)
        #httpd.handle_request()
        httpd.serve_forever()


class TestBasicScalaAPI(unittest.TestCase):
    """
    This will check for basic function of the Scala API.
    It's only check that the function will send some date.
    """

    # def setUp(self):
    #     Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    #     httpd = SocketServer.TCPServer(("", 8888), Handler)
    #     httpd.server_()

    def test_basic_insert(self):
        """
        Try to insert data to the localhost
        """
        result = insert_into_scala("localhost", "8888", "Nothing")
        # Accept a 501 status_code for now. SimpleHTTPServer can't handle
        # POST/PUT requests.
        self.assertEqual(result.status_code, 501)

    def test_basic_connection(self):
        """
        Setup a basic HTTP Server and try to get the root via re3quest
        module.
        """
        result = check_API_HOST_reachable("localhost", "8888")
        self.assertEqual(result.status_code, 200)

    @classmethod
    def tearDownClass(cls):
        for thread in enumerate():
            if thread.isAlive():
                try:
                    thread._Thread__stop()
                except:
                    print str(thread.getName()) + ' could not be terminated'


class TestImportHelper(unittest.TestCase):

    def setUp(self):
        # Need an extra Folder for the tests.
        self.test_folder = "/tmp/OBP_TEST_FOLDER"
        if not os.path.exists(self.test_folder):
            os.makedirs(self.test_folder)

    def test_check_for_existing_csv(self):

        self.path_to_no_csv = "false"
        with self.assertRaises(IOError):
            check_for_existing_csv(self.path_to_no_csv)

    def test_check_for_clean_folder(self):

        check_for_clean_folder(self.test_folder)
        self.assertEqual(0, len(os.listdir(self.test_folder)))

        # Create a file that should be removed.
        copy("/bin/false", self.test_folder)
        self.assertEqual(1, len(os.listdir(self.test_folder)))
        check_for_clean_folder(self.test_folder)
        self.assertEqual(0, len(os.listdir(self.test_folder)))

    def test_json_formatter(self):

        self.result = json_formatter(dumps([{}], sort_keys=False))
        self.assertEqual(" {} ", self.result)

    def test_remove_empty_lines(self):
        self.test_file_name = os.path.join(self.test_folder, "test_example_utf8_headers.csv")
        copy("usr/tests/test_example_utf8_headers.csv", self.test_file_name)
        self.assertTrue(os.path.exists(self.test_file_name))

        check_for_existing_csv(self.test_file_name)

        remove_empty_lines(self.test_file_name)


if __name__ == '__main__':
    local_simple_http_server = ThreadClass()
    local_simple_http_server.deamon = False
    local_simple_http_server.start()
    unittest.main()
    #local_simple_http_server.stop()
