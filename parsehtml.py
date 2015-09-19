import sys
import re
from bs4 import BeautifulSoup

# get each row in table of contacts
def has_name(tag):
    if tag.has_attr('valign'):
        if tag.td is not None:
            if tag.td.a is not None:
                return tag.td.a.has_attr('name')
    return False



if len(sys.argv) < 2:
    print 'not enough arguments'
    exit(1)

file_name = sys.argv[1]
#file_name = './html/min/mcys.html'

html_doc = open(file_name, 'r')

soup = BeautifulSoup(html_doc.read(), 'html.parser')
# print(soup.prettify())

# //TODO get child links

#print soup.find_all('table')
#print soup.body.table.tr.td.next_sibling.table.tr.next_sibling.td.table.tr.td.font.table.tr.td.table.next_sibling.tr.contents

print len(soup.find_all(has_name))
for link in soup.find_all(has_name):
    print link
    print '\n========\n\n'

html_doc.close()

