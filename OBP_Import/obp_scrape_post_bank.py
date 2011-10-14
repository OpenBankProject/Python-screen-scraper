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
import re
import pdb

#f = urllib.urlopen("http://Volumes/not_on_your_nelly/Bank_statements/Postbank-Online-Banking_100_days.html")

f = open('./Postbank-Online-Banking_100_days_minus_javascript_cut_down.html', 'r')

# Read from the object, storing the page's contents in 's'.
s = f.read()
f.close()


html = s

soup = BeautifulSoup(html)



# note: this id seems to change!
#
transactions_div_id = "idc7c"
tbody = soup.find("tbody", {"id": transactions_div_id})



transaction_rows = tbody.findAll(attrs={"class": "even state-expanded"})
#[comment.extract() for comment in comments]

#print  'info_elemnt: %s\n' % info_element
#for attr in info_elements
for i in range(len(transaction_rows)):
    span_tag = info_elements[i].findAll('span')
    td_tag = info_elements[i].find('td')

    for j in range(len(span_tag)):
        to_remove = span_tag[j].findAll(text=True)
        if j == 0:
            print '%s\n' % to_remove
        else:
            print to_remove










