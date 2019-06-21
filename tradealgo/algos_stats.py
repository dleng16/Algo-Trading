from matplotlib import pyplot as plt
import matplotlib.ticker
import pandas as pd
import os.path
import numpy as np






class algo_analysis:

	def __init__(self):
		self. safety = True



	def file_input_processing(self, file):
		self.file = file
		f = open(file, 'r')
		line_text = None
		data = []
		self.variables = None

		line = f.readline()
		self.variables = line.split()

		line = f.readline()
		for i in line.split():
			temp = []
			temp.append(float(i))
			data.append(temp)
		while line:
			line = f.readline()
			line = line.split()
			for i in range(len(line)):
				data[i].append(float(line[i]))

		data[0] = [60*int(i) for i in data[0]]
		data[0] = [data[0][i] + int(data[1][i]) for i in range(len(data[0]))] # convert hours and minutes to total minutes of day (combine data)

		#data[0] = 60*data[0] + data[1]
		#data = float(data)
		j = 0
		for i in data:
			plt.figure(j)
			plt.plot(data[0], i)
			plt.xlabel(self.variables[j])
			#axes = plt.axes()
			#axes.get_xaxis().get_major_formatter().set_useOffset(False)
			plt.locator_params(axis='y', nbins=20)
			print(self.variables[j])
			j = j + 1


		plt.show()







class algo_simulator:

	def __init__(self, api, buyingpower = 30000, algoname = "default"):
		self.safety = True
		self.api = api
		self.buyingpower = buyingpower #total cash in account
		self.ledger = None
		self.stocks = {}
		self.algoname = algoname
		self.order_flag = "hold"

	def minute_simulator(self, time):
		time = time + pd.Timedelta('1 min')
		return time

	def buy(self, ticker, current_price, num_stocks = 50):
		if(self.buyingpower - current_price*num_stocks < 0):
			pass
		else:
			self.buyingpower = self.buyingpower - num_stocks*current_price
			self.stocks[ticker] = self.stocks[ticker] + num_stocks
			self.order_flag = "buy"

	def sell(self, ticker, current_price, num_stocks = 50):
		if(self.stocks[ticker] == 0):
			pass
		else:
			self.buyingpower = self.buyingpower + current_price*num_stocks
			self.stocks[ticker] -= num_stocks
			self.order_flag = "sell"

	def record_stats(self, file_name, variable_list, data_list):
		if os.path.isfile(file_name) != True:
			f = open(file_name, 'w')
		f = open(file_name, 'r')
		if f.read(1):
			f = open(file_name, 'a')   
		else:
			f = open(file_name, 'a')
			f.write(' '.join(variable_list))
			f.write('\n')
		f = open(file_name, 'a')
		f.write(' '.join(map(str,data_list)))
		f.write('\n')
		f.flush()
		f.close()

	def recursive_regression_trading(self, ticker, starting_time):

		algo_variables = ['time', 'stock-price', 'decision', 'number-of-stocks', 'portfolio-value']

		if ticker in self.stocks.keys():
			pass
		else:
			self.stocks[ticker] = 0

		if(starting_time.hour == 16):
			pass
		else:
			time = pd.Timestamp(starting_time, tz='America/New_York').isoformat()

			order = 6

			bars = self.api.get_barset(ticker, '1Min', limit=order, end = time)
			# data = []
			# for i in range(order):
			# 	data.append((bars[ticker][i].c))

			current_price = bars[ticker][order-1].c

			#regression analyze current direction
			regression_analysis = []
			for i in range(1,order,1):
				x = [j for j in range(order, order-1-i, -1)]
				y = []
				for j in range(i+1):
					y.append(bars[ticker][order-j-1].c)
				regression_analysis.append(np.poly1d(np.polyfit(x, y, 1)))

			decision = 0
			for i in regression_analysis:
				if(i(order+1) > current_price):
					decision += 1
				else:
					decision -= 1

			print(decision)
			if(decision < 0):
				self.buy(ticker, current_price)
			else:
				self.sell(ticker, current_price)

			self.ledger = self.buyingpower + self.stocks[ticker]*current_price

			#record stats
			file_string = "history/" + self.algoname + self.recursive_regression_trading.__name__ + "-" + str(starting_time.year) + "-" + str(starting_time.month) + "-" + str(starting_time.day) + ".txt"
			data = [starting_time.hour*60 + starting_time.minute, current_price, decision, self.stocks[ticker], self.ledger]
			
			self.record_stats(file_string, algo_variables, data)

			
			starting_time = self.minute_simulator(starting_time)

			#debugger/logger
			print(starting_time)
			print(str(self.ledger) + " " + str(self.buyingpower) + " " + str(self.stocks[ticker]) + " " + self.order_flag)

			#recursive call until end of stock market
			self.recursive_regression_trading(ticker, starting_time)


	def momentum_with_volume(self, ticker, starting_time):

		self.algo_variables = ['time-hour', 'stock-price', 'avg-price-3-min', 'avg-price-5-min', 'average-volume', 'current-volume', 'number-of-stocks', 'portfolio-value']

		if ticker in self.stocks.keys():
			pass
		else:
			self.stocks[ticker] = 0

		if(starting_time.hour == 16):
			pass
		else:
			time = pd.Timestamp(starting_time, tz='America/New_York').isoformat()

			bars = self.api.get_barset(ticker, '1Min', limit=3, end = time)
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
			bars = self.api.get_barset(ticker, '1Min', limit=3, end = time)
			start_price_three=  bars[ticker][0].o
			last_three_min_open = []
			convolution_list = [.3333,.3333,.3333]
			for i in range(3):
				last_three_min_open.append((bars[ticker][i].c)*convolution_list[i])
			avg_price_three = sum(last_three_min_open)

			#stock price last three minutes
			bars = self.api.get_barset(ticker, '1Min', limit=3, end = time)
			start_price_two=  bars[ticker][0].o
			last_two_min_open = []
			convolution_list = [.5,.5]
			for i in range(2):
				last_two_min_open.append((bars[ticker][i].c)*convolution_list[i])
			avg_price_two = sum(last_two_min_open)

			#stock price last five minutes
			bars = self.api.get_barset(ticker, '1Min', limit=5, end = time)
			start_price_five =  bars[ticker][0].o
			last_five_min_open = []
			convolution_list = [.2,.2,.2,.2,.2]
			for i in range(5):
				last_five_min_open.append((bars[ticker][i].c)*convolution_list[i])
			avg_price_five = sum(last_five_min_open)

			#current volume
			current_volume = bars[ticker][4].v
			current_price = bars[ticker][4].c


			order_flag = "hold"

			#submit sell
			#if(((current_volume > vol_percentile_threshold) and (avg_price_five < start_price_five)) or ((current_volume > avg_vol) and (avg_price_five < start_price_five))):
			if(((current_volume > avg_vol) and (avg_price > start_price))): 
				print("Sell " + str(start_price) + " " + str(bars[ticker][4].c))
				#if(self.api.list_positions().length() = 0):
				self.buyingpower = self.buyingpower + current_price*self.stocks[ticker]
				self.stocks[ticker] = 0
				order_flag = "sell"

			#submit buy
			if(order_flag != "sell"):
				if(avg_price_two < start_price_two):
					print("Buy " + str(start_price) + " " + str(bars[ticker][4].c))
					self.buyingpower = self.buyingpower - 25*current_price
					self.stocks[ticker] = self.stocks[ticker] + 25
					order_flag = "buy"


			self.ledger = self.buyingpower + self.stocks[ticker]*current_price

			#record stats
			file_string = "history/" + self.algoname + "-" + str(starting_time.year) + "-" + str(starting_time.month) + "-" + str(starting_time.day) + ".txt"
			if os.path.isfile(file_string) != True:
				f = open(file_string, 'w')
			f = open(file_string, 'r')

			if f.read(1):
				f = open(file_string, 'a')   
			else:
				f = open(file_string, 'a')
				for i in self.algo_variables:
					f.write(i + " ")

			f.write(str(starting_time.hour*60 + starting_time.minute)+" "+str(current_price) + " "+str(avg_price) +" "+ str(avg_price_five) +" "+ str(avg_vol) +" "+ str(current_volume) +" "+ str(self.stocks[ticker]) + " " + str(self.ledger) + "\n")
			f.flush()
			f.close()
			
			


			#debugger/logger
			starting_time = self.minute_simulator(starting_time)
			print(starting_time)
			print(str(self.ledger) + " " + str(self.buyingpower) + " " + str(self.stocks[ticker]) + " " + order_flag)

			#recursive call until end of stock market
			self.momentum_with_volume(ticker, starting_time) 


	def mode_based_trading(self, ticker, starting_time):

		self.algo_variables = ['time-hour', 'stock-price', 'avg-price-5-min', 'regression-coef', 'number-of-stocks', 'portfolio-value']

		if ticker in self.stocks.keys():
			pass
		else:
			self.stocks[ticker] = 0

		if(starting_time.hour == 16):
			pass
		else:
			time = pd.Timestamp(starting_time, tz='America/New_York').isoformat()

			bars = self.api.get_barset(ticker, '1Min', limit=5, end = time)
			last_five_min_open = []
			convolution_list = [.2,.2,.2,.2,.2]
			for i in range(5):
				last_five_min_open.append((bars[ticker][i].c)*convolution_list[i])
			avg_price_five = sum(last_five_min_open)
			current_price = bars[ticker][4].c

			#regression analyze current direction
			bars = self.api.get_barset(ticker, '1Min', limit=10, end = time)
			x = [i for i in range(10)]
			y = [j.c for j in bars[ticker]]
			z = np.polyfit(x, y, 1)


			#bars_eight = self.api.get_barset(ticker, '1Min', limit=8, end = time)

			order_flag = "hold"

			print(current_price)

			#submit sell
			#if(((current_volume > vol_percentile_threshold) and (avg_price_five < start_price_five)) or ((current_volume > avg_vol) and (avg_price_five < start_price_five))):
			# if(z[0] >= 0.009):
			# 	if(current_price >= avg_price_five): 
			# 		#print("Sell " + str(start_price) + " " + str(bars[ticker][4].c))
			# 		#if(self.api.list_positions().length() = 0):
			# 		if(self.stocks[ticker] == 50):
			# 					pass
			# 		else:
			# 			self.buyingpower = self.buyingpower - 50*current_price
			# 			self.stocks[ticker] = self.stocks[ticker] + 50
			# 			order_flag = "buy"
			# 		# print("hi")
			# else:
			if(current_price >= avg_price_five): 
				#print("Sell " + str(start_price) + " " + str(bars[ticker][4].c))
				#if(self.api.list_positions().length() = 0):
				self.buyingpower = self.buyingpower + current_price*self.stocks[ticker]
				self.stocks[ticker] = 0
				order_flag = "sell"
				# print("hi")
			else:
				#print("Buy " + str(start_price) + " " + str(bars[ticker][4].c))
				# print("HHH")
				# print(abs(bars[ticker][4].c-avg_price_five))
				# print("HHH")
				# self.buyingpower = self.buyingpower - 25*current_price
				# self.stocks[ticker] = self.stocks[ticker] + 25
				# order_flag = "buy"
				#if(z[0] < 0.009 or z[0] > -0.009436/2):
				if(z[0] > 0):
					if((abs(bars[ticker][4].c-avg_price_five) <.40)):
						if(self.stocks[ticker] == 50):
							pass
						else:
							self.buyingpower = self.buyingpower - 50*current_price
							self.stocks[ticker] = self.stocks[ticker] + 50
							order_flag = "buy"
					else:
						self.buyingpower = self.buyingpower + current_price*self.stocks[ticker]
						self.stocks[ticker] = 0
						order_flag = "sell"
				else:
					self.buyingpower = self.buyingpower + current_price*self.stocks[ticker]
					self.stocks[ticker] = 0
					order_flag = "sell"



			self.ledger = self.buyingpower + self.stocks[ticker]*current_price

			#record stats
			file_string = "history/" +self.algoname + "-" + str(starting_time.year) + "-" + str(starting_time.month) + "-" + str(starting_time.day) + ".txt"
			if os.path.isfile(file_string) != True:
				f = open(file_string, 'w')
			f = open(file_string, 'r')

			if f.read(1):
				f = open(file_string, 'a')   
			else:
				f = open(file_string, 'a')
				for i in self.algo_variables:
					f.write(i + " ")

			f.write(str(starting_time.hour*60 + starting_time.minute)+" "+str(current_price) +" "+ str(avg_price_five) +" "+ str(z[0]) + " " + str(self.stocks[ticker]) + " " + str(self.ledger) + "\n")
			f.flush()
			f.close()
			
			


			#debugger/logger
			starting_time = self.minute_simulator(starting_time)
			print(starting_time)
			print(str(self.ledger) + " " + str(self.buyingpower) + " " + str(self.stocks[ticker]) + " " + order_flag)
			print(str(z[0]) + " " + str(z[1]))

			#recursive call until end of stock market
			self.mode_based_trading(ticker, starting_time) 




	def delayed_volume_price_trading(self, ticker, starting_time):

		self.algo_variables = ['time', 'stock-price', 'current-volume','avg-price-5-min', 'avg-price-10-5-min', 'avg-vol-10-min', 'avg-vol-20-10-min', 'number-of-stocks', 'portfolio-value']

		if ticker in self.stocks.keys():
			pass
		else:
			self.stocks[ticker] = 0

		if(starting_time.hour == 16):
			pass
		else:
			time = pd.Timestamp(starting_time, tz='America/New_York').isoformat()

			bars = self.api.get_barset(ticker, '1Min', limit=10, end = time)
			last_five_ten_min_open = []
			for i in range(5):
				last_five_ten_min_open.append((bars[ticker][i].c))
			avg_price_five_ten = sum(last_five_ten_min_open)/5

			price_five_min_ago = bars[ticker][4].c

			last_five_min_open = []
			for i in range(5):
				last_five_min_open.append((bars[ticker][i+5].c))
			avg_price_five = sum(last_five_min_open)/5

			current_price = bars[ticker][9].c

			bars = self.api.get_barset(ticker, '1Min', limit=20, end = time)
			last_20_10_min_open_vol = []
			for i in range(10):
				last_20_10_min_open_vol.append((bars[ticker][i].v))
			avg_20_10_vol = sum(last_20_10_min_open_vol)/10

			last_10_min_open_vol = []
			for i in range(10):
				last_10_min_open_vol.append((bars[ticker][i+10].v))
			avg_10_vol = sum(last_10_min_open_vol)/10

			current_volume = (bars[ticker][19].v)

			order_flag = "hold"




			if((avg_price_five <= avg_price_five_ten) and (avg_10_vol > avg_20_10_vol)): 
				self.buyingpower = self.buyingpower - 25*current_price
				self.stocks[ticker] = self.stocks[ticker] + 25
				order_flag = "buy"
			else:
			#if(avg_price_five > price_five_min_ago):
				self.buyingpower = self.buyingpower + current_price*self.stocks[ticker]
				self.stocks[ticker] = 0
				order_flag = "sell"


			self.ledger = self.buyingpower + self.stocks[ticker]*current_price

			#record stats
			file_string = "history/" +self.algoname + "-" + str(starting_time.year) + "-" + str(starting_time.month) + "-" + str(starting_time.day) + ".txt"
			if os.path.isfile(file_string) != True:
				f = open(file_string, 'w')
			f = open(file_string, 'r')

			if f.read(1):
				f = open(file_string, 'a')   
			else:
				f = open(file_string, 'a')
				for i in self.algo_variables:
					f.write(i + " ")
				f.write("\n")

			f.write(str(starting_time.hour*60 + starting_time.minute)+" "+str(current_price) +" "+ str(current_volume) + " " + str(avg_price_five) +" "+ str(avg_price_five_ten) +" "+ str(avg_10_vol) +" "+ str(avg_20_10_vol) +" "+ str(self.stocks[ticker]) + " " + str(self.ledger) + "\n")
			f.flush()
			f.close()
			
			


			#debugger/logger
			starting_time = self.minute_simulator(starting_time)
			print(starting_time)
			print(str(self.ledger) + " " + str(self.buyingpower) + " " + str(self.stocks[ticker]) + " " + order_flag)
			print("delayed_volume")

			#recursive call until end of stock market
			self.delayed_volume_price_trading(ticker, starting_time) 




