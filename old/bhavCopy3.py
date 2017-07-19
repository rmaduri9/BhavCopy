'''
Created on 09-Apr-2017

@author: rmaduri
'''

import sys
import tkinter as tk
import mysql.connector
import datetime 
from mysql.connector import cursor
import decimal

DT_MAX = datetime.date(2999, 12, 31)


class DBMysql():
    def __init__(self):
        self.CNX = mysql.connector.connect(user='rmaduri', password='madmed70', host='127.0.0.1', database='bhavCopy')
        self.getInitValues()

    def getDBResult(self, selSQL):
        cursor = self.CNX.cursor(dictionary=True, buffered = True)
        cursor.execute(selSQL)
        
        #fields = list(map(lambda x : x[0], cursor.description))       
        #result = [dict(zip(fields, row)) for row in cursor.fetchall()]
        
        result = cursor.fetchall()
        self.CNX.commit()
        return result
     
    def dateAsYMD(self, dt):
        return "%04d-%02d-%02d" % (dt.year, dt.month, dt.day) 
     
        
    def getInitValues(self):
        selSQL = "Select distinct TR_DATE from equity order by TR_DATE desc"
        result = self.getDBResult(selSQL)
        self.trDate = [self.dateAsYMD(row["TR_DATE"]) for row in result]
 
    def getDateList(self):
        return self.trDate
        


    def updateDB(self, res, tbl, fld, val):
        res[fld] = val
        if val == 'null':
            updSQL = "Update %s set %s = %s where seq = %s" % (tbl, fld, val, res['seq'])
        else:
            updSQL = "Update %s set %s = '%s' where seq = %s" % (tbl, fld, val, res['seq'])
        cursor = self.CNX.cursor()
        cursor.execute(updSQL)
        self.CNX.commit()
        
    def updateYmd_to(self, tbl, wh):
        if wh == '': wh = " 1=1 "
        # Update ymd_to = ymd_fr
        cursor = self.CNX.cursor()
        updSQL = "update %s set ymd_to = ymd_fr where %s" % (tbl, wh)
        cursor.execute(updSQL)
        self.CNX.commit()       
        
        # mark the last items ymd_to = 2999-12-31'
        selSQL = "select * from %s where (%s) order by ymd_fr" % (tbl, wh) 
        result = self.getDBResult(selSQL)
        i = len(result)-1
        self.updateDB(result[i], tbl, 'ymd_to', DT_MAX)
        
        prv = result[0]
        for row in result[1:]:
            if prv['ymd_fr'] + datetime.timedelta(days=1) != row['ymd_fr']:
                self.updateDB(prv, tbl, 'ymd_to', row['ymd_fr'] + datetime.timedelta(days=-1))
            prv = row

        self.CNX.commit()
        

    def DBClose(self):
        self.CNX.commit()
        self.CNX.close()


DB = DBMysql()



    

class DayListFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.dayList = tk.Listbox(self, relief=tk.RAISED, selectmode=tk.MULTIPLE, width=12)
        self.dayList.pack(fill=tk.BOTH, expand=True)
        self.dayListData = DB.getDateList()
        
        self.initUI()
        
        
    def initUI(self):
        for dt in self.dayListData:
            self.dayList.insert(tk.END, dt)
        
    def getSelectedList(self):
        items = self.dayList.curselection()
        items = [self.dayListData[item] for item in items]
        return items



        
            

class Example(tk.Frame):
  
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)   
         
        self.parent = parent
        self.initUI()


    def getDayList(self):
        print(self.leftFrame.getSelectedList())
        
    def initUI(self):
        self.parent.title("Bhavcopy")
        self.pack(fill=tk.BOTH, expand=True)    
    
    
        self.frameButtonbar = tk.Frame(self, relief=tk.RAISED, height=30)
        self.frameButtonbar.grid_rowconfigure(0, weight=1)
        for c in range(8):
            self.frameButtonbar.grid_columnconfigure(c, weight=1)
        
        btn = tk.Button(self.frameButtonbar, text="Button", command=self.getDayList).grid(row=0, column=0, sticky=tk.E+tk.W)        
        self.frameButtonbar.pack(fill=tk.X)
   
   
        self.pWindow = tk.PanedWindow(self)
        self.pWindow.pack(fill=tk.BOTH, expand=True)    
        self.leftFrame = DayListFrame(self.pWindow, relief=tk.RAISED)
        self.pWindow.add(self.leftFrame)    

        self.rightFrame = tk.Frame(self.pWindow, relief=tk.RAISED, background = "red")
        self.rightFrame.grid_columnconfigure(0, weight=1)
        self.rightFrame.grid_rowconfigure(0, weight=1)
        self.pWindow.add(self.rightFrame)
        
        
        
# '''   
#         class DataGrid(tk.Frame):
#     def __init__(self, parent, dateList, *args, **kwargs):
#         tk.Frame.__init__(self, parent, *args, **kwargs)
#         
#         dateList = ['"'+ d + '"' for d in dateList]
#         wc = " where TR_DATE in (" + ",".join(dateList)+ ")"
# 
#         result = DB.getDBResult("Select * from equity " + wc)
#         fieldList = list(result[0].keys())
#         
#         self.header = tk.Frame(parent, relief=tk.RAISED, height=30)
#         print(fieldList)
#         for f in range(len(fieldList)): 
#             self.header.grid_columnconfigure(f, weight=1)
#             tk.Label(self.header, text=fieldList[f] ).grid(row = 0, column=f, sticky=tk.N+tk.E+tk.W)
#         
# '''   
        
        
        self.t = tk.Frame(self.rightFrame, background="grey", height=30)
        result = DB.getDBResult("Select * from equity where TR_DATE = '2017-01-05'")
        fieldList = list(result[0].keys())
        
        for f in range(len(fieldList)):
            self.t.grid_columnconfigure(f, weight=1)
            tk.Label(self.t, text=fieldList[f], background="grey").grid(row=0, column=f, sticky=tk.N+tk.E+tk.W)
        self.t.grid(row=0, column=0, sticky=tk.E+tk.N+tk.W)
        
        #self.t2 = tk.Frame(self.rightFrame, background="blue")
        #self.t2.pack(fill=tk.BOTH, expand=True)
           
        #self.frame1b = tk.Frame(self.pWindow, relief=tk.RAISED, background="grey", height=30)
        #self.frame1b.pack(fill=tk.X)
        
    
        

def main():
    print(sys.version)
    root = tk.Tk()
    root.geometry("800x600+0+0")
    app = Example(root)
    root.mainloop()  



def main2():
    #DB.updateYmd_to("curxchg", "fr_curr = 'USD' and to_curr = 'INR'")
    #DB.updateYmd_to('gldusd', "1=1")
    #DB.DBClose()


    cur = DB.CNX.cursor(dictionary = True, buffered = True)
    selSQL = "Select distinct TR_DATE from equity"
    cur.execute(selSQL)
    eqTRD = cur.fetchall()
    for row in eqTRD:
        selSQL = "Select rate from curxchg where fr_curr = '%s' and to_curr = '%s' and ('%s' between ymd_fr and ymd_to)" % ('USD', 'INR', DB.dateAsYMD(row['TR_DATE']))
        cur.execute(selSQL)
        xrate = cur.fetchone()
        if xrate == None: continue

        selSQL = "Select rate from gldusd where ('%s' between ymd_fr and ymd_to)" % (DB.dateAsYMD(row['TR_DATE'],) )
        cur.execute(selSQL)
        grate = cur.fetchone()
        if grate == None: continue        

        xrate = xrate['rate']
        grate = grate['rate']
        
        gr = grate * xrate / decimal.Decimal(100.0)
        updSQL = "Update equity set G_RATE = %s, X_RATE = %s where TR_DATE = '%s'" % (grate, xrate, row['TR_DATE'])
        cur.execute(updSQL)
        DB.CNX.commit()
        
        updSQL = "Update equity set G_UNIT = CUR_LAST / ( G_RATE * X_RATE / 100.0) where TR_DATE = '%s'" % (row['TR_DATE'], )
        cur.execute(updSQL)
        
        DB.CNX.commit()




#     cur = DB.CNX.cursor(dictionary=True, buffered = True)
#     selSQL = "Select * from equity where SC_CODE = 500002"
#     cur.execute(selSQL)
#     eqRes = cur.fetchall()
#     
#     for eq in eqRes:
#         selSQL = "Select rate from curxchg where fr_curr = '%s' and to_curr = '%s' and ('%s' between ymd_fr and ymd_to)" % ('USD', 'INR', DB.dateAsYMD(eq['TR_DATE']))
#         cur.execute(selSQL)
#         xrate = cur.fetchone()
#         if xrate == None: continue
# 
#         selSQL = "Select rate from gldusd where ('%s' between ymd_fr and ymd_to)" % (DB.dateAsYMD(eq['TR_DATE'],) )
#         cur.execute(selSQL)
#         grate = cur.fetchone()
#         if grate == None: continue
#         
#         xrate = xrate['rate']
#         grate = grate['rate']
#         
#         grate = grate * xrate / decimal.Decimal(100.0)
#         
#         gUnit = eq['CUR_LAST'] / grate
#         updSQL = "Update equity set G_UNIT = %s, G_RATE = %s where TR_DATE = '%s' and SC_CODE = %s" % (gUnit, grate, eq['TR_DATE'], eq['SC_CODE'])
#         cur.execute(updSQL)
#         
#     DB.CNX.commit()

    
    DB.DBClose()
    
if __name__ == '__main__':
    main()