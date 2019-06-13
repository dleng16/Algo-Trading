import alpaca_trade_api as tradeapi
import time
import numpy as np
import pandas as pd

import tradealgo.algos as ta
from tradealgo import misc

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
print(time.clock())
# hi = pd.Timestamp(year=2017, month=1, day=1, hour=12).time()
# print(hi)
print(time.localtime())

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
#                 qty=2156,
#                 side='buy',
#                 type='market',
#                 time_in_force='day',
#             )

# api.submit_order(
#                 symbol='TSLA',
#                 qty=903,
#                 side='buy',
#                 type='market',
#                 time_in_force='day',
#             )
# api.submit_order(
#                 symbol='FB',
#                 qty=1056,
#                 side='buy',
#                 type='market',
#                 time_in_force='day',
#             )
# time.sleep(200)

# clock = api.get_clock()

#print(api.get_asset("AAPL"))

# now = clock.timestamp

# print(now)
# print(clock.is_open)
# #print(api.list_assets())
#pos = api.list_positions()
#print(pos[0])
# print(now.strftime('%Y-%m-%d'))

#a = ['AAPL', 'TSLA']
# bars = api.get_barset("AAPL", '1Min', 5)

# #print(bars)
# # print(" ")
# # print(" ")
# # print(bars.df)
# #print(bars["AAPL"])
# print(bars)
# #print(api)
# print(api.list_orders())
# print(api.get_account().portfolio_value)
# print(len(api.list_positions()))
# print(api.get_barset("AAPL", '1Min', 1)["AAPL"][0].c)

# f = open("work.txt", "a")
# f.write("record")
# f.close()

# last = api.get_barset("AAPL", '1Min', 1)
# current_time = time.localtime()
# file_string = str(time.localtime().tm_year) + "-" + str(time.localtime().tm_mon) + "-" + str(time.localtime().tm_mday) + ".txt"
# f = open(file_string, "a")
# f.write(str(current_time.tm_hour)+" "+str(current_time.tm_min)+" "+str(last["AAPL"][0].c) + api.get_account().portfolio_value + "\n")
# f.flush()
# f.close
# r = open(file_string, "r")
# print(r.read())

# file_string = str(time.localtime().tm_year) + "-" + str(time.localtime().tm_mon) + "-" + str(time.localtime().tm_mday) + ".txt"
# f = open(file_string, 'a')
# f.close()

# for i in api.list_positions():
# 	print(i.qty)


to_email = 'avilesov@usc.edu' 
subject = 'OMG Super Important Message'  
body = 'You'
filename = 'work.txt'

# try:
misc.emailing_package(to_email, subject, body, filename)
# except: 
# 	print("Email not sent.")
#_______________________
base = ta.trading_algo(api)

while True:
	clock = api.get_clock()
	check_time = time.localtime()

	if clock.is_open:
		print("")
		base.momentum_with_volume('AAPL', True)
		#base.momentum_trade()

	else:
		hours = check_time.tm_hour - 8
		if(hours < 0):
			hours = hours +24
		if(hours == 23 and check_time.tm_min == 28): #market just closed
			to_email = 'avilesov@usc.edu'
			subject = base.algo_name
			body = "Variable Info of " + base.algo_name + " algorithm"
			filename = str(time.localtime().tm_year) + "-" + str(time.localtime().tm_mon) + "-" + str(time.localtime().tm_mday) + ".txt"
			filename = base.algo_name + "-" + str(time.localtime().tm_year) + "-" + str(time.localtime().tm_mon) + "-" + str(time.localtime().tm_mday) + ".txt"
			misc.emailing_package(to_email, subject, body, filename)



		print("Market Closed " + str(clock.timestamp))
	time.sleep(59)

#hours = check_time.tm_hour - 8
# if(hours < 0):
# 	hours = hours +24
#l
	