# -*- coding: utf-8 -*-
__author__ = ['simonredfern (simon@tesobe.com)',
             'Jan Alexander Slabiak (alex@tesobe.com)']

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

# tds is transaction_date_start
def get_field_tds(data, field_name):
    if field_name == 'obp_transaction_date_start':
        field_value = get_obp_transaction_date_start(data)

# tdc is get_obp_transactions_date_complete
def get_field_tdc(data, field_name):
    if field_name == 'get_obp_transactions_date_complete':
        field_value = get_obp_transactions_date_complete(data)
"""

import time
import urllib
import datetime

from sys import exit
from bson import son
from obp_config import *
from libs.import_helper import *
from libs.debugger import *
from libs.mongodb_handler import *
from socket import gethostname
from BeautifulSoup import BeautifulSoup, Comment




def get_obp_transaction_date_start(input_data):
    html_data = input_data[0].findAll('span')
    clean_data = html_data[0].find(text=True)
    data = clean_data
    return data


def get_obp_transactions_date_complete(input_data):
    clean_data = input_data[0].find(text=True)
    data = clean_data
    return data


def get_obp_transaction_type_de(input_data):
    html_data = input_data[0].findAll('span')
    clean_data = html_data[0].find(text=True)
    data = clean_data
    return data


# ToDo here we need better slicing
def get_obp_transaction_data_blob(input_data):
    html_data = input_data[0].findAll('span')
    #get the last data
    clean_data = html_data[len(html_data) - 1].find(text=True)
    # of the html_data
    #for n in range(len(html_data)):
    #    clean_data = []
    #    clean_data.append(html_data[n].find(text=True))
    data = clean_data
    return data


def get_obp_transaction_amount(input_data):
    html_data = input_data[0].findAll('span')
    # This will check for a existing -, if not it will return None
    if html_data[1].find(text=True) == None:
        clean_data = html_data[2].find(text=True)
    else:
            clean_data = html_data[1].find(text=True) + html_data[2].find(text=True)
    data = clean_data
    return data


def get_obp_transaction_new_balance(input_data):
    clean_data = input_data[0].find(text=True)
    data = clean_data
    return data

def read_html_file(file):
    file_open = open(file,'r')
    file_read = file_open.read()
    # Read from the object, storing the page's contents in 'file_read'.
    file_open.close
    return file_read


def do_scrape():
    print ('starting import')
    connection = connect_to_mongod(MONGODB_SERVER,MONGODB_SERVER_PORT)
    database = connect_to_mongod_db(connection,MONGODB_DATABASE)
    collection = mongodb_to_collection(database,MONGODB_COLLECTION)

    html = read_html_file(HTML_FILE_PATH)
    soup = BeautifulSoup(html)

    # Getting the <div>, where all transactions are stroed.
    # note: this id seems to change!
    # Will now using the orginal HTML file

    # Now getting all tranaction row out of the tbody.
    transaction_rows_even = soup.findAll(attrs={"class": "even state-expanded"})
    transaction_rows_odd = soup.findAll(attrs={"class": "odd state-expanded"})
    # There a two row class, have to merge them now tougther or we lost the
    # sorting. First Even the odd
    transaction_rows = transaction_rows_even + transaction_rows_odd


    # Loop trough all rows. Getting all the elements out of transaction row
    for i in range(len(transaction_rows)):
        header_data_start = transaction_rows[i].findAll(attrs={"class": "headers-date"})
        header_date_end = transaction_rows[i].findAll(attrs={"class": "headers-value-date"})
        header_type = transaction_rows[i].findAll(attrs={"class": "headers-type"})
        header_note = transaction_rows[i].findAll(attrs={"class": "headers-entry-note"})
        header_amount = transaction_rows[i].findAll(attrs={"class": "headers-amount"})
        header_balance = transaction_rows[i].findAll(attrs={"class": "headers-balance"})
        span_tags = transaction_rows[i].findAll('span')
        td_tag = transaction_rows[i].find('td')

        #print '%s\n%s' % (header_data_start, header_date_end)
        obp_transaction_row = {    'obp_transaction_date_start': get_obp_transaction_date_start(header_data_start)
                                ,'obp_transactions_date_complete': get_obp_transactions_date_complete(header_date_end)
                                ,'get_obp_transaction_type_de': get_obp_transaction_type_de(header_type)
                                ,'obp_transaction_data_blob':get_obp_transaction_data_blob(header_note)
                                ,'obp_transaction_amount':get_obp_transaction_amount(header_amount)
                                ,'obp_transaction_new_balance':get_obp_transaction_new_balance(header_balance)}

       # exit()
        # Print now all Elements from a single row, with no HTML-Tag
        for j in range(len(span_tags)):
            # This will just return text
            data_item = span_tags[j].findAll(text=True)
            if j == 0:
                print '\n%s' % data_item

            else:
                print data_item


        # Will tkae obp_transaction_row to convert it to a json
        posting = son.SON({
            'bank_account':get_bank_account(),
            'uploader_host':gethostname(),
            'insert_date':datetime.datetime.utcnow(),
            'obp_transaction': obp_transaction_row
            })

        print posting
        result = insert_into_mongodb(collection,posting)

"""
    We want to end up with the following data items
    Prefix with obp_ so we have consistent meaning

    obp_transaction_date_start = the date the transaction was started
    obp_transactions_date_complete = the date the transaction went live
    obp_transaction_type_en = the type of transaction in english
    obp_transaction_type_de = the type of transaction in german
    obp_transaction_data_blob = the big blob of unorganised data
    opb_from_account
    obp_to_account
    obp_transaction_currency
    obp_transaction_amount
    obp_transaction_new_balance


def main():
    do_scrape()

"""

if __name__ == '__main__':
    do_scrape()


