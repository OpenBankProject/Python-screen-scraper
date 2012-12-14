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
from obp_config import TMP, TMP_CSV_SUFFIX
from libs.to_utf8 import main as utf8_main
from libs.scala_api_handler import *
from shutil import copy
from libs.import_helper import *
from libs.csv_importer import *
from libs.gls_get_csv import *
from random import randrange
from codecs import open as codeces_open

import libs.csv_importer
# This will start checking Database
# Drop, Create, Insert, Tables Style ,Drop
# Using the testcase assertisNot instead of assertEqual,
# http://docs.python.org/library/unittest.html#deprecated-aliases

TEST_FOLDER = "/tmp/OBP_TEST_FOLDER"


class ThreadClass(threading.Thread):
    """
        Will start a single thread of the SimpleHTTPServer.
        TODO:
        Using the BaseHTTPServer, the SimpleHTTPServer can't handle POST/PUT
        request.
        http://docs.python.org/library/basehttpserver.html#module-BaseHTTPServer

        There is still a problem with an open connection, after a successfull run.

    """
    def __init__(self, input_port):
        threading.Thread.__init__(self)
        self._input_port = input_port

    def run(self):
        Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        httpd = SocketServer.TCPServer(("", self._input_port), Handler)
        #httpd.handle_request()
        httpd.serve_forever()


class TestGetGLSCSV(unittest.TestCase):
    """
        This is a basic function test. To ensure the function of the GLS Bank Importer.
    """

    def setUp(self):
        self.test_folder = TEST_FOLDER
        if not os.path.exists(self.test_folder):
            os.makedirs(self.test_folder)

    def test_gls_get_csv_with_selenium(self):
        """
            This should return a Path to a vaild CSV File.
        """
        self.gls_main_url_login_page = "https://internetbanking.gad.de/ptlweb/WebPortal?bankid=4967&modus=demo"
        self.user = "6666700"
        self.password = "13579"
        self.result = gls_get_csv_with_selenium(self.gls_main_url_login_page, self.test_folder, self.user, self.password)
        self.assertEqual(os.path.join(self.test_folder, TMP_CSV_SUFFIX), self.result)

        self.path_to_csv = self.result
        self.result = os.listdir(self.path_to_csv)
        self.assertTrue(self.result[0].endswith('csv'))
        # Now getting the file name and check for a .csv ending.

    @classmethod
    def tearDownClass(cls):
            # For now we remove this file. Need this for late to genareate the JSON.
            dir_to_remove = os.path.join(TEST_FOLDER, TMP_CSV_SUFFIX)
            file_to_remove = os.listdir(dir_to_remove)
            os.remove(os.path.join(dir_to_remove, file_to_remove[0]))
            os.removedirs(dir_to_remove)


class TestCSVImporterGLS(unittest.TestCase):

    def setUp(self):
        if not os.path.exists(TEST_FOLDER):
            os.makedirs(TEST_FOLDER)

        self.test_file_name = os.path.join(TEST_FOLDER, "test_example_latin2.csv")
        copy("usr/tests/test_example_latin2.csv", self.test_file_name)
        self.file_to_csv = os.listdir(TEST_FOLDER)
        debug()
        self.converted_file = libs.to_utf8.main(self.test_file_name, TEST_FOLDER)
        self.assertEqual(os.path.join(TEST_FOLDER, self.file_to_csv[0]), self.converted_file)

    def test_parse_row_of_csv(self):
        #get_posted_date(BANK)
        result = parse_row_of_csv(self.converted_file)
        print result

    @classmethod
    def tearDownClass(cls):
            # For now we remove this file. Need this for late to genareate the JSON.
            file_to_remove = os.listdir(TEST_FOLDER)
            os.remove(os.path.join(TEST_FOLDER, file_to_remove[0]))
            os.removedirs(TEST_FOLDER)


class TestFilesToUTF8(unittest.TestCase):

    def setUp(self):
        if not os.path.exists(TEST_FOLDER):
            os.makedirs(TEST_FOLDER)

        self.test_file_name = os.path.join(TEST_FOLDER, "test_example_latin2.csv")
        copy("usr/tests/test_example_latin2.csv", self.test_file_name)
        self.file_to_csv = os.listdir(TEST_FOLDER)

    def test_to_utf8(self):
        csv_lines = 7

        self.converted_file = libs.to_utf8.main(self.test_file_name, TEST_FOLDER)
        self.assertEqual(os.path.join('/tmp/OBP_TEST_FOLDER/test_example_latin2_utf8.csv'), self.converted_file)

        debug()
        os.chdir(os.path.split(self.converted_file)[0])
        line_number = 0
        for line in codeces_open(os.path.split(self.converted_file)[1], 'rU', "utf-8"):
            line_number += 1
        else:
            self.assertEqual(csv_lines, line_number)

    @classmethod
    def tearDownClass(cls):
            # For now we remove this file. Need this for late to genareate the JSON.
            file_to_remove = os.listdir(TEST_FOLDER)
            os.remove(os.path.join(TEST_FOLDER, file_to_remove[0]))
            os.removedirs(TEST_FOLDER)


class TestBasicScalaAPI(unittest.TestCase):
    """
    This will check for basic function of the Scala API.
    It's only check that the function will send some date.
    """

    def setUp(self):
        self.random_api_port = str(randrange(60000, 65000))
        self.local_simple_http_server = ThreadClass(int(self.random_api_port))
        self.local_simple_http_server.deamon = False
        self.local_simple_http_server.start()

    def test_basic_insert(self):
        """
        Try to insert data to the localhost
        """
        result = insert_into_scala("localhost", self.random_api_port, "Nothing")
        # Accept a 501 status_code for now. SimpleHTTPServer can't handle
        # POST/PUT requests.
        self.assertEqual(result.status_code, 501)

    def test_basic_connection(self):
        """
        Setup a basic HTTP Server and try to get the root via request
        module.
        """
        result = check_API_HOST_reachable("localhost", self.random_api_port)
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
    unittest.main()
