from bs4 import BeautifulSoup

file_name = './html/min/mcys'

html_doc = open(file_name, 'r')

soup = BeautifulSoup(html_doc.read(), 'html.parser')
# print(soup.prettify())

# //TODO parse each html file
# //TODO add .html extensions to all html files
for link in soup.find_all('font'):
  print(link.string)

html_doc.close()
