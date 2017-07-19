'''
Created on 08-Apr-2017

@author: rmaduri
'''
import tkinter as tk
import tkinter.ttk as ttk
import sys

class bhavCopy(tk.Frame):
    
    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.root = root
        self.createWidgets()
        print(self.config())

        self.mainloop()
        

    def cmdOpen(self):
        pass
    
    def cmdExit(self):
        self.root.destroy()
        
    def createMenubar(self):
        menubar = tk.Menu(self.root)
        fileMenu = tk.Menu(menubar, tearoff=0)
        fileMenu.add_command(label="Open", command=self.cmdOpen)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self.cmdExit)
        menubar.add_cascade(label="File", menu=fileMenu)
        
        self.root.config(menu = menubar)
    
    
    def createFrameWidget(self):
        shortcutbar = tk.Frame(self.root, height=25, bg="light sea green")
        btnLoadNew = ttk.Button(shortcutbar, text="Space").pack()
        shortcutbar.pack(expand=tk.NO, fill=tk.X)
        pass
    
    def createWidgets(self):
        self.createMenubar()
        self.createFrameWidget()
        
        
        
bhavCopy(tk.Tk())