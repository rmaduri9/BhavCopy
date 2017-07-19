'''
Created on 16-Apr-2017

@author: rmaduri

import data from internet to graph

http://chartapi.finance.yahoo.com/instrument/1.0/TSLA/chartdata;type=quote;range=1y/csv
'''

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import bytespdate2num
import matplotlib.ticker as mticker
from matplotlib.finance import candlestick_ohlc
from matplotlib import style

import numpy as np
import urllib2


# # print(plt.style.available)
# # builtin styles site-packages/matplotlib/mpl-data/stylelib
# [u'seaborn-darkgrid', 
# u'seaborn-notebook', 
# u'classic', 
# u'seaborn-ticks', 
# u'grayscale', 
# u'bmh', 
# u'seaborn-talk', 
# u'dark_background', 
# u'ggplot', 
# u'fivethirtyeight', 
# u'seaborn-colorblind', 
# u'seaborn-deep', 
# u'seaborn-whitegrid', 
# u'seaborn-bright', 
# u'seaborn-poster', 
# u'seaborn-muted', 
# u'seaborn-paper', 
# u'seaborn-white', 
# u'seaborn-pastel', 
# u'seaborn-dark', 
# u'seaborn', 
# u'seaborn-dark-palette']


# style.use('ggplot')
style.use('fivethirtyeight')


def b2num(fmt, encoding = 'utf-8'):
    strconverter = mdates.strpdate2num(fmt)
    def bytesconverter(b):
        s = b.decode(encoding)
        return strconverter(s)
    return bytesconverter
    


def graph_data(stock):
    
    fig = plt.figure()
    ax1 = plt.subplot2grid((1,1), (0,0) ) 
    
    url = 'http://chartapi.finance.yahoo.com/instrument/1.0/' + stock + '/chartdata;type=quote;range=10y/csv'
    source_code =  urllib2.urlopen(url).read().decode()
    stock_data = []
    split_source = source_code.split('\n')
    
    for line in split_source:
        split_line = line.split(',')
        if len(split_line) == 6:
            if 'values' not in line and 'labels' not in line:
                stock_data.append(line)
    
    dt, clP, hiP, loP, opP, vlP = np.loadtxt(stock_data, 
                                             delimiter=",", 
                                             unpack=True, 
                                             converters = {0:bytespdate2num('%Y%m%d')})
    
###### 
#     # ax1.plot_date(dt, clP, '-', label="test")
#     ax1.fill_between(dt, clP, clP[0], where = (clP > clP[0]), label="tst", facecolor='g', alpha=0.3)
#     ax1.fill_between(dt, clP, clP[0], where = (clP < clP[0]), label="tst", facecolor='r', alpha=0.3)
#     ax1.axhline(clP[0], color='k', linewidth=1)
#     
#     for label in ax1.xaxis.get_ticklabels():
#         label.set_rotation(45)
#     #ax1.grid(True) # , color='g', linestyle='-', linewidth=5)
#     #ax1.xaxis.label.set_color('c')
#     #ax1.yaxis.label.set_color('r')
#     ax1.set_yticks([0,25,50,75])
#     
#     ax1.spines['left'].set_color('c')
#     ax1.spines['right'].set_visible(False)
#     ax1.spines['top'].set_visible(False)
#     ax1.tick_params(axis='x', colors='#f06215')
    
#### ohlc
    ohlc= []
    for i in range(len(dt)):
        ohlc.append( (dt[i], opP[i], hiP[i], loP[i], clP[i], vlP[i]))
    ## candlestick_ohlc(ax1, ohlc, width=0.5, colorup='g', colordown='r')
    
    ax1.plot(dt, clP)
    ax1.plot(dt, opP)
    
    #candlestick_ohlc(ax, quotes, width, colorup, colordown, alpha)
    
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
    
    plt.xlabel('date')
    plt.ylabel('price')
    plt.title('interesting graph')
    plt.legend()
    
    
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)    
        
    plt.subplots_adjust(left=0.09, bottom=0.16, right=0.94, top=0.95, wspace=0.2, hspace=0)
    
    plt.show()



if __name__ == '__main__':
    graph_data("TWTR")