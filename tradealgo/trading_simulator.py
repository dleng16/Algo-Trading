import matplotlib
import matplotlib.pyplot as plt
import tradealgo.algos_stats as algos_stats
import alpaca_trade_api as tradeapi
import time
import numpy as np
import pandas as pd
import os.path
import math


#second based simulator

class trading_simulator:

	def __init__(self, buyingpower = 30000, algoname = "default"):
		self.safety = True
		self.buyingpower = buyingpower #total cash in account
		self.portfolio_value = buyingpower #portfolio value
		self.stocks = {}
		self.algoname = algoname
		self.order_flag = "hold"

	def pipline(self, function, ticker, start_date, end_date, data, resolution, safety = True, record = False): #dates have to be in panda timestamp form
		date = start_date
		filename = "history/" + self.algoname + ":" + self.pipline.__name__ + ":" + function.__name__ + ":" + str(start_date) + "-" + str(end_date) + ".txt"
 
		if(date.hour <= 9 and date.minute <= 30):
			date += pd.Timedelta('9 hours') + pd.Timedelta('30 minutes')
			if safety:
				pass



		while(date.year != end_date.year or date.month != end_date.month or date.day != end_date.day or date.hour != 16+4): #unix time now
			if(date.isoweekday() < 6):
				# try:
				algo_vars, data_vars = function(ticker, date, data)
				# except:
				# 	print("Failed on this date: " + str(date))
			date = self.time_simulator(date, resolution)

	def time_simulator(self, time, time_delta):
		time = time + pd.Timedelta('1 min')
		return time

	def buy(self, ticker, current_price, num_stocks = .25):
		num_stocks = math.floor((self.portfolio_value*num_stocks)/current_price)
		if(self.buyingpower - current_price*num_stocks < 0):
			pass
		else:
			self.buyingpower = self.buyingpower - num_stocks*current_price
			self.stocks[ticker] = self.stocks[ticker] + num_stocks
			self.order_flag = "buy"
		self.portfolio_value = self.buyingpower + self.stocks[ticker]*current_price

	def sell(self, ticker, current_price, num_stocks = .25):
		num_stocks = math.floor((self.portfolio_value*num_stocks)/current_price)
		if(self.stocks[ticker] != 0):
			if(self.stocks[ticker] < num_stocks):
				self.sell_all(ticker, current_price)
			else:
				self.buyingpower = self.buyingpower + current_price*num_stocks
				self.stocks[ticker] -= num_stocks
				self.order_flag = "sell"
		self.portfolio_value = self.buyingpower + self.stocks[ticker]*current_price

	def sell_all(self, ticker, current_price):
		if(self.stocks[ticker] != 0):
			self.buyingpower = self.buyingpower + current_price*self.stocks[ticker]
			self.stocks[ticker] = 0
			self.order_flag = "sell"
		self.portfolio_value = self.buyingpower + self.stocks[ticker]*current_price

	def momentum_function(self, ticker, data, n_seconds = 10, lag = 0):
		self.stocks[ticker] = 0
		count = 0
		history = []
		for i in range(len(data)):
			last_n_seconds = []
			time_pd = pd.to_datetime(data[i]['unix_time'], unit='ms')
			if (time_pd.hour >= 9 or time_pd.minute >= 45) and (time_pd.hour != 19 or time_pd.minute <=45):
				for j in range(1,n_seconds+1,1):
					last_n_seconds.append(data[i-j]['price'])
					last_n_seconds.reverse()
				x = np.linspace(1, n_seconds, n_seconds)
				regression = np.polyfit(x, last_n_seconds, 1)
				#if (abs(data[i]['price'] - data[i-1]['price']) < 0.3 ):
				if regression[0] > 0:
					self.buy(ticker, data[i+lag]['price'])
				else:
					self.sell_all(ticker, data[i+lag]['price'])
				#print(str(self.portfolio_value) + " " + str(data[i]['price']) + " " + self.order_flag + " "+str(pd.to_datetime(data[i]['unix_time'], unit='ms')))
				history.append(self.portfolio_value)
			else:
				self.sell_all(ticker, data[i+lag]['price'])
			count += 1
		#print("n_seconds: " + str(n_seconds) + " Balance: " + str(self.portfolio_value) + " " + str(self.momentum_function.__name__))
		plt.figure(0)
		N = len(history)
		x = np.linspace(0.0, 1.0, N)
		plt.plot(x, history)
		print(len(history))

	def recursive_momentum_function(self, ticker, data, n_seconds = 10, lag = 0):
		self.stocks[ticker] = 0
		count = 0
		history = []
		for i in range(len(data)):
			decision = 0
			last_n_seconds = []
			time_pd = pd.to_datetime(data[i]['unix_time'], unit='ms')
			if (time_pd.hour >= 9 or time_pd.minute >= 45) and (time_pd.hour != 19 or time_pd.minute <=45):
				for k in range(2, n_seconds+1,1):
					for j in range(1, k+1, 1):
						last_n_seconds = []
						last_n_seconds.append(data[i-j]['price'])
						last_n_seconds.reverse()
					x = np.linspace(1, k, len(last_n_seconds))
					regression = np.polyfit(x, last_n_seconds, 1)
					if regression[0] > 0:
						decision += 1
					else:
						decision -= 1
				if decision > 0:
					self.buy(ticker, data[i+lag]['price'])
				else:
					self.sell_all(ticker, data[i+lag]['price'])
				#print(str(self.portfolio_value) + " " + str(data[i]['price']) + " " + self.order_flag + " "+str(pd.to_datetime(data[i]['unix_time'], unit='ms')))
				history.append(self.portfolio_value)
			else:
				self.sell_all(ticker, data[i+lag]['price'])
			count += 1
		#print("n_seconds: " + str(n_seconds) + " Balance: " + str(self.portfolio_value) + " " + str(self.momentum_function.__name__))
		plt.figure(0)
		N = len(history)
		x = np.linspace(0.0, 1.0, N)
		plt.plot(x, history)
		print(len(history))


	def reverse_momentum_function(self, ticker, data, n_seconds = 10, lag = 0):
		self.stocks[ticker] = 0
		count = 0
		history = []
		for i in range(len(data)):
			last_n_seconds = []
			time_pd = pd.to_datetime(data[i]['unix_time'], unit='ms')
			if (time_pd.hour >= 9 or time_pd.minute >= 45) and (time_pd.hour != 19 or time_pd.minute <=45):
				for j in range(1,n_seconds+1,1):
					last_n_seconds.append(data[i-j]['price'])
				x = np.linspace(1, n_seconds, n_seconds)
				regression = np.polyfit(x, last_n_seconds, 1)
				#if (abs(data[i]['price'] - data[i-1]['price']) < 0.3 ):
				if regression[0] > 0:
					self.buy(ticker, data[i+lag]['price'])
				else:
					self.sell_all(ticker, data[i+lag]['price'])
				#print(str(self.portfolio_value) + " " + str(data[i]['price']) + " " + self.order_flag + " "+str(pd.to_datetime(data[i]['unix_time'], unit='ms')))
				history.append(self.portfolio_value)
			else:
				self.sell_all(ticker, data[i+lag]['price'])
			count += 1
		print("n_seconds: " + str(n_seconds) + " Balance: " + str(self.portfolio_value) +  " " + str(self.reverse_momentum_function.__name__))
		plt.figure(0)
		N = len(history)
		x = np.linspace(0.0, 1.0, N)
		plt.plot(x, history)
		print(len(history))

	def momentum_function_quick_sell(self, ticker, data, n_seconds = 10, quick_sell_seconds = 5, lag = 0):
		self.stocks[ticker] = 0
		count = 0
		history = []
		for i in range(len(data)):
			last_n_seconds = []
			quick_sell_list = []
			time_pd = pd.to_datetime(data[i]['unix_time'], unit='ms')
			if (time_pd.hour >= 9 or time_pd.minute >= 45) and (time_pd.hour != 19 or time_pd.minute <=45):
				
				for j in range(1,n_seconds+1,1): #look back behind you
					last_n_seconds.append(data[i-j]['price'])
					last_n_seconds.reverse()
				x = np.linspace(1, n_seconds, n_seconds)
				regression = np.polyfit(x, last_n_seconds, 1)
				#if (abs(data[i]['price'] - data[i-1]['price']) < 0.3 ):
				
				quick_sell_list = last_n_seconds[0:quick_sell_seconds]
				x = np.linspace(1, quick_sell_seconds, len(quick_sell_list))
				regression_quick = np.polyfit(x, quick_sell_list, 1)

				if regression[0] < 0 or regression_quick[0] < 0:
					self.sell_all(ticker, data[i+lag]['price'])
				else:	
					self.buy(ticker, data[i+lag]['price'])
				#print(str(self.portfolio_value) + " " + str(data[i]['price']) + " " + self.order_flag + " "+str(pd.to_datetime(data[i]['unix_time'], unit='ms')))
				history.append(self.portfolio_value)
			else:
				self.sell_all(ticker, data[i+lag]['price'])
			count += 1
		print("n_seconds: " + str(n_seconds) + " Balance: " + str(self.portfolio_value))
		plt.figure(0)
		N = len(history)
		x = np.linspace(0.0, 1.0, N)
		plt.plot(x, history)

	# def momentum_function(self, ticker, data, n_seconds = 10, lag = 0):
	# self.stocks[ticker] = 0
	# count = 0
	# for i in range(len(data)):
	# 	last_n_seconds = []
	# 	time_pd = pd.to_datetime(data[i]['unix_time'], unit='ms')
	# 	if time_pd.hour >= 13 and time_pd.minute >= 40:
	# 		for j in range(1,n_seconds+1,1):
	# 			last_n_seconds.append(data[i-j]['price'])
	# 		x = np.linspace(1, n_seconds, n_seconds)
	# 		regression = np.polyfit(x, last_n_seconds, 1)
	# 		if regression[0] > 0:
	# 			self.buy(ticker, data[i+lag]['price'])
	# 		else:
	# 			self.sell_all(ticker, data[i+lag]['price'])
	# 		print(str(self.ledger) + " " + self.order_flag + " "+str(data[i]['unix_time']))
	# 	count += 1




