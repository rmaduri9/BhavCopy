'''
Created on 14-Apr-2017

@author: rmaduri
'''

import sys
import tkinter as tk
import tkinter.ttk as ttk
import DBMysql

import numpy as np

import matplotlib
from test.test_asyncio.test_base_events import MyDatagramProto
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt



LARGE_FONT= ("Verdana", 12)
GraphFrame = 0




class graphPage(tk.Frame):

    def __init__(self, parent, xData, yData, *args, **kwarg):
        tk.Frame.__init__(self, parent, *args, **kwarg)
        self.parent = parent
        self.xData = xData
        self.yData = yData
        self.refresh()


    def updateGraph(self, xData, yData):
        self.xData = xData
        self.yData = yData
        self.refresh()
        
    def refresh(self):
        if self.xData:
#             fig = plt.figure(1)
#             plt.ion()
#             plt.plot(self.xData, self.yData)
#             
#             canvas = FigureCanvasTkAgg(fig, master=self)
#             plot_widget = canvas.get_tk_widget()
#             fig.canvas.draw()
           
            
            f = Figure(figsize=(1,1), dpi=100)
            f.clear()
            a = f.add_subplot(111)
            a.plot(self.xData, self.yData)
 
            canvas = FigureCanvasTkAgg(f, self)
            canvas.show()
            canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
 
            #toolbar = NavigationToolbar2TkAgg(canvas, self)
            #toolbar.update()
            canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
             


class FrameGUI(tk.Frame):
  
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)   
         
        self.parent = parent
        self.db = DBMysql.DBMysql()
        self.scNames = self.dbBCName()
        self.lbData = list()
        self.initUI()

    def dbBCName(self):
        selSQL = "Select * from scname order by SC_NAME"
        result = self.db.getDBResult(selSQL)
        return result

    def evt_txtSearch(self, event):
        txt = self.srchText.get()
        self.fillSCNames(self.pwLB, txt.upper())

    def evt_lbSCNamesDC(self, event):
        index = self.pwLB.curselection()
        
        row = self.lbData[index[0]]
        selSQL = "Select * from equity where SC_CODE = %s order by TR_DATE" % (row['SC_CODE'])
        result = self.db.getDBResult(selSQL)
        self.txtDetail.delete(1.0, tk.END)
        if result:
            txt = "%s \t %s \t %s \t %s \t %s \n" % ('TR_DATE', 'CUR_LAST', 'G_UNIT', 'G_RATE', 'X_RATE')
            self.txtDetail.insert(tk.END, txt)
            txt = "%s \t %s \t %s \t %s \t %s \n" % ('-------', '--------', '------', '------', '------')
            self.txtDetail.insert(tk.END, txt)

            for row in result:
                txt = "%s \t %s \t %s \t %s \t %s \n" % (row['TR_DATE'], row['CUR_LAST'], row['G_UNIT'], row['G_RATE'], row['X_RATE'])
                self.txtDetail.insert(tk.END, txt)
            
            xData = [row['TR_DATE'] for row in result]
            yData = [row['G_UNIT'] for row in result]
            self.graphNW.updateGraph(xData, yData) 
            
            yData = [row['CUR_LAST'] for row in result]
            self.graphNE.updateGraph(xData, yData)
        

    def fillSCNames(self, listbox, filter):
        listbox.delete(0, len(self.lbData)-1)
        self.lbData.clear()
        if filter =="":
            for row in self.scNames:
                listbox.insert(tk.END, "%s-%s" % (row['SC_CODE'], row['SC_NAME']))
                self.lbData.append(row)
        else:   
            for row in self.scNames:
                txt = "%s-%s" % (row['SC_CODE'], row['SC_NAME'])
                if filter in txt:
                    listbox.insert(tk.END, txt)
                    self.lbData.append(row)
                



    def initUI(self):
        self.pack(fill=tk.BOTH, expand=True)
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure(".", font=LARGE_FONT)

        frHead = tk.Frame(self, relief=tk.RAISED)
        frHead.grid_rowconfigure(0, weight=1)
        
        for i in range(11):
            frHead.grid_columnconfigure(i, weight=1)
        
        btnGUnit = ttk.Button(frHead, text="GUnit")
        btnGUnit.grid(row=0, column=0, sticky=tk.NSEW)
        
           

        frHead.pack(fill=tk.X, anchor=tk.N)
        
        
        pw1 = tk.PanedWindow(self)
        pw1.pack(fill=tk.BOTH, expand=True)

        pw1F = tk.Frame(pw1)
        pw1F.pack(fill=tk.BOTH, expand=True)
        
        self.srchText = tk.Entry(pw1F, width=10, relief=tk.RAISED)
        self.srchText.bind("<Return>", self.evt_txtSearch)
        self.srchText.pack(fill=tk.X)
        
        self.pwLB = tk.Listbox(pw1F, background="grey", font = ("Courier New", 14))
        self.pwLB.pack(fill=tk.BOTH, expand=True)
        self.pwLB.bind("<Double-Button-1>", self.evt_lbSCNamesDC)
        # add data to listbox.
        self.fillSCNames(self.pwLB, '')
        #for row in self.scNames:
        #    self.pwLB.insert(tk.END, "%s-%s" % (row['SC_CODE'], row['SC_NAME']))
        

        pwRight= tk.Frame(pw1, background="blue")
        pwRight.grid()
       
        # 2x2 grid
        for i in range(2):
            pwRight.grid_rowconfigure(i, weight=1)
            pwRight.grid_columnconfigure(i, weight=1)

        #grNW = tk.Frame(pwRight, background="blue")
        self.graphNW = graphPage(pwRight, None, None, background="grey")
        self.graphNW.grid(row=0, column=0, sticky=tk.NSEW)
        
        
        self.graphNE = graphPage(pwRight, None, None, background="grey")
        self.graphNE.grid(row=0, column=1, sticky=tk.NSEW)
        
        #frS = tk.Frame(pwRight, background="green")
        #frS.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)
        
        self.txtDetail = tk.Text(pwRight, background="grey", height=-1, font = ("Courier New", 14))
        self.txtDetail.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)

        
        
        pw1.add(pw1F)
        pw1.add(pwRight)

        
        frFooter = tk.Frame(self, relief=tk.RAISED, background="grey", height=30)
        frFooter.pack(fill=tk.X)

 




def main():
    print(sys.version)
    root = tk.Tk()
    root.geometry("1024x768+0+0")
    # root.resizable(False, False)
    app = FrameGUI(root)
    root.mainloop()  


if __name__ == '__main__':
    main()