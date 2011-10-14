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

from BeautifulSoup import BeautifulSoup, Comment


import urllib

#f = urllib.urlopen("http://Volumes/not_on_your_nelly/Bank_statements/Postbank-Online-Banking_100_days.html")


file = open('./Postbank-Online-Banking_100_days_minus_javascript_cut_down.html', 'r')

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
    span_tags = transaction_rows[i].findAll('span')
    td_tag = transaction_rows[i].find('td')

    # Print now all Elements from a single row, with no HTML-Tag
    for j in range(len(span_tags)):
        data_items = span_tags[j].findAll(text=True) # This will just return text
        if j == 0:
            print '%s\n' % data_items
        else:
            print data_items


# ToDO: Need to filter the span elements: not everything is a vaild information.










