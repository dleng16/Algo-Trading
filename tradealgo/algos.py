def print_info():
	print("Now in tradealgo package")
	

def sell_all(api):
	for i in api.list_positions():
			api.submit_order(
                symbol=i.symbol,
                qty=i.qty,
                side='sell',
                type='market',
                time_in_force='day',
            )


def momentum_state_defined(api):
	check_time = time.localtime()
	if(check_time.tm_hour == 9-3 and check_time.tm_min == 30):
	 	print("Stock Market Opened!")
	 	momentum_up_state = api.get_barset('AAPL', '1min', 1)


def momentum_trade(api):

	bars = api.get_barset('AAPL', '1Min', 3)
	start =  bars["AAPL"][0].c
	last_five_min_open = []
	convolution_list = [.25,.25,.5]
	for i in range(3):
		last_five_min_open.append((bars["AAPL"][i].c)*convolution_list[i])
	avg = sum(last_five_min_open)
	if(avg > start):
		print("Buy 1 " + str(start) + " " + str(avg))

		api.submit_order(
                symbol='AAPL',
                qty=150,
                side='buy',
                type='market',
                time_in_force='day',
            )
	else:
		print("Sell All " + str(start) + " " + str(avg))

		sell_all(api)
	 	
	#while(True):