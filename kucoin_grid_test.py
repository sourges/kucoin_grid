import json
import requests
import time
import hashlib
import config
import hmac
import base64




url = 'https://api.kucoin.com/api/v1/accounts'
now = int(time.time() * 1000)
str_to_sign = str(now) + 'GET' + '/api/v1/accounts'
signature = base64.b64encode(
    hmac.new(config.api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
passphrase = base64.b64encode(hmac.new(config.api_secret.encode('utf-8'), config.api_passphrase.encode('utf-8'), hashlib.sha256).digest())
headers = {
    "KC-API-SIGN": signature,
    "KC-API-TIMESTAMP": str(now),
    "KC-API-KEY": config.api_key,
    "KC-API-PASSPHRASE": passphrase,
    "KC-API-KEY-VERSION": "2",
    "Content-Type": "application/json"
}

# for testing connection
# response = requests.request('get', url, headers=headers)
# print(response.status_code)
# print(response.json())





# needs major clean up
def call_code(data_json=None, order_id=None):
	if data_json == None:
		now = int(time.time() * 1000)
		#str_to_sign = str(now) + 'GET' + '/api/v1/orders?status=active'
		#str_to_sign = str(now) + 'GET' + '/api/v1/orders/' + order_id  #
		#str_to_sign = str(now) + 'GET' + '/api/v1/accounts'
		#str_to_sign = str(now) + 'GET' + '/api/v1/market/allTickers'
		#str_to_sign = str(now) + 'GET' + '/api/v1/symbols'
		str_to_sign = str(now) + 'GET' + '/api/v1/limit/orders'
	else:
		now = int(time.time() * 1000)
		str_to_sign = str(now) + 'POST' + '/api/v1/orders' + data_json
		
		print(str_to_sign)

	signature = base64.b64encode(
		hmac.new(config.api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
	passphrase = base64.b64encode(hmac.new(config.api_secret.encode('utf-8'), config.api_passphrase.encode('utf-8'), hashlib.sha256).digest())
	HEADERS = {
		"KC-API-KEY": config.api_key,
		"KC-API-SIGN": signature,
		"KC-API-TIMESTAMP": str(now),
		"KC-API-PASSPHRASE": passphrase,
		"KC-API-KEY-VERSION": "2",
		"Content-Type": "application/json"
	}
	return HEADERS


# gets single ticker info - must know which ticker request
# currently works

def get_single_ticker():
	#must create a variable for symbol
	orderbook = requests.get(f'https://api.kucoin.com/api/v1/market/orderbook/level2_20?symbol={config.symbol}')
	print(orderbook.status_code)
	print(f"{config.symbol} Asks - " + orderbook.json()['data']['asks'][0][0])
	print(f"{config.symbol} Bids - " + orderbook.json()['data']['bids'][0][0])
	

	best_ask = orderbook.json()['data']['asks'][0][0]
	best_bid = orderbook.json()['data']['bids'][0][0]

	average = (float(best_ask) + float(best_bid)) / 2             # might have issues here with float # - ex - Asks - 0.9234,  Bids - 0.9227, average - 0.9230499999999999
	print(f"average - {average}")


	# returns bid price to set medium for grid
	return average



def place_order(price, position_size, side):
	# is position_size needed for an arguement if its coming from config

	url = 'https://api.kucoin.com/api/v1/orders'
	now = int(time.time() * 1000)
	data = {
		"clientOid":now,
		"side":side,
		"symbol":config.symbol,
		"type":"LIMIT",
		"price": round(price, 4),
		"size":config.position_size  # since moved to config, does place_order function need position_size anymore
	}
	data_json = json.dumps(data)
	HEADERS = call_code(data_json)
	response = requests.post(url, headers = HEADERS, data = data_json)
	print(response.status_code)
	print(response.json())
	return response.json()

# test order
# place_order(0.85, 10, "BUY")


# must know id before use
def get_order_info(order_id):
	url = 'https://api.kucoin.com/api/v1/orders/' + order_id
	# str_to_sign = str(now) + 'GET' + '/api/v1/orders/62c19f43fc3df20001f6214c'
	data_json = None
	HEADERS = call_code(data_json, order_id)
	response = requests.get(url, headers = HEADERS)
	print(response.status_code)
	print(response.json())
	return response.json()



# closed or canceled trades - use 'id'
# works
def get_list():
	url = 'https://api.kucoin.com/api/v1/limit/orders'
	data_json = None
	HEADERS = call_code(data_json)
	response = requests.get(url, headers = HEADERS)
	print(response.status_code)
	print(response.json())


get_list()




# not sure if needed

# def get_symbols(): 
# 	now = int(time.time() * 1000)
# 	str_to_sign = str(now) + 'GET' + '/api/v1/symbols/'
# 	url = f'https://api.kucoin.com/api/v1/symbols/{config.symbol}'
# 	HEADERS = call_code(str_to_sign)
# 	response = requests.get(url, headers = HEADERS)
# 	baseIncrement = len(response.json()['data']['baseIncrement'].split('.')[1])
# 	quoteIncrement = len(response.json()['data']['quoteIncrement'].split('.')[1])
# 	priceIncrement = len(response.json()['data']['priceIncrement'].split('.')[1])
# 	return baseIncrement, quoteIncrement, priceIncrement

# base, quote, priced = get_symbols()
# print(base, quote, priced)





# not completed


def test_grid():

	current_price = get_single_ticker()  # to get the median price
	buy_orders = []
	sell_orders = []

	# sell grid

	for i in range(config.number_sell_gridlines):
		price = current_price + (config.grid_size * (i+1))
		price = round(price, 8)   
		time.sleep(1)
		order = place_order(price, config.position_size, side = "SELL")
		sell_orders.append(order['data'])


 	# buy grid

	for i in range(config.number_buy_gridlines):
		price = current_price - (config.grid_size * (i+1))
		price = round(price, 8)

		time.sleep(1)
		order = place_order(price, config.position_size, side = "BUY")
		buy_orders.append(order['data'])

	return sell_orders, buy_orders



#sell_orders, buy_orders = test_grid()  
closed_order_ids = []

# print(buy_orders)


# while True:

# 	time.sleep(5)
# 	try:
# 		closed_trades = get_list()
# 	except Exception as e:
# 		print("check closed trades failed")
# 	else:
# 		print("************************************")


# 	for closed_trade in closed_trades['data']

# # # all prints in this loop for testing, will give more meaningful info later / take out random prints

# while True:
# 	#print("checking orders")

# 	# put in a try, except - or at least see about being timed out

# 	for sell_order in sell_orders:
# 		print("checking sells")
# 		try:
# 			order = get_order_info(sell_order['orderId'])
		

# 			order_info = order['data']
# 			#print(order_info)

# 			print(f"buy list - {buy_orders}")
# 			print(f"sell list - {sell_orders}")
# 		except Exception as e:
# 			print("error in #1")
# 			continue

# 		if order_info['isActive'] == config.closed_order_status:  # need a variable or can just do False?
# 			closed_order_ids.append(order_info['id'])
			
# 			print(f"Closed Orders - {closed_order_ids}")

# 			new_buy_price = float(order_info['price']) - config.grid_size
# 			new_buy_order = place_order(new_buy_price, config.position_size, "BUY")
# 			buy_orders.append(new_buy_order['data'])

			

# # need to make sure this append works - print out buy_ourders again with new append


# 		time.sleep(config.check_orders_frequency) # do we really need this variable and not just a normal #

# 	for buy_order in buy_orders:
# 		try:
# 			order = get_order_info(buy_order['orderId'])
# 		 	# print(order)

# 			order_info = order['data']
# 		except Exception as e:
# 			print("error in #2")
# 			continue

# 		if order_info['isActive'] == config.closed_order_status:  # need a variable or can just do False?
# 			closed_order_ids.append(order_info['id'])

# 			print(f"Closed Orders - {closed_order_ids}")

# 			new_sell_price = float(order_info['price']) + config.grid_size
# 			new_sell_order = place_order(new_sell_price, config.position_size, "SELL")
# 			sell_orders.append(new_sell_order['data'])

# 		time.sleep(config.check_orders_frequency) # do we really need this variable and not just a normal #

	
# 	for order_id in closed_order_ids:
# 		buy_orders = [buy_order for buy_order in buy_orders if buy_order['orderId'] != order_id]
# 		print(f" Buy list - {buy_orders}")
		
# 		sell_orders = [sell_order for sell_order in sell_orders if sell_order['orderId'] != order_id]
# 		print(f" Sell list - {sell_orders}")



