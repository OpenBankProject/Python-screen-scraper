# -*- coding: utf-8 -*
__doc__ = '''
This is the mongodb_handler
'''
from pymongo import Connection

def insert_into_mongodb(data_to_insert):
    collection = db.obptransactions.insert(data_to_insert)
    return collection


