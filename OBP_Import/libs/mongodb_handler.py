# -*- coding: utf-8 -*
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

