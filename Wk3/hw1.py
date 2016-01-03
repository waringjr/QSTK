
#Homework 1; Computational Investing; Coursera 2 Jan 2015
 

# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def simulate(dt_start,dt_end,ls_symbols,weights):
    #function takes a start date, end date, ticker symbols, and 
    #allocations, and calculates the optimal portfolio for 2011

    # We need closing prices so the timestamp should be hours=16.
    dt_timeofday = dt.timedelta(hours=16)

    # Get a list of trading days between the start and the end.
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)

    # Creating an object of the dataaccess class with Yahoo as the source.
    c_dataobj = da.DataAccess('Yahoo')

    # Keys to be read from the data, it is good to read everything in one go.
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    # Reading the data, now d_data is a dictionary with the keys above.
    # Timestamps and symbols are the ones that were specified before.
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    
    # Filling the data for NAN
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    # Getting the numpy ndarray of close prices.
    na_price = d_data['close'].values
    
    #the cumulative return is then:
    cum_returns = sum((na_price[-1,:]/na_price[0,:])*weights)
    
    # Normalizing the prices to start at 1 and see relative returns
    na_normalized_price = na_price / na_price[0, :]
    
    alloc = np.array(weights).reshape(4,1)
    portVal = np.dot(na_normalized_price, alloc)    
    
    # Copy the normalized prices to a new ndarry to find returns.
    na_rets = portVal.copy()
    # Calculate the daily returns of the prices. (Inplace calculation)
    # returnize0 works on ndarray and not dataframes.
    tsu.returnize0(na_rets) 
    
    #these numbers are slightly off...dunno why
    daily_ret = np.mean(na_rets)
    vol = np.std(na_rets)
    sharpe = np.sqrt(252)*daily_ret/vol
    
    return cum_returns,daily_ret,vol,sharpe

def printsim(dt_start,dt_end,ls_symbols,weights):
    
    cum_returns,daily_ret,vol,sharpe = simulate(dt_start,dt_end,ls_symbols,weights)
    
    print "Start Date: ", dt_start
    print "End Date: ", dt_end
    print "Symbols: ", ls_symbols
    print "Optimal Allocations: ", weights
    print "Sharpe Ratio: ", sharpe
    print "Volatility (stdev): ", vol
    print "Average Daily Return: ", daily_ret
    print "Cumulative Return: ", cum_returns


def opt_alloc(dt_start,dt_end,ls_symbols):
    
    #initialize store for max sharpe ratio and allocation
    max_sharpe = -1
    max_alloc = [0.0,0.0,0.0,0.0]
    
    for i in range(0,11):
        for j in range(0,11-i):
            for k in range(0,11-i-j):
                for l in range(0,11-i-j-k):
                    # is this allocation legal?
                    if(i+j+k+l) == 10:
                        alloc = [float(i)/10, float(j)/10, float(k)/10, float(l)/10]
                        cum,daily,vol,sharpe = simulate(dt_start,dt_end,ls_symbols,alloc)

                        if sharpe > max_sharpe:
                            max_alloc = alloc
                            max_sharpe = sharpe
    return max_alloc
                    
