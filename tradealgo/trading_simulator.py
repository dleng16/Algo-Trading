import matplotlib
import tradealgo.algos_stats as algos_stats
import alpaca_trade_api as tradeapi
import time
import numpy as np
import pandas as pd
import os.path


#second based simulator

class trading_simulator:

	def __init__(self, api, buyingpower = 30000, algoname = "default"):
		self.safety = True
		self.api = api
		self.buyingpower = buyingpower #total cash in account
		self.portfolio_value = buyingpower #portfolio value
		self.stocks = {}
		self.algoname = algoname
		self.order_flag = "hold"


	def minute_simulator(self, time):
		time = time + pd.Timedelta('1 min')
		return time