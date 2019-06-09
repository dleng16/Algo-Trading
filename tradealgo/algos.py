import alpaca_trade_api as tradeapi
import time
import numpy as np
import pandas as pd

class trading_algo:

	def __init__(self, api, safety = True):
		self.api = api #api class from alpaca markets
		self.safety = safety

	def print_info(self):
		print("Now in tradealgo package")
		

	def sell_all(self):
		for i in self.api.list_positions():
				self.api.submit_order(
	                symbol=i.symbol,
	                qty=i.qty,
	                side='sell',
	                type='market',
	                time_in_force='day',
	            )

	def momentum_trade(self):

		#take the convolution of the last three minutes with a weighted array
		bars = self.api.get_barset('AAPL', '1Min', 3)
		start =  bars["AAPL"][0].c
		last_five_min_open = []
		convolution_list = [.25,.25,.5]
		for i in range(3):
			last_five_min_open.append((bars["AAPL"][i].c)*convolution_list[i])
		avg = sum(last_five_min_open)

		#if the average sum of weighted array is greater than price 3 minutes ago, buy, else sell all
		if(avg > start):
			print("Buy 1 " + str(start) + " " + str(avg))
			self.api.submit_order(
	                symbol='AAPL',
	                qty=150,
	                side='buy',
	                type='market',
	                time_in_force='day',
	            )
		else:
			print("Sell All " + str(start) + " " + str(avg))
			sell_all()

	def momentum_state_defined(self):
		check_time = time.localtime()
		if(check_time.tm_hour == 9-3 and check_time.tm_min == 30):
		 	print("Stock Market Opened!")
		 	momentum_up_state = self.api.get_barset('AAPL', '1min', 1)


	def momentum_with_volume(self, ticker):

		#get avg volume of last 1000 minutes
		avg_vol_hist = 0
		volume_list = []
		bars = self.api.get_barset(ticker, '1Min', limit=1000)
		for i in bars[ticker]:
			volume_list.append(i.v)
			avg_ = avg_vol_hist + i.v
		avg_vol_hist = avg_vol_hist / 1000
		vol_percentile_threshold = np.percentile(volume_list, 90) # 90 percentile of volume


		bars = self.api.get_barset(ticker, '1Min', limit=3)

		#volume last three minutes
		start_vol = bars[ticker][0].o
		avg_vol = 0
		for i in bars[ticker]:
			avg_vol = avg_vol + i.v 
		avg_vol = avg_vol / 3

		#stock price last three minutes
		start_price =  bars[ticker][0].o
		last_three_min_open = []
		convolution_list = [.25,.25,.5]
		for i in range(3):
			last_three_min_open.append((bars[ticker][i].c)*convolution_list[i])
		avg_price = sum(last_three_min_open)

		#stock price last three minutes
		bars = self.api.get_barset(ticker, '1Min', limit=5)
		start_price_five =  bars[ticker][0].o
		last_five_min_open = []
		convolution_list = [.2,.2,.2,.2,.2]
		for i in range(5):
			last_five_min_open.append((bars[ticker][i].c)*convolution_list[i])
		avg_price_five = sum(last_five_min_open)

		#current volume
		current_volume = bars[ticker][4].v

		#submit buy
		if(((current_volume > vol_percentile_threshold) and (avg_price > start_price)) or ((current_volume > avg_vol) and (avg_price > start_price))): 
			print("Buy " + str(start_price) + " " + str(bars[ticker][4].c))
			self.api.submit_order(
	                symbol=ticker,
	                qty=150,
	                side='buy',
	                type='market',
	                time_in_force='day',
	            )
	  	#submit sell
		if(((current_volume > vol_percentile_threshold) and (avg_price_five < start_price_five)) or ((current_volume > avg_vol) and (avg_price_five < start_price_five))):
			print("Sell " + str(start_price) + " " + str(bars[ticker][4].c))
			sell_all()		

		#print("avg_price_five: " + str(avg_price_five) + " start_five" + str(start_price_five))	











		bars = self.api.get_barset(ticker, '1Min', 1)

