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
import pdb

# This will start checking Database
# Drop, Create, Insert, Tables Style ,Drop
# Using on the testcase assertisNot instead of assertEqual,
# http://docs.python.org/library/unittest.html#deprecated-aliases


def debug():
    pdb.set_trace()



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

    def test_mongodb_database_collections(self):
        self.connection = Connection('obp_mongod', 27017)
        # This line below, ensure that we don't have dupiclaed db
        self.connection.drop_database('imports_testdb') 
        self.mongo_db = self.connection.imports_testdb
        result = self.mongo_db.collection_names()
        # Nothing for insert, so nothing is created, should return a 0 in len
        self.assertEqual(len(result), 0)
        
        should_result = [u'imports_testdb', u'system.indexes']
        self.mongo_db.imports_testdb.insert({'test':123})
        result = self.mongo_db.collection_names()
        self.assertEqual(result, should_result)
        self.connection.drop_database('imports_testdb')

        # Check for no collection in imports_testdb
        self.mongo_db = self.connection.imports_testdb
        result = self.mongo_db.collection_names()
        # Should return a 0 in len
        self.assertEqual(len(result), 0)


class TestImporting(unittest.TestCase):

      def setUp(self):
          self.connection = Connection('obp_mongod', 27017)
          self.mongo_db = self.connection.imports_testdb


      def test_basic_import(self):
          self.import_data ={u'Bank Account':u'1234561231'
                              ,u'Bank Info': [u'Jesus',u'Christ']
                              ,u'Bank Numer ':u'123'
                             } 
          result = self.mongo_db.imports_testdb.insert(self.import_data)
          test_db_collection = self.mongo_db.imports_testdb
          result = test_db_collection.find_one(result)
          self.assertEqual(result,self.import_data)


      def test_baisc_date_type(self):
          pass
          

        


#class TestImportedData(self):




         

if __name__ == '__main__':
    unittest.main()
