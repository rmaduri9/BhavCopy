'''
Created on 16-Apr-2017

@author: rmaduri
'''

import bs4 as bs
import urllib2

response = urllib2.urlopen("http://python.org")
html = response.read()

bsData = bs.BeautifulSoup(html, 'lxml')

a = bsData.find_all("a")

# print(bsData.title.text)

# rint(bsData.find_all('p'))

#for para in bsData.find_all('p'):
#    print(para.string)


# for url in bsData.find_all("a"):
#     print(url.get("href"))

# nav = bsData.nav
# 
# for url in nav.find_all('a'):
#     print(url.get('href'))


# for div in bsData.find_all('div', class_="do-not-print"):
#     print(div.text)
    
tbl = bsData.find('table')
tblR = tbl.find_all('tr')

for tr in tblR:
    td = tr.find_all('td')
    row = [i.text for i in td] 
    print(row)   
      
    