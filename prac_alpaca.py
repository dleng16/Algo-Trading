import alpaca_trade_api as tradeapi

fh = open("../private.txt","r")


temp = fh.read().split('\n')
print(temp)


api = tradeapi.REST(
    key_id= temp[0],
    secret_key= temp[1],
    base_url='https://paper-api.alpaca.markets'
)

print(api.get_clock())
print(api.get_barset('AAPL', 'day', limit=1))