#get html docs
import urllib2

url_toplevel = 'http://eresources.nlb.gov.sg/webarchives/wayback/20070223201456/http://app.sgdi.gov.sg/'

headers = { 'User-Agent' : 'Mozilla/5.0' }
req = urllib2.Request(url_toplevel, None, headers)
html = urllib2.urlopen(req).read()

print html