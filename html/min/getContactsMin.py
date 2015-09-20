import sys
import re
import time
from urllib2 import Request, urlopen
from urllib2 import HTTPError
from bs4 import BeautifulSoup

def main():
    if len(sys.argv) < 2:
        print 'not enough arguments'
        exit(1)

    base_url = 'http://eresources.nlb.gov.sg/webarchives/wayback/20070223201456/http://app.sgdi.gov.sg/'
    file_name = sys.argv[1]
    #file_name = './html/min/mcys.html'
    org = file_name.replace('.html', '')
    div = ''
    subdiv = ''
    subsubdiv = ''

    html_doc = open(file_name, 'r')

    soup = BeautifulSoup(html_doc.read(), 'html.parser')
    # print(soup.prettify())


    # Extract cell contents
    cells = []
    for link in soup.find_all(has_name):
        cells.append(link.get_text().strip())
        # print link.get_text().strip()
        # print '\n========\n\n'


    # Printing
    print 'Organization\tDivision\tSubdivision\tSubsubdivision\tPost\tFull Name'
    for cell in cells:
        fields = cell.split('\n')
        # no name
        if(fields[2].strip() != '-'):
            print org+'\t'+div+'\t'+subdiv+'\t'+subsubdiv+'\t'+ fields[0].strip() + '\t' + fields[2].strip()
        

    # Subdivs
    
    # get depts/divisions links
    for link in soup.find_all('a'):
        if(link.get('href') is not None):
            url = link.get('href')
            if(url.find('listing.asp?agency_subtype=dept') is not -1):
                if((url.find('http') is -1) and (url.find('#dept_anchor') is -1)):
                    div = link.string


                    #get html docs
                    req_norm = Request(base_url+url)
                    req_expand = Request(base_url+url.replace('listing', 'listing_expand'))

                    try:
                        response_norm = urlopen(req_norm)
                    #normal is missing
                    except HTTPError as e:
                        if e.code == 417 or e.code == 404:
                            response = None
                        
                    #normal is okay
                    else:
                        try:
                            response_expand = urlopen(req_expand)
                        #expand is missing
                        except HTTPError as e:
                            if e.code == 417 or e.code == 404:
                                response = response_norm
                        else:
                            response = response_expand


                    
                    #missing
                    if response is None:
                        print org+'\t'+div+'\t'+subdiv+'\t'+subsubdiv+'\t'+ 'MISSING' + '\t' + 'MISSING'

                    #normal
                    else:
                        soup = BeautifulSoup(response.read(), 'html.parser')

                        # Extract cell contents
                        is_first = True
                        for link in soup.find_all(has_subdivname):

                            #find subdiv
                            for font in link.find_all('font'):
                                if font.has_attr('size'):
                                    if font['size'] == '3':
                                        if is_first:
                                            div = font.string
                                            is_first = False
                                        else:
                                            subdiv = font.string
                                        break

                            #find position and name
                            for tag in link.find_all('tr'):
                                if tag.has_attr('valign'):
                                    if tag.td is not None:
                                        if tag.td.a is not None:
                                            if tag.td.a.has_attr('name'):
                                                pos = tag.td.a.string.strip()
                                                name = tag.td.next_sibling.next_sibling.font.get_text().strip()

                                                #no name
                                                if name != '-':
                                                    print org+'\t'+div+'\t'+subdiv+'\t'+subsubdiv+'\t'+ pos + '\t' + name



        # delay 0.1 sec
        time.sleep(0.1)


    html_doc.close()






# get each row in table of contacts
def has_name(tag):
    if tag.has_attr('valign'):
        if tag.td is not None:
            if tag.td.a is not None:
                return tag.td.a.has_attr('name')
    return False

# get each table containing subdiv name and contacts
def has_subdivname(tag):
    if tag.name == 'table':
        if tag.has_attr('width'):
            if tag['width'] == '600':
                for font in tag.find_all('font'):
                    if font.has_attr('size'):
                        if font['size'] == '3':
                            return True
    return False



if __name__ == '__main__':
    main()
