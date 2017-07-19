'''
Created on 09-Apr-2017

@author: rmaduri
'''

from tkinter import *

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        
        master.geometry("800x600+100+100")
        
        self.grid()
        self.master.title("Grid Manager")

        for r in range(6):
            self.master.rowconfigure(r, weight=1)    
        for c in range(5):
            self.master.columnconfigure(c, weight=1)
            Button(master, text="Button {0}".format(c)).grid(row=6,column=c,sticky=E+W)

        Frame1 = Frame(master, bg="red")
        Frame1.grid(row = 0, column = 0, rowspan = 3, columnspan = 2, sticky = W+E+N+S) 
        Frame2 = Frame(master, bg="blue")
        Frame2.grid(row = 3, column = 0, rowspan = 3, columnspan = 2, sticky = W+E+N+S)
        Frame3 = Frame(master, bg="green")
        Frame3.grid(row = 0, column = 2, rowspan = 6, columnspan = 3, sticky = W+E+N+S)










class Application2(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        
        master.geometry("800x600+100+100")
        
        self.grid()
        self.master.title("Grid Manager")

        for r in range(30):
            self.master.rowconfigure(r, weight=1)    
        for c in range(5):
            self.master.columnconfigure(c, weight=1)
            Button(master, text="Button {0}".format(c)).grid(row=30,column=c,sticky=E+W)
            
        Frame0 = Frame(master, bg="yellow")
        Frame0.rowconfigure(0, weight=1)
        for i in range(5):
            Frame0.columnconfigure(i, weight=1, pad=0)
        Frame0.grid(row=0, columnspan=5, sticky=N+E+W+S)
        
        
        for c in range(5):
            Button(Frame0, text="Button {0}".format(c)).grid(row=0, column= c, sticky=E+W)

        Frame1 = Frame(master, bg="red")
        Frame1.grid(row = 1, column = 0, rowspan = 10, columnspan = 2, sticky = W+E+N+S) 
        Frame2 = Frame(master, bg="blue")
        Frame2.grid(row = 11, column = 0, rowspan = 19, columnspan = 2, sticky = W+E+N+S)
        Frame3 = Frame(master, bg="green")
        Frame3.grid(row = 1, column = 2, rowspan = 29, columnspan = 3, sticky = W+E+N+S)





app = Application2(master=Tk())
app.mainloop()