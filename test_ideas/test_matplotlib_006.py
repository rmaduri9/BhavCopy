import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import bytespdate2num
import matplotlib.ticker as mticker
from matplotlib.finance import candlestick_ohlc
from matplotlib import style

import numpy as np
import urllib2

### style.use('fivethirtyeight')


def b2num(fmt, encoding = 'utf-8'):
    strconverter = mdates.strpdate2num(fmt)
    def bytesconverter(b):
        s = b.decode(encoding)
        return strconverter(s)
    return bytesconverter


MA1 = 10
MA2 = 30

def moving_average(values, window):
    weights = np.repeat(1.0, window) / window
    smas = np.convolve(values, weights, 'valid')
    return smas
    
    
def high_minus_low(highs, lows):
    return highs - lows

def graph_data(stock):
    
    fig = plt.figure()

    plt.title(stock)
    plt.xlabel('date')

    ax1 = plt.subplot2grid((6,1), (0,0), rowspan=1, colspan=1 )
    plt.ylabel("H-L")
    
    ax2 = plt.subplot2grid((6,1), (1,0), rowspan=4, colspan=1 )
    plt.ylabel('Price')    
    
    ax3 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1 )
    plt.ylabel('MAvgs')
    
    url = 'http://chartapi.finance.yahoo.com/instrument/1.0/' + stock + '/chartdata;type=quote;range=1y/csv'
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
    

    ohlc= []
    for i in range(len(dt)):
        ohlc.append( (dt[i], opP[i], hiP[i], loP[i], clP[i], vlP[i]))
    
    
    ma1 = moving_average(clP, MA1)
    ma2 = moving_average(clP, MA2)
    start = len(dt[MA2-1:])
    
    h_l = list(map(high_minus_low, hiP, loP))
    
    
    ax1.plot_date(dt, h_l, '-')
    ax1.yaxis.set_major_locator(mticker.MaxNLocator(nbins=5, prune='lower'))
    
    candlestick_ohlc(ax2, ohlc, width=0.5, colorup='g', colordown='r')




        
### annotate price
    bbox_props = dict(boxstyle='round', fc='w', ec='k')
    ax2.annotate(str(clP[-1]), (dt[-1], clP[-1]), 
                 xytext=(dt[-1]+1, clP[-1]),
                 bbox = bbox_props
                 )




    ax3.plot(dt[-start:], ma1[-start:], linewidth=1)
    ax3.plot(dt[-start:], ma2[-start:], linewidth=1)
    ax3.fill_between(dt[-start:], ma2[-start:], ma1[-start:], where=(ma1[-start:] < ma2[-start:]), facecolor='r')
    ax3.fill_between(dt[-start:], ma2[-start:], ma1[-start:], where=(ma1[-start:] > ma2[-start:]), facecolor='g')
       
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax3.xaxis.set_major_locator(mticker.MaxNLocator(10))
    
    for label in ax3.xaxis.get_ticklabels():
        label.set_rotation(45)   
        
    plt.setp(ax1.get_xticklabels(), visible=False)
    plt.setp(ax2.get_xticklabels(), visible=False)
    plt.subplots_adjust(left=0.09, bottom=0.16, right=0.94, top=0.95, wspace=0.2, hspace=0)
    
    plt.show()
    

if __name__ == '__main__':
    graph_data("ebay")