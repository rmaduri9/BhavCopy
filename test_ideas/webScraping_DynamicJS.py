'''
Created on 16-Apr-2017

@author: rmaduri
'''

import sys
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebPage

import bs4 as bs
import urllib2

class Client(QWebPage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        self.loadFinished.connect(self.on_page_load)
        self.mainFrame().load(QUrl(url))
        self.app_exec_()
        
    def on_page_load(self):
        self.app.quit()
        
        
url = "http://python.org"
client_response = Client(url)
source = client_response.mainFrame().toHtml()
soup = bs.BeautifulSoup(source, 'lxml')

# data after js processed
js_test = soup.find('p', class_='jstest')
print(js_test.text)