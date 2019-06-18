from matplotlib import pyplot as plt
import matplotlib.ticker
import pandas as pd
import os.path






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


	def minute_simulator(self, time):
		time = time + pd.Timedelta('1 min')
		return time

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
			file_string = self.algoname + "-" + str(starting_time.year) + "-" + str(starting_time.month) + "-" + str(starting_time.day) + ".txt"
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

		self.algo_variables = ['time-hour', 'stock-price', 'avg-price-5-min', 'number-of-stocks', 'portfolio-value']

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



			order_flag = "hold"

			#submit sell
			#if(((current_volume > vol_percentile_threshold) and (avg_price_five < start_price_five)) or ((current_volume > avg_vol) and (avg_price_five < start_price_five))):
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
				
				if((abs(bars[ticker][4].c-avg_price_five) <.40)):
					self.buyingpower = self.buyingpower - 25*current_price
					self.stocks[ticker] = self.stocks[ticker] + 25
					order_flag = "buy"
				else:
					self.buyingpower = self.buyingpower + current_price*self.stocks[ticker]
					self.stocks[ticker] = 0
					order_flag = "sell"


			self.ledger = self.buyingpower + self.stocks[ticker]*current_price

			#record stats
			file_string = self.algoname + "-" + str(starting_time.year) + "-" + str(starting_time.month) + "-" + str(starting_time.day) + ".txt"
			if os.path.isfile(file_string) != True:
				f = open(file_string, 'w')
			f = open(file_string, 'r')

			if f.read(1):
				f = open(file_string, 'a')   
			else:
				f = open(file_string, 'a')
				for i in self.algo_variables:
					f.write(i + " ")

			f.write(str(starting_time.hour*60 + starting_time.minute)+" "+str(current_price) +" "+ str(avg_price_five) +" "+ str(self.stocks[ticker]) + " " + str(self.ledger) + "\n")
			f.flush()
			f.close()
			
			


			#debugger/logger
			starting_time = self.minute_simulator(starting_time)
			print(starting_time)
			print(str(self.ledger) + " " + str(self.buyingpower) + " " + str(self.stocks[ticker]) + " " + order_flag)

			#recursive call until end of stock market
			self.mode_based_trading(ticker, starting_time) 

