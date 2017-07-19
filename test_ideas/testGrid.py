'''
Created on 09-Apr-2017

@author: rmaduri
'''

import tkinter as tk
import tkinter.ttk as ttk



class Example(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        
        self.parent = parent
        self.genUI()

    def genUI(self):
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)
                
        self.parent.title("Test Grid 10")
        
        
        
        
        
        
        self.fbtn = tk.Frame(self.parent, relief = tk.constants.RAISED, background="green", height=30)
        self.fbtn.pack(fill=tk.X)
        
        self.frest = tk.Frame(self.parent, relief = tk.constants.RAISED, background="blue")
        self.frest.pack(fill=tk.BOTH, expand=True)
        
        self.ft1 = tk.Frame(self.frest, relief=tk.constants.RAISED, background="black", height=30)
        self.ft1.pack(fill=tk.X)
        

def main():
  
    root = tk.Tk()
    root.geometry("350x300+300+300")
    app = Example(root)
    root.mainloop()  


if __name__ == '__main__':
    main() 
    
    