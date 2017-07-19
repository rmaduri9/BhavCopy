'''
Created on 08-Apr-2017

@author: rmaduri
'''
import tkinter as tk
import tkinter.ttk as ttk
from appFrames import appConst

class FrameRoot(tk.Frame):
    def __init__(self, parent, root):
        tk.Frame.__init__(self, parent)

        
        
        
        self.buttonBar = tk.Frame(self, height = 25, background = "light sea green", relief=tk.RAISED, bd=1)
        self.buttonBar.pack(expand=tk.NO, fill=tk.X)
        
        self.addWidgets(parent, root)
        self.addMenu(root)

        
    def addWidgets(self, parent, root):
        pass

    def addMenu(self, root):
        pass
    
    
    
    
    
    





class StartPage(FrameRoot):
    def __init__(self, parent, rootController):
        FrameRoot.__init__(self, parent, rootController) 
    
    
    
    def addWidgets(self, parent, rootController):
        frm1 = tk.Frame(self, height=800, width=600, background = "light sea green")
        frm1.pack(side="left")
        
        
        
        label = tk.Label(self, text="Start Page", font=appConst.LARGE_FONT)
        #label.pack(pady=10, padx=10)
        label.pack()

        button1 = tk.Button(self, text="PageOne Page", 
                            command=lambda: rootController.show_frame(PageOne))
        button1.pack() 

        self.btnAry = []
        for i in range(10):
            btn = tk.Button(self.buttonBar, text="", width=1, relief=tk.FLAT)
            btn.grid(row=0, column=i)
            self.btnAry.append(btn)   
            

    def addMenu(self, rootController):
        menubar = tk.Menu(rootController)
        
        fileMenu = tk.Menu(menubar, tearoff=0)
        fileMenu.add_command(label="Open", command=lambda: print("Menu Open"))
        fileMenu.add_command(label="Save", command=lambda: print("Menu Save"))
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=rootController.quit)
        menubar.add_cascade(label="File", menu=fileMenu)
        
        
        rootController.config(menu=menubar)
        
    
        
        
        
        
        
        
        
        
class PageOne(FrameRoot): 
    def __init__(self, parent, rootController):
        FrameRoot.__init__(self, parent, rootController)

        
        label = tk.Label(self, text="Visit Page 1", font=appConst.LARGE_FONT)
        label.pack(pady=10, padx=10)
        
        button1 = tk.Button(self, text="Start Page", 
                            command=lambda: rootController.show_frame(StartPage))
        button1.pack() 
        
        self.addMenu(rootController)

    
    def addWidgets(self, parent, root):
        self.btnAry = []
        for i in range(20):
            btn = ttk.Button(self.buttonBar, text="", width=1)
            btn.grid(row=0, column=i)
            self.btnAry.append(btn)   
            
    
    def addMenu(self, rootController):
        menubar = tk.Menu(rootController)
        
        fileMenu = tk.Menu(menubar, tearoff=0)
        fileMenu.add_command(label="Open", command=lambda: print("PageOne Open"))
        fileMenu.add_command(label="Save", command=lambda: print("PageOne Save"))
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=rootController.quit)
        menubar.add_cascade(label="File", menu=fileMenu)
        
        
        rootController.config(menu=menubar) 