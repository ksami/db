import sys
import re
import time
from urllib2 import Request, urlopen
from urllib2 import HTTPError
from bs4 import BeautifulSoup

base_url = 'http://eresources.nlb.gov.sg/webarchives/wayback/20070223201456/http://app.sgdi.gov.sg/'

def main():
    if len(sys.argv) < 2:
        print 'not enough arguments'
        exit(1)

    file_name = sys.argv[1]
    #file_name = './html/min/mcys.html'
    org = file_name.replace('.html', '')
    div = ''
    subdiv1 = ''
    subdiv2 = ''
    subdiv3 = ''
    subdiv4 = ''
    subdiv5 = ''
    subdiv6 = ''
    subdiv7 = ''
    subdiv8 = ''
    subdiv9 = ''

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
    print 'Organization\tDivision\tSubdivision\tSubsubdivision\tSubsubsubdivision\tSubdivision4\tSubdivision5\tSubdivision6\tSubdivision7\tSubdivision8\tSubdivision9\tPost\tFull Name'
    for cell in cells:
        fields = cell.split('\n')
        # no name
        if(fields[2].strip() != '-'):
            print '\t'.join([org,div,subdiv1,subdiv2,subdiv3,subdiv4,subdiv5,subdiv6,subdiv7,subdiv8,subdiv9,fields[0].strip(),fields[2].strip()])
        

    # Divisions
    # start from div index 1
    extractContent(soup, [org, div, subdiv1, subdiv2, subdiv3, subdiv4, subdiv5, subdiv6, subdiv7, subdiv8, subdiv9], 1)


    html_doc.close()





def extractContent(soup, orglist, level):
    # get division links
    for link in soup.find_all('a'):
        if(link.parent.name == 'font' and link.parent.has_attr('size') and link.get('href') is not None):
            url = link.get('href')
            if(link.parent['size'] == '2' and url.find('listing.asp?agency_subtype=dept') is not -1):
                if((url.find('http') is -1) and (url.find('#dept_anchor') is -1)):

                    #set org level
                    orglist[level] = link.get_text()
                    org = orglist[0]
                    div = orglist[1]
                    subdiv1 = orglist[2]
                    subdiv2 = orglist[3]
                    subdiv3 = orglist[4]
                    subdiv4 = orglist[5]
                    subdiv5 = orglist[6]
                    subdiv6 = orglist[7]
                    subdiv7 = orglist[8]
                    subdiv8 = orglist[9]
                    subdiv9 = orglist[10]


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
                        print '\t'.join([org, div, subdiv1, subdiv2, subdiv3, subdiv4, subdiv5, subdiv6, subdiv7, subdiv8, subdiv9,'MISSING','MISSING'])

                    #normal
                    else:
                        doc = response.read().replace('</br>', '<br>')
                        soup = BeautifulSoup(doc, 'html.parser')

                        # Extract cell contents
                        for link in soup.find_all(has_subdivname):

                            #find div/subdiv/subdiv2 name
                            # for font in link.find_all('font'):
                            #     if font.has_attr('size'):
                            #         if font['size'] == '3':
                            #             if is_first:
                            #                 div = font.string
                            #                 is_first = False
                            #             else:
                            #                 subdiv = font.string
                            #             break

                            #find position and name
                            for tag in link.find_all('tr'):
                                if tag.has_attr('valign'):
                                    if tag.td is not None:
                                        if tag.td.a is not None:
                                            if tag.td.a.has_attr('name') and tag.td.a.string is not None:
                                                poss = tag.td.a.string.strip().split('\n')
                                                names = tag.td.next_sibling.next_sibling.font.get_text().strip().split('\n')

                                                #no name
                                                if names[0] != '-':
                                                    #discard address in name/pos and replace unicode apostrophe
                                                    #and discard other unicode chars
                                                    pos = poss[0].replace( u'\x92', u'\'').encode('ascii', 'ignore')
                                                    name = names[0].replace( u'\x92', u'\'').encode('ascii', 'ignore')
                                                    print '\t'.join([org,div,subdiv1,subdiv2,subdiv3,subdiv4,subdiv5,subdiv6,subdiv7,subdiv8,subdiv9,pos,name])
                        
                        # delay 0.1 sec
                        time.sleep(0.1)

                        #recursively extract content
                        extractContent(soup, [org,div,subdiv1,subdiv2,subdiv3,subdiv4,subdiv5,subdiv6,subdiv7,subdiv8,subdiv9], (level+1))
                        






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
