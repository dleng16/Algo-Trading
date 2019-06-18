import matplotlib
import tradealgo.algos_stats as algos_stats
import alpaca_trade_api as tradeapi
import time
import numpy as np
import pandas as pd
import os.path



#stats = algos_stats.algo_analysis('history/momentum_with_volume-2019-6-14.txt')

fh = open("../private.txt", "r")
temp = fh.read().split('\n')
api = tradeapi.REST(
    key_id= temp[0],
    secret_key= temp[1],
    base_url='https://paper-api.alpaca.markets'
)

ticker = 'AAPL'

stats = algos_stats.algo_simulator(api, 30000, "tesla-modes15")

# noo = pd.Timestamp('2019-06-17 16:00',tz='America/New_York').isoformat()
start = pd.Timestamp(year=2019, month=6, day=12, hour=9, minute = 30)
# startbeta = pd.Timestamp('2019-06-17 15:58',tz='America/New_York').isoformat()
# startbetapoint = pd.Timestamp(year=2019, month=6, day=13, hour=11, minute = 33).isoformat()




# print(api.get_barset(ticker, '1Min', limit=2, end = noo))
# start = start + pd.Timedelta('1 min')
# print(start)
# print(api.get_barset(ticker, '1Min', limit=2, end= startbeta))

# print(api.get_barset(ticker, '1Min', limit=2, ))


#stats.momentum_with_volume('TSLA', start)
stats.mode_based_trading('TSLA',start)