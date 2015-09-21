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
        

    # Divisions
    
    # get division links
    for link in soup.find_all('a'):
        if(link.get('href') is not None):
            url = link.get('href')
            if(url.find('listing.asp?agency_subtype=dept') is not -1):
                if((url.find('http') is -1) and (url.find('#dept_anchor') is -1)):
                    div = link.string

                    try:
                        req_norm = Request(base_url+url)
                        response = urlopen(req_norm)
                        #response_norm = urlopen(req_norm)
                    #normal is missing
                    except HTTPError as e:
                        if e.code == 417 or e.code == 404:
                            response = None

                    
                    #missing
                    if response is None:
                        print org+'\t'+div+'\t'+subdiv+'\t'+subsubdiv+'\t'+ 'MISSING' + '\t' + 'MISSING'

                    #normal
                    else:
                        soup = BeautifulSoup(response.read(), 'html.parser')

                        # Extract cell contents
                        is_first = True
                        for link in soup.find_all(has_subdivname):

                            #find div name
                            # for font in link.find_all('font'):
                            #     if font.has_attr('size'):
                            #         if font['size'] == '3':
                            #             if is_first:
                            #                 div = font.string
                            #                 is_first = False
                            #             else:
                            #                 subdiv = font.string
                            #             break

                            #//TODO: missed out subsub(sub)div check header above subdiv for its parent div
                            #ref: MOF ECONOMIC PROGRAMMES DIRECTORATE
                            #find position and name
                            for tag in link.find_all('tr'):
                                if tag.has_attr('valign'):
                                    if tag.td is not None:
                                        if tag.td.a is not None:
                                            if tag.td.a.has_attr('name') and tag.td.a.string is not None:
                                                pos = tag.td.a.string.strip()
                                                names = tag.td.next_sibling.next_sibling.font.get_text().strip().split('\n')

                                                #no name
                                                if names[0] != '-':
                                                    #why is their address part of their name
                                                    name = names[0]
                                                    print '\t'.join([org,div,subdiv,subsubdiv,pos,name])



                        # Subdivs
                        
                        # get subdiv links
                        for link in soup.find_all('a'):
                            if(link.get('href') is not None):
                                url = link.get('href')
                                if(url.find('listing.asp?agency_subtype=dept') is not -1):
                                    if((url.find('http') is -1) and (url.find('#dept_anchor') is -1)):
                                        subdiv = link.string

                                        try:
                                            req_norm = Request(base_url+url)
                                            response = urlopen(req_norm)
                                            #response_norm = urlopen(req_norm)
                                        #normal is missing
                                        except HTTPError as e:
                                            if e.code == 417 or e.code == 404:
                                                response = None
                                        
                                        #missing
                                        if response is None:
                                            print '\t'.join([org,div,subdiv,subsubdiv,'MISSING','MISSING'])

                                        #normal
                                        else:
                                            soup = BeautifulSoup(response.read(), 'html.parser')

                                            # Extract cell contents
                                            for link in soup.find_all(has_subdivname):

                                                #find div name
                                                # for font in link.find_all('font'):
                                                #     if font.has_attr('size'):
                                                #         if font['size'] == '3':
                                                #             subdiv = font.string


                                                #find position and name
                                                for tag in link.find_all('tr'):
                                                    if tag.has_attr('valign'):
                                                        if tag.td is not None:
                                                            if tag.td.a is not None:
                                                                if tag.td.a.has_attr('name') and tag.td.a.string is not None:
                                                                    pos = tag.td.a.string.strip()
                                                                    names = tag.td.next_sibling.next_sibling.font.get_text().strip().split('\n')

                                                                    #no name
                                                                    if names[0] != '-':
                                                                        #why is their address part of their name
                                                                        name = names[0]
                                                                        print '\t'.join([org,div,subdiv,subsubdiv,pos,name])





        # delay 0.1 sec and reset
        time.sleep(0.1)
        div = ''
        subdiv = ''
        subsubdiv = ''


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
