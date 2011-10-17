__author__ = ['simonredfern (simon@tesobe.com)'
             , 'Jan Alexander Slabiak (alex@tesobe.com)']

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


def get_obp_transaction_date_start(input_data):
    html_data = input_data[0].findAll('span')
    clean_data = html_data[0].find(text=True)
    #import pdb;pdb.set_trace()
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
    clean_data = html_data[len(html_data)-1].find(text=True) #get the last data
    # of the html_data
    #for n in range(len(html_data)):
    #    clean_data = []
    #    clean_data.append(html_data[n].find(text=True))
    data = clean_data
    return data

def get_obp_transaction_amount(input_data):
    html_data = input_data[0].findAll('span')
    clean_data = html_data[1].find(text=True) + html_data[2].find(text=True)
    data = clean_data
    return data

def get_obp_transaction_new_balance(input_data):
    clean_data = input_data[0].find(text=True)
    data = clean_data
    return data



def do_scrape():
    from BeautifulSoup import BeautifulSoup, Comment
    from pymongo import Connection
    from sys import exit
    import urllib

    #f = urllib.urlopen("http://Volumes/not_on_your_nelly/Bank_statements/Postbank-Online-Banking_100_days.html")



    print ('starting import')
    connection = Connection('obp_mongodb', 27017)
    # db = connection.obp_imports
    db = connection.OBP003
    collection = db.obptransactions


    #file = open('./Postbank-Online-Banking_100_days_minus_javascript_cut_down.html', 'r')
    #file = open('/Volumes/not_on_your_nelly/Bank_statements/Postbank-Online-Banking_100_days_minus_javascript_cut_down.html', 'r')

    file = open('/Volumes/not_on_your_nelly/Bank_statements/Postbank-Online-Banking_100_days_minus_javascript.html', 'r')


    # Read from the object, storing the page's contents in 's'.
    html = file.read()
    file.close()
    soup = BeautifulSoup(html)



    # Getting the <div>, where all transactions are stroed.
    # note: this id seems to change!
    transactions_div_id = "idc7c"
    tbody = soup.find("tbody", {"id": transactions_div_id})


    # Now getting all tranaction row out of the tbody.
    transaction_rows = tbody.findAll(attrs={"class": "even state-expanded"})






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
        obp_transaction_row = {'obp_transaction_date_start': get_obp_transaction_date_start(header_data_start)
                                ,'obp_transactions_date_complete': get_obp_transactions_date_complete(header_date_end)
                                ,'get_obp_transaction_type_de': get_obp_transaction_type_de(header_type)
                                ,'obp_transaction_data_blob':get_obp_transaction_data_blob(header_note)
                                ,'obp_transaction_amount':get_obp_transaction_amount(header_amount)
                                ,'obp_transaction_new_balance':get_obp_transaction_new_balance(header_balance)}

       # exit()
        # Print now all Elements from a single row, with no HTML-Tag
        for j in range(len(span_tags)):
            data_item = span_tags[j].findAll(text=True) # This will just return text
            if j == 0:
                print '\n%s' % data_item

            else:
                print data_item


        # Will tkae obp_transaction_row to convert it to a json

        collection = db.obptransactions.insert(obp_transaction_row)
        #print obp_transaction_row
    #    doc = { author : 'joe', created : new Date('03/28/2009'), ... }
    #    db.posts.insert(doc);


    # ToDO: Need to filter the span elements: not everything is a vaild information.



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
"""




if __name__ == '__main__':
    do_scrape()


