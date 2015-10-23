# -*- coding: utf-8 -*
__doc__ = """
This will provide funtions to insert data to MongoDB.
Using from MongoDB API pymongo.
LINK: http://api.mongodb.org/python/
"""
__author__ = ['Jan Alexander Slabiak (alex@tesobe.com)']
__license__ = """
    Copyright (C) 2011-2015, TESOBE / Music Pictures Ltd

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Email: contact@tesobe.com
    TESOBE / Music Pictures Ltd
    Osloerstrasse 16/17
    Berlin 13359, Germany
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
