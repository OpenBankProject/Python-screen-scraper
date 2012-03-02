# -*- coding: utf-8 -*
__doc__ = """
This will provide funtions to insert data to MongoDB.
Using from MongoDB API pymongo.
LINK: http://api.mongodb.org/python/
"""
__author__ = ['Jan Alexander Slabiak (alex@tesobe.com)']
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


from pymongo import Connection
import bson.son


def connect_to_mongod(mongdod_host, mongod_host_port):
    """
    Need the IP/Host + Port of the MongoDB
    Create a connection to the MongoDB. Will retrun the connection obj.
    """

    mongod_connection = Connection(mongdod_host, mongod_host_port)
    return mongod_connection


def connect_to_mongod_db(connection, mongod_db):
    """
    Need a connection, need name of mongodb_db
    This will creat a connection to a Database
    return the connection obj with mongodb
    """

    mongodb = connection[mongod_db]
    return mongodb


def mongodb_to_collection(mongodb, mongo_collection):
    """
    Need a conned mongodb obj, and name of collection
    This will open/create a collection.
    Return the mongodb obj with collecition
    """

    mongodb_collection = mongodb[mongo_collection]
    return mongodb_collection


def insert_into_mongodb(collection, data_to_insert):
    """
    Need a collection obj and some stuff to insert.
    Will return the object_id of the insert data.
    """

    object_id = collection.insert(data_to_insert)
    return object_id
