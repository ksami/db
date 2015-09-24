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
    orglist = ['' for _ in range(11)]
    orglist[0] = file_name.replace('.html', '')
    # org = file_name.replace('.html', '')
    

    html_doc = open(file_name, 'r')

    soup = BeautifulSoup(html_doc.read(), 'html.parser')
    # print(soup.prettify())

    # Printing
    print 'Organization\tDivision\tSubdivision\tSubsubdivision\tSubsubsubdivision\tSubdivision4\tSubdivision5\tSubdivision6\tSubdivision7\tSubdivision8\tSubdivision9\tPost\tFull Name'

    # Process divs page
    for tr in soup.find_all(is_div):
        url = tr.td.a.get('href')
        orglist[1] = tr.td.a.get_text().strip()
        

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
            print '\t'.join(['\t'.join(orglist),'MISSING','MISSING'])

        #normal
        else:
            doc = response.read().replace('</br>', '<br>')
            soup = BeautifulSoup(doc, 'html.parser')

            # Extract cell contents
            for link in soup.find_all(has_subdivname):
                level = 2
                has_leveledup = False

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
                                if tag.td.a.has_attr('name') and tag.td.a.get_text() is not None:
                                    poss = tag.td.a.get_text('\n').strip().split('\n')
                                    names = tag.td.next_sibling.next_sibling.font.get_text().strip().split('\n')

                                    #no name
                                    if names[0] != '-':
                                        #discard address in name/pos and replace unicode apostrophe
                                        #and discard other unicode chars
                                        pos = poss[0].strip().replace( u'\x92', u'\'').encode('ascii', 'ignore')
                                        if len(poss) > 1:
                                            has_leveledup = True
                                            orglist[level] = poss[1].strip().replace( u'\x92', u'\'').encode('ascii', 'ignore')

                                        name = names[0].strip().replace( u'\x92', u'\'').encode('ascii', 'ignore')
                                        print '\t'.join(['\t'.join(orglist),pos,name])
            

            # Subdivisions
            # start from subdiv index 2 or if already filled, index 3
            if has_leveledup:
                extractContent(soup, orglist, (level+1))
            else:
                extractContent(soup, orglist, level)
        


    html_doc.close()





def extractContent(soup, orglist_orig, level, is_cmtepage=False):
    # get division links
    for link in soup.find_all('a'):
        if(link.get('href') is not None):

            url = link.get('href')
            if( (not is_cmtepage) and (link.get('href').find('http') is -1) and (link.get('href').find('listing.asp?agency_subtype=cmte') is not -1) ):
                #set org level
                orglist = orglist_orig[:]
                orglist[level] = link.get_text()

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
                    print '\t'.join(['\t'.join(orglist),'MISSING','MISSING'])

                #normal
                else:
                    doc = response.read().replace('</br>', '<br>')
                    soup = BeautifulSoup(doc, 'html.parser')

                    extractContent(soup, orglist, level, True)


            if(link.parent.name == 'font' and link.parent.has_attr('size')):
                if(link.parent['size'] == '2'):

                    if( (url.find('http') is -1) and (url.find('listing.asp?agency_subtype=dept') is not -1) and (url.find('#dept_anchor') is -1) ):

                        #set org level
                        orglist = orglist_orig[:]
                        orglist[level] = link.get_text()
                        has_leveledup = False

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
                            print '\t'.join(['\t'.join(orglist),'MISSING','MISSING'])

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
                                                if tag.td.a.has_attr('name') and tag.td.a.get_text() is not None:
                                                    poss = tag.td.a.get_text('\n').strip().split('\n')
                                                    names = tag.td.next_sibling.next_sibling.font.get_text().strip().split('\n')

                                                    #no name
                                                    if names[0] != '-':
                                                        #discard address in name/pos and replace unicode apostrophe
                                                        #and discard other unicode chars
                                                        pos = poss[0].strip().replace( u'\x92', u'\'').encode('ascii', 'ignore')
                                                        if len(poss) > 1:
                                                            has_leveledup = True
                                                            orglist[level+1] = poss[1].strip().replace( u'\x92', u'\'').encode('ascii', 'ignore')

                                                        name = names[0].strip().replace( u'\x92', u'\'').encode('ascii', 'ignore')
                                                        print '\t'.join(['\t'.join(orglist),pos,name])
                            
                            # delay 0.1 sec
                            time.sleep(0.1)

                            #recursively extract content
                            if has_leveledup:
                                extractContent(soup, orglist, (level+2))
                            else:
                                extractContent(soup, orglist, (level+1))
                            


# get div names and links for Others
def is_div(tag):
    if tag.name == 'tr' and tag.parent.name == 'table':
        if tag.has_attr('valign') and tag.parent.has_attr('width'):
            if tag.td is not None and tag.parent['width'] == '100%':
                if tag.td.a is not None:
                    if tag.td.a.has_attr('href'):
                        if tag.td.a.get('href').find('listing.asp?agency_subtype=dept') is not -1 and tag.td.a.get('href').find('#dept_anchor') is -1:
                            return True
    return False


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
