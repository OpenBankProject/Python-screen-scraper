__author__ = 'simonredfern'

from BeautifulSoup import BeautifulSoup, Comment


import urllib
import re
import pdb

#f = urllib.urlopen("http://Volumes/not_on_your_nelly/Bank_statements/Postbank-Online-Banking_100_days.html")

f = open('/home/akendo/Work/Tesobe/Pro/Projects/try_out/OBP_Import/Postbank-Online-Banking_100_days_minus_javascript_cut_down.html', 'r')

# Read from the object, storing the page's contents in 's'.
s = f.read()
f.close()


html = s

soup = BeautifulSoup(html)


#print soup.prettify()


#print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

#balance = soup.find("span", { "class" : "balance-amount" })

#print 'balance is %s' % balance.contents[0]

"""

entry = soup.find("td", { "class" : "headers-entry-note" })

print 'entry is %s' % entry

print 'entry.next is %s' % entry.next


print 'entry.parent is %s' % entry.parent


entries = soup.findAll("td", { "class" : "headers-entry-note" })

print 'entries is %s' % entries

for e in entries:
    print e
    print "\n"

"""

# Grab the <table id="mini_player"> element
#scores = soup.find('table', {'id':'mini_player'})

# Get a list of all the <tr>s in the table, skip the header row
#rows = scores.findAll('tr')
# note: this id seems to change!

my_id = "idc7c"
tbody = soup.find("tbody", {"id": my_id})
#print 'tbody is %s' % tbody

#links = soup.findAll()

#print 'yyyyyyyyyyyyyyyyyyyyyyyyyyy'

#rows = tbody.findAll('a')[0:]
#print rows


comments = tbody.findAll('a')[0:]
[comment.extract() for comment in comments]

# 1
# <a>2<b>3</b></a>
#print tbody
#for numbers_in_tbody in range

info_elements = tbody.findAll(attrs={"class": "even state-expanded"})
#[comment.extract() for comment in comments]

#print  'info_elemnt: %s\n' % info_element
#for attr in info_elements
for numbers_of_info_elements in range(len(info_elements)):
    info_tag = info_elements[numbers_of_info_elements].findAll('span')
    table_tag = info_elements[numbers_of_info_elements].find('td')

    for numbers in range(len(info_tag)):
        to_remove = info_tag[numbers].findAll(text=True)
        if numbers == 0:
            print '%s\n' % to_remove
        else:
            print to_remove


#print 'info tag:%s\ntable_tag: %s\n' % (info_tag, table_tag)

#table_tag_text = table_tag.findAll(text=True)
#print table_tag_text









