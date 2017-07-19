import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import bytespdate2num
import matplotlib.ticker as mticker
from matplotlib.finance import candlestick_ohlc
from matplotlib import style

import numpy as np
import urllib2

## style.use('fivethirtyeight')


def b2num(fmt, encoding = 'utf-8'):
    strconverter = mdates.strpdate2num(fmt)
    def bytesconverter(b):
        s = b.decode(encoding)
        return strconverter(s)
    return bytesconverter
    

### text and annotation
###
def graph_data(stock):
    
    fig = plt.figure()
    ax1 = plt.subplot2grid((1,1), (0,0) ) 
    
    url = 'http://chartapi.finance.yahoo.com/instrument/1.0/' + stock + '/chartdata;type=quote;range=1m/csv'
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
    candlestick_ohlc(ax1, ohlc, width=0.5, colorup='g', colordown='r')
    
    
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
    
    
#     ## text example font dict
#     font_dict = {'family' : 'serif',
#                  'color' : 'darkred',
#                  'size' : 15}
#     ax1.text(dt[10], clP[1], 'ebay pricing', fontdict=font_dict)
    
 
# ### annotation 
#     ax1.annotate('test annotate', (dt[11],loP[11]), xytext=(0.8, 0.9),
#                  textcoords='axes fraction',
#                  arrowprops = dict(color='blue', width=1) )


### annotate price
    bbox_props = dict(boxstyle='round', fc='w', ec='k')
    ax1.annotate(str(clP[-1]), (dt[-1], clP[-1]), 
                 xytext=(dt[-1]+1, clP[-1]),
                 bbox = bbox_props
                 )



    plt.xlabel('date')
    plt.ylabel('price')
    plt.title('interesting graph')
    ## plt.legend()
    
    
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)    
        
    plt.subplots_adjust(left=0.09, bottom=0.16, right=0.94, top=0.95, wspace=0.2, hspace=0)
    
    plt.show()



if __name__ == '__main__':
    graph_data("ebay")