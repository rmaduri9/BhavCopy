'''
Created on 16-Apr-2017

@author: rmaduri
'''

import matplotlib.pyplot as plt
import csv
import random
import numpy as np


random.random()

# ### line plot
# x = [1,2,3,4,5]
# y = [432,54,1456,45, 443]
# x2 = [1,2,3,4,5]
# y2 = [32,443,43,65,23]
# 
# plt.plot(x,y, label='1st Line')
# plt.plot(x2,y2, label='2nd Line')


# ### bar graph
# x = [2,4,6,8,10]
# y = [6,7,8,2,4]
# x2 = [1,3,5,7,9]
# y2 = [7,8,2,4,2]
#   
# plt.bar(x,y,label="bars 1", color="r")
# plt.bar(x2,y2, label="bars 2", color="c")


# ### bar graph 
# pop_ages = [22,55,62,45,21,22,98, 78, 43, 65, 99, 102, 125, 127, 121, 123, 34,42,42,4,9,99,102,110,120,21,3,44,54,65,76,87,65,49]
# ids = [x for x in range(len(pop_ages))]
# plt.bar(ids, pop_ages, label="test")


# ### histogram 
# pop_ages = [22,55,62,45,21,22,98, 78, 43, 65, 99, 102, 125, 127, 121, 123, 34,42,42,4,9,99,102,110,120,21,3,44,54,65,76,87,65,49]
# ids = [x for x in range(len(pop_ages))]
# bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130]
# plt.hist(pop_ages, bins, histtype='bar', rwidth=0.8, label="x")
#  

# ### scatter plot
# r = 10
# x = [random.randint(1,10) for i in range(r)]
# y = [random.randint(1,10) for i in range(r)]
# plt.scatter(x, y, label="scatter", color='k')


# ### stack plot
# days = [1,2,3,4,5]
# 
# sleep = [7,8,6,11,7]
# eating= [2,3,4,3,2]
# working=[7,8,7,2,2]
# playing=[8,5,7,8,13]
# 
# plt.plot([], [], color='m', label='sleep')
# plt.plot([], [], color='r', label='eat')
# plt.plot([], [], color='y', label='work')
# plt.plot([], [], color='g', label='play')
# 
# plt.stackplot(days, sleep, eating, working, playing, colors=['m', 'r', 'y', 'g'])


# ### pie chart
# days = [1,2,3,4,5]
#  
# sleep = [7,8,6,11,7]
# eating= [2,3,4,3,2]
# working=[7,8,7,2,2]
# playing=[8,5,7,8,13]
# 
# activities = (sleep, eating, working, playing)
# 
# slices = [x[4] for x in activities]
# lbl_activities = ('sleep', 'eat', 'work', 'play')
# 
# plt.pie(slices, labels=lbl_activities)


### load data from csv
x = []
y = []
## part 1 : using csv module
# with open("/users/rmaduri/downloads/test.csv", 'r') as csvfile:
#     plots = csv.reader(csvfile, delimiter=",")
#     for row in plots:
#         x.append(int(row[0]))
#         y.append(int(row[1]))

### part 2 : using numpy
x, y = np.loadtxt("/users/rmaduri/downloads/test.csv", delimiter=",", unpack=True)
    
plt.plot(x, y, label="test")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.title("Graph")



plt.show()