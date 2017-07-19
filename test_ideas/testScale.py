'''
Created on 16-Apr-2017

@author: rmaduri
'''

from tkinter import *


master = Tk()

w = Scale(master, from_=0, to=100)
w.pack()

w = Scale(master, from_=0, to=200, orient=HORIZONTAL)

w.pack()

mainloop()