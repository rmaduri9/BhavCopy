'''
Created on 14-Apr-2017

@author: rmaduri
'''

import mysql.connector
import datetime 
from mysql.connector import cursor
import decimal


class DBMysql():
    def __init__(self):
        self.CNX = mysql.connector.connect(user='rmaduri', password='madmed70', host='127.0.0.1', database='bhavCopy')

    def getDBResult(self, selSQL):
        cursor = self.CNX.cursor(dictionary=True, buffered = True)
        cursor.execute(selSQL)
        result = cursor.fetchall()
        return result
     
    def dateAsYMD(self, dt):
        return "%04d-%02d-%02d" % (dt.year, dt.month, dt.day) 
            

    def DBClose(self):
        self.CNX.commit()
        self.CNX.close()
