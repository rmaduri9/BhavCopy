'''
Created on 08-Apr-2017

@author: rmaduri
'''

import tkinter as tk
import tkinter.ttk as ttk
from appFrames import allFrames



APP_PAGES = (allFrames.StartPage, allFrames.PageOne)

class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self._root = self
        tk.Tk.geometry(self, "%dx%d+0+0" % (tk.Tk.winfo_screenwidth(self), tk.Tk.winfo_screenheight(self)))

        container = tk.Frame(self._root)
        
        container.pack(side="top", fill="both", expand=True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for F in APP_PAGES:
            frame = F(container, self._root)
            frame.grid(row=0, column=0, sticky = tk.NSEW)
            #frame.pack(side="top", fill="both", expand=True)
            self.frames[F] = frame
        
        self.show_frame(APP_PAGES[0])
        
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()



    
app = Application()
app.mainloop()