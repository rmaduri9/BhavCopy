'''
Created on 03-Apr-2017

@author: rmaduri

http://www.bseindia.com/download/BhavCopy/Equity/EQ_ISINCODE_310317.zip

uses python 2
'''

import urllib2
import os.path
import mysql.connector
import sys
from datetime import date
from decimal import Decimal


url = "http://www.bseindia.com/download/BhavCopy/Equity/"
bhavDir = "/Users/rmaduri/Downloads/BhavCopy/"
outDir = bhavDir + "data/current/"
csvDir = bhavDir + "csv/"

def downloadBhav(file_name):
    if os.path.isfile(outDir + file_name): return

    u = urllib2.urlopen(url + file_name)
    f = open(outDir + file_name, 'wb')

    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size) ,

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        ## status = status + chr(8)*(len(status)+1)
        ## print status,
    f.close()
    print status


def downloadAll():
    for m in range(1,13):
        for d in range(1,32):
            file_name = "eq%02d%02d17_csv.zip" % (d, m)
            try:
                if not os.path.isfile(outDir + file_name):
                    downloadBhav(file_name)
            except urllib2.HTTPError:
                ## print("Error reading file " + file_name)
                pass



def readAllHeaders():
    allHeaders = set()
    for f in os.listdir(csvDir):
        fileLine = open(csvDir + f)
        allHeaders.add(fileLine.readline())
        fileLine.close()
    print(allHeaders)



def dataLine(fileName, line):
    # DMY
    ymd = date(int(fileName[6:8]), int(fileName[4:6]), int(fileName[2:4]))
    items = line.split(",")
    
    for i in [4,5,6,7,8,9,10,12]:
        if items[i].strip() == "":
            items[i] = "0.00"
    if items[11].strip() == "":
        items[11] = "0"
    
    dataEq = {
        'trDate' : date(int("20" + fileName[6:8]), int(fileName[4:6]), int(fileName[2:4])),
        'scCode' : items[0].strip(),
        'scName' : items[1].strip(),
        'scGroup': items[2].strip(),
        'scType' : items[3].strip(),
        'curOpen': Decimal(items[4].strip()),
        'curHigh': Decimal(items[5].strip()),
        'curLow' : Decimal(items[6].strip()),
        'curClose': Decimal(items[7].strip()),
        'curLast' : Decimal(items[8].strip()),
        'prvClose': Decimal(items[9].strip()),
        'numTrades': Decimal(items[10].strip()),
        'numShares': int(items[11].strip()),
        'netTurn'  : Decimal(items[12].strip()),
        'tdCloIndi': items[13].strip()
        }
    
    return dataEq
    
def connectDB():
    cnx = mysql.connector.connect(user='rmaduri', password='madmed70', host='127.0.0.1', database='bhavCopy')
    return cnx;

def dataToDB():
    cnx = connectDB()
    cursor = cnx.cursor()
    insDataSQL = ("Insert into equity "
                   "(TR_DATE, SC_CODE, SC_NAME, SC_GROUP, SC_TYPE, "
                   "CUR_OPEN, CUR_HIGH, CUR_LOW, CUR_CLOSE, CUR_LAST, PRV_CLOSE, "
                   "NO_TRADES, NO_OF_SHRS, NET_TURNOV, TDCLOINDI) "
                   "VALUES (%(trDate)s, %(scCode)s, %(scName)s, %(scGroup)s, %(scType)s, "
                   "%(curOpen)s, %(curHigh)s, %(curLow)s, %(curClose)s, %(curLast)s, %(prvClose)s, "
                   "%(numTrades)s, %(numShares)s, %(netTurn)s, %(tdCloIndi)s )" )
    
    selDataSQL = ("Select count(1) as count from equity where TR_DATE = %(trDate)s")
    delDataSQL = ("Delete from equity where TR_DATE = %(trDate)s")
    
    
    for f in os.listdir(csvDir):
        print(f)
        lines = open(csvDir + f).readlines()[1:]
        
        dataEquity = dataLine(f, lines[0])
        cursor.execute(selDataSQL, dataEquity)
        
        row = cursor.fetchone()
        if len(lines) != row[0]:
            print("Deleting records for " + f)
            cursor.execute(delDataSQL, dataEquity)
            cnx.commit()
        
            iComitCount = 0
            for line in lines:
                dataEquity = dataLine(f, line)
                cursor.execute(insDataSQL, dataEquity)
                iComitCount += 1
                if iComitCount % 1000 == 0:
                    cnx.commit()
            cnx.commit()
    
    cnx.close()

# return the result as {key:value, key:value} list of rows.
def getDBResult(cnx, selSQL):
    cursor = cnx.cursor()
    cursor.execute(selSQL)
    fields = map(lambda x : x[0], cursor.description)
    result = [dict(zip(fields, row)) for row in cursor.fetchall()]
    return result

def dateAsYMD(dt):
    return "%04d-%02d-%02d" % (dt.year, dt.month, dt.day)

def getDBValues_Date(cnx, selField, selSQL):
    result = getDBResult(cnx, selSQL)
    trDate = [dateAsYMD(row[selField]) for row in result]
    trDate.sort()
    return trDate


def dataAsGrid(smryFields, whereDate):
    cnx = connectDB()
    cursor = cnx.cursor()
    selSQL = "SELECT DISTINCT TR_DATE FROM EQUITY "
    trDate = getDBValues_Date(cnx, "TR_DATE", selSQL + whereDate)

    scName = dict()
    scData = dict()
    # get scCode and scName as the data is read by date.
    i = 0
    for strDt in trDate:
        print("%s : %d of %d" % (strDt, i, len(trDate)))
        selSQL = "Select * from equity where TR_DATE = '%s'" % strDt
        result = getDBResult(cnx, selSQL)
        for row in result:
            if scName.get(row["SC_CODE"]) == None:
                scName[row["SC_CODE"]] = row["SC_NAME"]
        
            if scData.get(row["SC_CODE"]) == None:
                scData[row["SC_CODE"]] = {}
            scData[row["SC_CODE"]][strDt]= [row[smryField] for smryField in smryFields]
        i += 1
        
    ## print to file.                
    fo = open(bhavDir + "data_" + smryFields[0] + ".csv", "w")
    fo.write(",,," + ",".join(["'" + dt  for dt in trDate]) + "\n")
    for scnKey in scName.keys():
        sLine = '"%s", "%s",' %(scnKey, scName[scnKey])
        sData = ""
        scd = scData[scnKey]
        for sf in range(len(smryFields)):
            sData = smryFields[sf] + ","
            for dt in trDate:
                if scd.get(dt) == None:
                    sData = sData + "0,"
                else:
                    sData = sData + str(scd[dt][sf]) + ","
            fo.write(sLine + sData + "\n")
            print(sLine + sData)
        print('')
        fo.flush()
    fo.close()

def main():
    ## downloadAll()
    # readAllHeaders()
    # dataToDB()
    
    dataAsGrid( ("CUR_CLOSE", "NO_OF_SHRS"), " WHERE YEAR(TR_DATE) = 2008 AND MONTH(TR_DATE) = 01 and (DAY(TR_DATE) >= 1 AND DAY(TR_DATE) <= 5)")
    print("Done")



if __name__ == "__main__":
    main()
