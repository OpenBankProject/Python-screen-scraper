# -*- coding: utf-8 -*-
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
___doc___"""
TODO: Using this Object!
I'm no developer and have no much use to Python Object. This here is a approve of
adapting a object to this Project. It hasn't use jet. Becourse we use a simple concept,
what have to work first. 
"""

import obp_config

import datetime
import re
from libs.debugger import debug
from socket import gethostname

class obp_account:
    OBP_version = obp_config.OBP_VERSION
    OBP_loader_host = gethostname()
    insert_date = datetime.datetime.utcnow()




class obp_transaction:
    start_date = ''
    complete_date = ''
    transaction_type = ''
    comment_1 = ''
    comment_2 = ''
    data_blob = ''
    amount = ''
    new_balance = ''
    this_account  = ''
    source_bank = ''
    transaction_currency  = ''


    def check_date_format(self,date_to_check):
        # This will change, currently is the default import date in german 
        # time format of DD.MM.YYYY
        try:
            valid_date = datetime.datetime.strptime( date_to_check, "%d.%m.%Y" )
            return True
        except ValueError:
              print('Invalid date!')
              return False


    def convert_date_to_clean_date(self,date_to_convert):
        # This function will convert a Date to a UTC time. 
        # It will take an input and return it as a UTC.
        assert self.check_date_format(date_to_convert) is True

        # The date only showing the detail of the day. Setting Sec,Min to 0
        self.zero_time = datetime.time(0,0,0)
        # We now where here the date is: 

        self.to_convert = datetime.date(
                int(date_to_convert[6:10]),
                int(date_to_convert[3:5]),
                int(date_to_convert[0:2]))
        datetime.datetime.combine(self.to_convert,self.zero_time)
        result = datetime.datetime.strftime(self.to_convert, "%Y,%m,%d,%H,%M,%S")

        print result
        print type(result)


    def get_currency(self,currency_input):
        # Take a INPUT and search for currentcy like € or $ and
        # return string return lile EUR,DOL YEN
        
        #Define Search String for EUR
        search_euro = re.match("€|\xe2\x82\xac|\u20ac",currency_input)
        #if 


    def set_currency(self):

        pass


    def set_balance(self):
        pass


    def handle_transaction_type(self):
        pass


    def account_info(self):
        pass
