__author__ = 'simonredfern',' Jan Alexander Slabiak'
__email__ = 'simon@tesobe.com','alex@tesobe.com'
__licens__ = 'APACHE '


from BeautifulSoup import BeautifulSoup, Comment


import urllib
import re
import pdb

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


# Now getting
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










