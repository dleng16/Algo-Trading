import alpaca_trade_api as tradeapi
import time
import numpy as np
import pandas as pd

import tradealgo.algos as ta

#Feeding in Username, API Passcode
fh = open("../private.txt", "r")
temp = fh.read().split('\n')
api = tradeapi.REST(
    key_id= temp[0],
    secret_key= temp[1],
    base_url='https://paper-api.alpaca.markets'
)

# print(api.get_clock())
# print()
# print(time.clock())
# hi = pd.Timestamp(year=2017, month=1, day=1, hour=12).time()
# print(hi)
# time.localtime()

# avg = 0
# volume_list = []
# bars = api.get_barset('AAPL', '5Min', limit=1000)
# for i in bars["AAPL"]:
# 	volume_list.append(i.v)
# 	avg = avg + i.v
# avg = avg /1000/5
# print(avg)
# print(np.percentile(volume_list, 95)/5)
# print(api.get_barset('AAPL', '1Min', limit=5))

# api.submit_order(
#                 symbol='AAPL',
#                 qty=1,
#                 side='buy',
#                 type='market',
#                 time_in_force='day',
#             )

# clock = api.get_clock()

#print(api.get_asset("AAPL"))

# now = clock.timestamp

# print(now)
# print(clock.is_open)
# #print(api.list_assets())
# pos = api.list_positions()
# print(pos[0])
# print(now.strftime('%Y-%m-%d'))

#a = ['AAPL', 'TSLA']
#bars = api.get_barset(a, '1Min', 5)

#print(bars)
# print(" ")
# print(" ")
# print(bars.df)
#print(bars["AAPL"])
#print(bars)
#print(api)

base = ta.trading_algo(api)

while True:
	clock = api.get_clock()
	if clock.is_open:
		print("")
		base.momentum_with_volume('AAPL')
		#momentum_state_defined(api)
	else:
		#momentum_state_defined(api)
		print("Market Closed " + str(clock.timestamp))
	time.sleep(20)

