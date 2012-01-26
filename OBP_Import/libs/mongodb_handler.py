# -*- coding: utf-8 -*
__author__ = ['Jan Alexander Slabiak (alex@tesobe.com)']
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
__doc__ = '''
This is the mongodb_handler
'''
from pymongo import Connection
import bson.son


def connect_to_mongod(mongdod_host,mongod_host_port):
    mongod_connection = Connection(mongdod_host,mongod_host_port)
    return mongod_connection


def connect_to_mongod_db(connection,mongod_db):
    mongodb = connection[mongod_db]
    return mongodb


def mongodb_to_collection(mongodb,mongo_collection):
    mongodb_collection = mongodb[mongo_collection]
    return mongodb_collection


def insert_into_mongodb(collection,data_to_insert):
    object_id = collection.insert(data_to_insert)
    return object_id


def pre_insert_data(data_to_prepere):
    #This function will convert the data to son.
    pass


def check_index():
    pass


def make_uniq_index():
    pass
