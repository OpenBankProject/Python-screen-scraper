# -*- coding: utf-8 -*-

import obp_config

import datetime
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


    def set_currency(self):
        pass


    def set_balance(self):
        pass


    def handle_transaction_type(self):
        pass


    def 


'''
u'obp_transaction_date_start': input_row[0]
u'obp_transaction_date_complete':input_row[1]
u'obp_transaction_transaction_type_de':input_row[2]
u'obp_transaction_comment1': input_row[3].rstrip()
u'obp_transaction_comment2': input_row[4].rstrip()
u'obp_transaction_data_blob': input_row[5]
u'obp_transaction_amount': amount.group()
u'obp_transaction_new_balance': new_balance.group()
'''
