'''
Created on 15-Apr-2017

@author: rmaduri

DB, MVC, tkinter, DP, OOP, Python Constructs, WebScraping, ML

'''

import sys

import mysql.connector
from mysql.connector import cursor

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.figure
import matplotlib.dates as mdates
import matplotlib.ticker as mticker

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg

if sys.version_info.major == 3:
    import tkinter as tk
    import tkinter.ttk as ttk
else:
    import Tkinter as tk
    import ttk
    


class AppConst():
    APP_TITLE = "BhavCopy"
    
    APP_FONT_VERDANA_NORMAL= ("Verdana", 12)
    APP_FONT_VERDANA_SMALL = ("Verdana", 8)
    APP_FONT_COURIER_NORMAL = ("Courier New", 14)
    
    APP_GEOMETRY = "1024x768+0+0"

    DATE_FMT_YMD = "%04d-%02d-%02d"
    DATE_FMT_Y00 = "%s-01-01"
            
    APP_GRAPHBYVIEW = ('Open', 'High', 'Low', 'Close', 'Last', 'PClose', 'Trades', 'Shares', 'Turnover', 'G_Rate', 'G_Unit', 'X_Rate')
    APP_GRAPHBYFIELD = ('CUR_OPEN', 'CUR_HIGH', 'CUR_LOW', 'CUR_CLOSE', 'CUR_LAST', 'PRV_CLOSE', 'NO_TRADES', 'NO_OF_SHRS', 'NET_TURNOV', 'G_RATE', 'G_UNIT', 'X_RATE')

    
    APP_GFRAME_NE = "NE"
    APP_GFRAME_NW = "NW"

    
    BG_COLOR      = "grey"

    
    BIND_RETURN    = "<Return>"
    BIND_DOUBLE_B1 = "<Double-Button-1>"
    BIND_BUTTON1   = "<Button-1>"
    BIND_RELEASE_B1= "<ButtonRelease-1>"
    
    DB_USER = "rmaduri"
    DB_PASS = "madmed70"
    DB_HOST = "127.0.0.1"
    DB_NAME= "bhavCopy"
    
    DB_SQL_SCNAMES = "select SC_CODE, SC_NAME from scname "
    DB_SQL_EQUITY  = "Select * from equity where %s = %s and TR_DATE >= '%s' order by TR_DATE desc"
    

class GraphView(tk.Frame):
    def __init__(self, parent, *args, **kwarg):
        tk.Frame.__init__(self, parent, *args, **kwarg)
        self.parent = parent
        self.labelVar = tk.StringVar()
        tk.Label(self, textvariable=self.labelVar).pack()
        
        self.updateGraph(None, None, '')

    def updateGraph(self, xData, yData, labelText):
        xData = xData
        yData = yData
        if xData:            
            self.labelVar.set(labelText)
            f = matplotlib.figure.Figure(figsize=(1,1), dpi=100)
            f.clear()
            f.subplots_adjust(left=0.15, bottom=0.20, right=0.95, top=0.95, wspace=0.02, hspace=0)
            
            canvas = FigureCanvasTkAgg(f, master=self)
            
            a = f.add_subplot(111)
            a.plot_date(xData, yData, marker='.', markersize=2)
            
            a.yaxis.set_major_locator(mticker.MaxNLocator(nbins=10))
            a.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            a.xaxis.set_major_locator(mticker.MaxNLocator(nbins=10))

            for l in a.xaxis.get_ticklabels():
                l.set_rotation(45)  
                          
            canvas = FigureCanvasTkAgg(f, master=self)
            canvas.show()
            canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
            
            #toolbar = NavigationToolbar2TkAgg(canvas, self)
            #toolbar.update()
            #canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

#
#  self.lblStatus, self.btnXXXX, self.searchText, self.pwlbData, self.graphNW, self.graphNE, self.detailDataS
#
#
class BC_View(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)   

        self.pack(fill=tk.BOTH, expand=True)
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure(".", font=AppConst.APP_FONT_VERDANA_NORMAL)
        
        self.parent = parent
        self.buttons = list()
        frameHeader = tk.Frame(self, relief=tk.RAISED, height=30, background=AppConst.BG_COLOR)
        #frameHeader.pack(fill=tk.X, anchor=tk.N)
        frameHeader.pack(fill=tk.X)

        # add the buttons
        for btnLbl in AppConst.APP_GRAPHBYVIEW:
            btn = ttk.Button(frameHeader, text=btnLbl, width=10)
            btn.pack(side=tk.LEFT)
            self.buttons.append(btn)
        
        self.vscale = tk.Scale(frameHeader, from_=2000, to=2017, orient=tk.HORIZONTAL, font= AppConst.APP_FONT_VERDANA_SMALL)
        self.vscale.pack(side=tk.LEFT)
        
        #tmp01 = tk.Frame(self, relief=tk.RAISED)
        #tmp01.pack(fill=tk.BOTH, expand=True)
        
        pw01 = tk.PanedWindow(self, background=AppConst.BG_COLOR)
        pw01.pack(fill=tk.BOTH, expand=True)
        
        
        frameFooter = tk.Frame(self, relief=tk.RAISED, background=AppConst.BG_COLOR, height=30)
        frameFooter.pack(fill=tk.X, anchor=tk.S)
        
        self.lblStatusVar = tk.StringVar()
        lblStatus = tk.Label(frameFooter, background=AppConst.BG_COLOR, relief=tk.SUNKEN, textvariable = self.lblStatusVar)
        lblStatus.pack(fill=tk.X, expand=True, side=tk.LEFT)
        
        # Left pane and contents
        pwLeft = tk.Frame(pw01)
        pwLeft.pack(fill=tk.BOTH, expand=True)
        
        self.searchText = tk.Entry(pwLeft, width=10, relief=tk.RAISED)
        self.searchText.pack(fill=tk.X)
        
        self.pwlbData = tk.Listbox(pwLeft, background=AppConst.BG_COLOR, font= AppConst.APP_FONT_COURIER_NORMAL)
        self.pwlbData.pack(fill=tk.BOTH, expand=True)
        
        # right pane and contents
        pwRight = tk.Frame(pw01)
        pwRight.grid()
        for i in range(2):
            pwRight.grid_rowconfigure(i, weight=1)
            pwRight.grid_columnconfigure(i, weight=1)
            
        # self.graphNW = tk.Frame(pwRight, background="red")
        self.graphNW = GraphView(pwRight)
        self.graphNW.grid(row = 0, column=0, sticky=tk.NSEW)
        
        # self.graphNE = tk.Frame(pwRight, background="blue")
        self.graphNE = GraphView(pwRight)
        self.graphNE.grid(row = 0, column=1, sticky=tk.NSEW)
        
        #dataS = tk.Frame(pwRight)
        #dataS.grid(row = 1, column = 0, columnspan=2, sticky=tk.NSEW)
            
        self.detailDataS = tk.Text(pwRight, height = -1, font = AppConst.APP_FONT_COURIER_NORMAL)
        self.detailDataS.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)
        #self.detailDataS.pack(fill=tk.BOTH, expand=True)

        pw01.add(pwLeft)
        pw01.add(pwRight)




class BC_Model():
    def __init__(self):
        print("Open DB Connection")
        try:
            self.CNX = mysql.connector.connect(user=AppConst.DB_USER, password=AppConst.DB_PASS, host=AppConst.DB_HOST, database=AppConst.DB_NAME)
        except mysql.connector.Error as err:
            print("DB error {}".format(err))
            sys.exit()
        self.lbscnameData = list()
        self.detailData = list()
        
        self.currentGraphFrame = AppConst.APP_GFRAME_NE


    def getResult(self, selSQL):
        try:
            cursor = self.CNX.cursor(dictionary=True, buffered = True)
            cursor.execute(selSQL)
            result = cursor.fetchall()
        except mysql.connector.Error as err:
            print("DB error {}".format(err))
        return result
    
    # toggle between the two NE, NW
    def getNextGraphFrame(self):
        if self.currentGraphFrame == AppConst.APP_GFRAME_NE:
            self.currentGraphFrame = AppConst.APP_GFRAME_NW
        else:
            self.currentGraphFrame = AppConst.APP_GFRAME_NE
        return self.currentGraphFrame
    
    def getSCNames(self, wFilter):
        if sys.version_info.major == 3:
            self.lbscnameData.clear()
        else:
            self.lbscnameData = []

        result = self.getResult(AppConst.DB_SQL_SCNAMES + wFilter)
        if result:
            self.lbscnameData.extend(result)
        return self.lbscnameData        
     
    def get_equity_data(self, fieldName, row, yearSince):
        dtSince = AppConst.DATE_FMT_Y00 % yearSince
        selSQL = AppConst.DB_SQL_EQUITY % (fieldName, row[fieldName], dtSince )
        self.detailData = self.getResult(selSQL)
        return self.getDetailData()
    
    def getFieldVector(self, fieldName):
        return [row[fieldName] for row in self.getDetailData()]
    
    def getDetailData(self):
        return self.detailData
                        
    def dateAsYMD(self, dt):
        return AppConst.DATE_FMT_YMD % (dt.year, dt.month, dt.day) 
            
    def __del__(self):
        try:
            self.CNX.commit()
            self.CNX.close()
            print("Close DB connection")
        except:
            return

class BC_Controller():
    def __init__(self):        
        self.root = tk.Tk()
        self.root.geometry(AppConst.APP_GEOMETRY)
        self.view = BC_View(self.root)
        self.model = BC_Model()
        self.bindWidgets()
        self.refresh_viewData()

    def __del__(self):
        self.root.quit()
        # self.root.destroy()

    def refresh_scnameLB(self):
        self.view.pwlbData.delete(0, tk.END)
        wClause = " where SC_NAME like '%%%s%%'" % ( (self.view.searchText.get()).upper(),)
        result = self.model.getSCNames(wClause)
        for row in result:
            self.view.pwlbData.insert(tk.END, "%s-%s" % (row['SC_CODE'], row['SC_NAME']))
        self.view.pwlbData.select_set(first = 0)
        self.view.pwlbData.event_generate("<<ListboxSelect>>")

    def clear_status(self):
        self.view.lblStatusVar.set("")
        
    def refresh_status(self, status):
        self.view.lblStatusVar.set(status)
        self.root.after(2000, self.clear_status)
        
    def refresh_graphData(self, gf, iCol, fieldBy):
        self.refresh_status("Refresh graphData " + fieldBy)
        xData = self.model.getFieldVector('TR_DATE')
        yData = self.model.getFieldVector(fieldBy)
        if not xData: return
        if not yData: return
        
        # create a new graphFrame
        gfNew = GraphView(gf.parent)
        gfNew.grid(row = 0, column=iCol, sticky=tk.NSEW)
        gfNew.updateGraph(xData, yData, fieldBy)        
        

    def refresh_NextGraph(self, fieldBy):
        txt = self.model.getNextGraphFrame()
        if txt == AppConst.APP_GFRAME_NE:
            self.refresh_graphData(self.view.graphNE, 1, fieldBy)
        else:
            self.refresh_graphData(self.view.graphNW, 0, fieldBy)

    def refresh_detailData(self):
        index = self.view.pwlbData.curselection()
        try:
            row = self.model.lbscnameData[index[0]]
            result = self.model.get_equity_data('SC_CODE', row, self.view.vscale.get())
            if not result: return
        except LookupError:
            return 
        
        self.view.detailDataS.delete(1.0, tk.END)
        
        txt = '  TR_DATE    CUR_LAST        G_UNIT           G_RATE           X_RATE\n'
        self.view.detailDataS.insert(tk.END, txt)
            
        txt = "---------- ------------ ---------------- ---------------- ----------------\n"
        self.view.detailDataS.insert(tk.END, txt)

        for row in result:
            txt = "%s %12.2f %16.6f %16.6f %16.6f\n" % (row['TR_DATE'], row['CUR_LAST'], row['G_UNIT'], row['G_RATE'], row['X_RATE'])
            self.view.detailDataS.insert(tk.END, txt)
        
        self.refresh_NextGraph("CUR_LAST") 
        self.refresh_NextGraph("CUR_OPEN")        
        
        
    def refresh_viewData(self):
        self.refresh_scnameLB()
        self.refresh_detailData()

    def event_searchText(self, event):
        self.refresh_scnameLB()
        
    def event_selectedSCCode(self, event):
        self.refresh_detailData()        

    def event_scaleChange(self, event):
        # value = self.view.vscale.get()
        self.refresh_detailData()
        
    def event_buttonbarButton(self, event, buttonLabel):
        ix = AppConst.APP_GRAPHBYVIEW.index(buttonLabel)
        self.nextGraph = AppConst.APP_GRAPHBYFIELD[ix]
        self.refresh_NextGraph(self.nextGraph)
        

    # all the view widgets that are exposed are bound to methods in controller
    def bindWidgets(self):
        #self.view.pwlbData.delete(0, tk.END)
        self.view.searchText.bind(AppConst.BIND_RETURN, self.event_searchText)
        self.view.pwlbData.bind(AppConst.BIND_DOUBLE_B1, self.event_selectedSCCode)
        
        for btn in self.view.buttons:
            btn.bind(AppConst.BIND_BUTTON1, lambda event, lbl = btn.cget('text') : self.event_buttonbarButton(event, lbl))       
            
        self.view.vscale.bind(AppConst.BIND_RELEASE_B1, self.event_scaleChange)

    def run(self):
        self.root.title(AppConst.APP_TITLE)
        self.root.deiconify()
        self.root.mainloop()

def main():
    
    print(sys.version)
    BC_Controller().run()

if __name__ == '__main__':
    main()