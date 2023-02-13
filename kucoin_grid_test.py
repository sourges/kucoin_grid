import json
import requests
import time
import hashlib
import config
import hmac
import base64


# clean this up

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
		str_to_sign = str(now) + 'GET' + '/api/v1/orders/' + order_id  #
		#str_to_sign = str(now) + 'GET' + '/api/v1/accounts'
		#str_to_sign = str(now) + 'GET' + '/api/v1/market/allTickers'
		#str_to_sign = str(now) + 'GET' + '/api/v1/symbols'
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
	orderbook = requests.get(f'https://api.kucoin.com/api/v1/market/orderbook/level2_20?symbol={config.trading_pair}')
	print(orderbook.status_code)
	print(f"{config.trading_pair} Asks - " + orderbook.json()['data']['asks'][0][0])
	print(f"{config.trading_pair} Bids - " + orderbook.json()['data']['bids'][0][0])
	

	best_ask = orderbook.json()['data']['asks'][0][0]
	best_bid = orderbook.json()['data']['bids'][0][0]

	average = (float(best_ask) + float(best_bid)) / 2             # might have issues here with float # - ex - Asks - 0.9234,  Bids - 0.9227, average - 0.9230499999999999
	print(f"average - {average}")


	# returns bid price to set medium for grid
	return average



def place_order(price, position_size, side):
	url = 'https://api.kucoin.com/api/v1/orders'
	now = int(time.time() * 1000)
	data = {
		"clientOid":now,
		"side":side,
		"symbol":config.trading_pair,
		"type":"LIMIT",
		"price": round(price, 4),   # will change later - eth / btc size for example
		"size":config.position_size  
	}
	data_json = json.dumps(data)
	HEADERS = call_code(data_json)
	response = requests.post(url, headers = HEADERS, data = data_json)
	print(response.status_code)
	print(response.json())
	return response.json()

# test order
# place_order(0.85, 10, "BUY")



# closed or canceled trades - use 'id'
# works

# def get_closed_trades():
# 	url = 'https://api.kucoin.com/api/v1/limit/orders'
# 	now = int(time.time() * 1000)
# 	str_to_sign = str(now) + 'GET' + '/api/v1/limit/orders'
# 	signature = base64.b64encode(
# 		hmac.new(config.api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
# 	passphrase = base64.b64encode(hmac.new(config.api_secret.encode('utf-8'), config.api_passphrase.encode('utf-8'), hashlib.sha256).digest())
# 	HEADERS = {
# 		"KC-API-KEY": config.api_key,
# 		"KC-API-SIGN": signature,
# 		"KC-API-TIMESTAMP": str(now),
# 		"KC-API-PASSPHRASE": passphrase,
# 		"KC-API-KEY-VERSION": "2",
# 		"Content-Type": "application/json"
# 	}

# 	response = requests.get(url, headers = HEADERS)

# 	# #test prints
# 	# print(response.status_code)
# 	# print(response.json())

# 	return response.json()

# get_closed_trades()



def get_closed_trades():
	url = f'https://api.kucoin.com/api/v1/orders?status=done&symbol={config.trading_pair}&currentPage=1&pageSize=500'
	now = int(time.time() * 1000)
	str_to_sign = str(now) + 'GET' + f'/api/v1/orders?status=done&symbol={config.trading_pair}&currentPage=1&pageSize=500'
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

	response = requests.get(url, headers = HEADERS)

	#test prints
	# print(response.status_code)
	# print(response.json())

	return response.json()

# get_closed_trades()

# use later for price + size 

# def get_symbols(): 
# 	now = int(time.time() * 1000)
# 	str_to_sign = str(now) + 'GET' + '/api/v1/symbols/'
# 	url = f'https://api.kucoin.com/api/v1/symbols/{config.trading_pair}'
# 	HEADERS = call_code(str_to_sign)
# 	response = requests.get(url, headers = HEADERS)
# 	baseIncrement = len(response.json()['data']['baseIncrement'].split('.')[1])
# 	quoteIncrement = len(response.json()['data']['quoteIncrement'].split('.')[1])
# 	priceIncrement = len(response.json()['data']['priceIncrement'].split('.')[1])
# 	return baseIncrement, quoteIncrement, priceIncrement

# base, quote, priced = get_symbols()
# print(base, quote, priced)


def test_grid():

	current_price = get_single_ticker()  # to get the median price
	buy_orders = []
	sell_orders = []

	# sell grid

	for i in range(config.number_sell_gridlines):
		price = current_price + (config.grid_size * (i+1))
		price = round(price, 8)   
		time.sleep(2)
		order = place_order(price, config.position_size, side = "SELL")
		sell_orders.append(order['data'])


 	# buy grid

	for i in range(config.number_buy_gridlines):
		price = current_price - (config.grid_size * (i+1))
		price = round(price, 8)

		time.sleep(2)
		order = place_order(price, config.position_size, side = "BUY")
		buy_orders.append(order['data'])

	return sell_orders, buy_orders



sell_orders, buy_orders = test_grid()  
closed_order_ids = []

# print(buy_orders)


while True:

	time.sleep(15)
	try:
		closed_trades = get_closed_trades()
		time.sleep(2)
	except Exception as e:
		print("check closed trades failed")
	else:
		print("************************************")

	closed_ids = []

	for closed_trade in closed_trades['data']['items']:
		closed_ids.append(closed_trade['id'])


	for buy_order in buy_orders:
		for i in range(len(closed_trades['data']['items'])):
			try:
				if buy_order['orderId'] == closed_trades['data']['items'][i]['id']:
					print("**********************************************  buy_order loop ****************************")
					print("trade is closed")
					print("old buy_orders")
					print(buy_orders)
					# print(buy_order['price'])
					print(f"buy_order orderId = {buy_order['orderId']}")

					new_sell_price = float(closed_trades['data']['items'][i]['price']) + config.grid_size

					#new_sell_price = float(buy_order['price']) + config.grid_size
					print(f"********test********** {new_sell_price}")
					time.sleep(1)
					new_sell_order = place_order(new_sell_price, config.position_size, side = "SELL")


	                # next - not live


	                # while new_sell_order['success'] == False:
	                #     print("**************pending process need to finish ERROR*************")     # 2 errors fixed here ( currently testing ) - invalid signature parameter, pending process need to finish
	                #     time.sleep(1)                                                                # this will give an infiniate loop if not enough balance, will add if statement
	                #     new_sell_order = place_order(new_sell_price, config.position_size, side = "SELL")



					sell_orders.append(new_sell_order['data'])
					print(f"sell_orders - {sell_orders}")

					break
			except Exception as e:
				print("/////////////////// if error ////////////")
				continue


	for sell_order in sell_orders:
		for i in range(len(closed_trades['data']['items'])):
			try:                                                                                            # might take out try since the error with the bellow if statement has been corrected
				if sell_order['orderId'] == closed_trades['data']['items'][i]['id']:               
					print("****************************** sell_order loop ***************************")
					print("trade is closed")
					print("old sell_orders")
					print(sell_orders)
					#print(sell_order['price'])  
					print(f"sell_order orderId = {sell_order['orderId']}")

					new_buy_price = float(closed_trades['data']['items'][i]['price']) - config.grid_size

					print(f"**************test************ {new_buy_price}")
					time.sleep(1)
					new_buy_order = place_order(new_buy_price, config.position_size, side = "BUY")


					# not live yet

					# while new_buy_order['success'] == False:                     # 2 errors fixed here ( currently testing ) - invalid signature parameter, pending process need to finish
					# print("************** BUY ERROR*************")           # this will give an infiniate loop if not enough balance, will add if statement 
					# time.sleep(1)                        
					# new_buy_order = place_order(new_buy_price, config.position_size, side = "BUY")



					buy_orders.append(new_buy_order['data'])
					print(f"buy_orders - {buy_orders}") 
					break
			except Exception as e:
				print("/////////////////////// if error //////////////")
				continue


	for order_id in closed_ids: 
		buy_orders = [buy_order for buy_order in buy_orders if buy_order['orderId'] != order_id]

		sell_orders = [sell_order for sell_order in sell_orders if sell_order['orderId'] != order_id]

	print(f"pausing {config.trading_pair}")
	time.sleep(15)
