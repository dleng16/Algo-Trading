import alpaca_trade_api as tradeapi
import time


def sell_all(api):
	for i in api.list_positions():
			api.submit_order(
                symbol=i.symbol,
                qty=i.qty,
                side='sell',
                type='market',
                time_in_force='day',
            )

def momentum_trade(api):

	bars = api.get_barset('AAPL', '1Min', 5)
	start =  bars["AAPL"][0].o
	last_five_min_open = []
	convolution_list = [.1,.1,.2,.2,.4]
	for i in range(5):
		last_five_min_open.append((bars["AAPL"][i].o)*convolution_list[i])
	avg = sum(last_five_min_open)
	if(avg > start):
		print("Buy 1 " + str(start) + " " + str(avg))

		api.submit_order(
                symbol='AAPL',
                qty=1,
                side='buy',
                type='market',
                time_in_force='day',
            )
	else:
		print("Sell All " + str(start) + " " + str(avg))

		sell_all(api)





fh = open("../private.txt","r")

temp = fh.read().split('\n')
#print(temp)


api = tradeapi.REST(
    key_id= temp[0],
    secret_key= temp[1],
    base_url='https://paper-api.alpaca.markets'
)

# print(api.get_clock())
# print(api.get_barset('AAPL', 'day', limit=1))

# api.submit_order(
#                 symbol='AAPL',
#                 qty=1,
#                 side='buy',
#                 type='market',
#                 time_in_force='day',
#             )

# clock = api.get_clock()

# now = clock.timestamp

# print(now)
# print(clock.is_open)
# #print(api.list_assets())
# pos = api.list_positions()
# print(pos[0])
# print(now.strftime('%Y-%m-%d'))

# bars = api.get_barset('AAPL', '1Min', 5)

# print(bars)
# print(" ")
# print(" ")
# print(bars.df)
# print(bars["AAPL"][1].c)


while True:
	clock = api.get_clock()
	if clock.is_open:
		print("")
		momentum_trade(api)
	else:
		print("Market Closed " + str(clock.timestamp))

	time.sleep(60)

