import matplotlib
import tradealgo.algos_stats as algos_stats
import alpaca_trade_api as tradeapi
import time
import numpy as np
import pandas as pd
import os.path
from scipy.fftpack import fft, dct
import matplotlib.pyplot as plt



print("Testing Polygon API")

fh = open("../private.txt", "r")
temp = fh.read().split('\n')
api = tradeapi.REST(
    key_id= temp[0],
    secret_key= temp[1],
    base_url='https://paper-api.alpaca.markets'
)

hi = pd.Timestamp(year=2019, month=6, day=19, hour=10, minute = 3).isoformat()
time3 = pd.Timestamp(hi, tz='America/New_York').isoformat()
hi = pd.Timestamp(year=2019, month=6, day=19, hour=10, minute = 10).isoformat()
time2 = pd.Timestamp(hi, tz='America/New_York').isoformat()

aapl = api.polygon.historic_agg('minute', 'AAPL', _from = time3, to = time2, limit=10).df
testing = api.polygon.historic_quotes('AAPL', '2019-6-21', limit = 50, offset =  1561134600000)
historic = api.polygon.historic_trades('AAPL', '2019-6-21', limit = 50, offset = 1561134600000)
print(testing)
print(historic)

print(pd.Timestamp(year=2019, month=6, day=19, hour=10, minute = 3, second = 4).value / 10**6)
print(hi)

# while(1):
# 	print(api.polygon.last_quote('AAPL'))
# 	time.sleep(0.5)

def record_stats(file_name, data): #has to be in csv data format already
		if os.path.isfile(file_name) != True:
			f = open(file_name, 'w')
			f.write(data)
			f.flush()
			f.close

start = pd.Timestamp(year=2019, month=6, day=24, hour=15, minute = 40)
end = pd.Timestamp(year=2019, month=6, day=24, hour=16, minute = 40)

def conversion_lower_resolution(start, end, ticker, resolution = 'second'):
	unix_current = int(start.value /10**6)
	unix_end = int(end.value /10**6)
	lower_res_data = []
	while(unix_current < unix_end):
		data = api.polygon.historic_trades(ticker, str(start.year) + '-' + str(start.month) + '-' + str(start.day), limit = 10, offset = unix_current)
		count = 0
		price = 0
		size = 0
		previous_price = 0 #sometimes in a certain second there is no data so revert to past price
		new_dic = {}
		for i in data:
			if(int(i.timestamp.value /10**6) < unix_current + 1000):
				size += i.size
				price += i.price
				count += 1
			else: 
				break
		if(count == 0):
			price = previous_price
		else:
			price = price / count
			previous_price = price
		new_dic['unix_current'] = unix_current
		new_dic['price'] = price
		new_dic['size'] = size
		lower_res_data.append(new_dic)
		unix_current += 1000
		print(unix_current)
	return lower_res_data

def conversion_lower_resolutionV2(start, end, ticker, resolution = 'second'): #900 times faster
	unix_current = int(start.value /10**6)
	unix_end = int(end.value /10**6)
	lower_res_data = []
	count = 0
	price = 0
	size = 0
	previous_price = 0 #sometimes in a certain second there is no data so revert to past price
	new_dic = {}
	while(unix_current < unix_end):
		data = api.polygon.historic_trades(ticker, str(start.year) + '-' + str(start.month) + '-' + str(start.day), limit = 3000, offset = unix_current)
		#print("get_data")
		for i in data:
			if(int(i.timestamp.value /10**6) < unix_current + 1000):
				size += i.size
				price += i.price
				count += 1
			else: 
				if(count == 0):
					price = previous_price
				else:
					price = price / count
					previous_price = price
				new_dic['unix_current'] = unix_current
				new_dic['price'] = price
				new_dic['size'] = size
				lower_res_data.append(new_dic)
				#print(new_dic)
				new_dic = {}
				unix_current += 1000
				size = i.size
				price = i.price
				count = 1
				#print(str(unix_current) + ": " + str(unix_end))
	return lower_res_data

def fourier_transform(data, sample_spacing = 1): #data in list form please
	N = len(data)
	total_sum = sum(data)
	average = total_sum/N
	x = np.linspace(0.0, 1.0/sample_spacing, N)
	plt.figure(0)
	plt.plot(x, data)

	normalized_data = [i-average for i in data]

	N = len(normalized_data)
	y = np.array(normalized_data)
	yf = fft(y)
	xf = np.linspace(0.0, 1.0/(2.0*sample_spacing), N//2)

	log_data = np.log(2.0/N * np.abs(yf[0:N//2]))
	xf = np.delete(xf, 0)
	log_data = np.delete(log_data, 0)
	
	plt.figure(1)
	plt.plot(xf, log_data)
	plt.grid()
	plt.show()


dicty = conversion_lower_resolutionV2(start, end, 'AAPL')
print(dicty)
lol = pd.DataFrame(dicty)
print(lol['price'].tolist())
record_stats('aapl.23.22', lol.to_csv())

fourier_transform(lol['price'].tolist())




#print(testing[0].timestamp.value)

#record_stats("hips.csv", historic.to_csv())
#record_stats("hipso.csv", testing.df.to_csv())

class trading_simulator()