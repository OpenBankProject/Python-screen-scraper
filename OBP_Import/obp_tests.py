#!/usr/bin/env python
# -*- coding: utf-8 -*
__author__ = ['simonredfern (simon@tesobe.com)',' Jan Alexander Slabiak (alex@tesobe.com)']
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


from pymongo import Connection 
from socket import gethostbyname
import unittest
import json
import os 

# This will start checking Database
# Drop, Create, Insert, Tables Style ,Drop
# Using on the testcase assertisNot instead of assertEqual,
# http://docs.python.org/library/unittest.html#deprecated-aliases


class TestMongoDB(unittest.TestCase):

    def setUp(self):
        pass
        # TODO: It would be better to have a configuration file.
        # That would be loaded at this place. J.A.S


    def test_host_entry(self):
        result = gethostbyname("obp_mongod") 
        #check for host entry 
        self.assertIsNot(result,None)

    def test_mongodb_connection(self):
        result = Connection('obp_mongod', 27017)
        self.assertIsNot(result,None)
        result.disconnect()

    # Skiping the Database test, MongoDB creating automatlic a Datbase
    # so that every test for a database will pass
    #def test_mongodb_database_collections 
    #    self.connection = Connection('obp_mongod', 27017)
    #    self.mongodb = self.obp_imports_testdb
    #    result = self.mongodb.collection_names()


        


         

if __name__ == '__main__':
    unittest.main()
