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


get_single_ticker()




# not completed


# def test_grid():

# 	current_price = get_single_ticker()  # to get the median price
# 	buy_orders = []
# 	sell_orders = []

# 	# sell grid

# 	for i in range(config.number_sell_gridlines):
# 		price = current_price + (config.grid_size * (i+1))
# 		price = round(price, 8)
# 		time.sleep(1)
# 		order = place_order(price, config.position_size, side = "SELL")
# 		sell_orders.append(order['result'])


#  	# buy grid

# 	for i in range(config.number_buy_gridlines):
# 		price = current_price - (config.grid_size * (i+1))
# 		price = round(price, 8)

# 		time.sleep(1)
# 		order = place_order(price, config.position_size, side = "BUY")
# 		buy_orders.append(order['result'])

# 	return sell_orders, buy_orders


# sell_orders, buy_orders = test_grid()  
# closed_orders = []


# # all prints in this loop for testing, will give more meaningful info later / take out random prints

# while True:

#     time.sleep(7)
#     try:
#         closed_trades = my_trades()
#     except Exception as e:
#         print("check closed trades failed")
#     else:
#         print("*****************************************")
        	
#     closed_ids = []

#     for closed_trade in closed_trades['result']:
#         closed_ids.append(closed_trade['orderId'])


#     for sell_order in sell_orders:
#         for i in range(len(closed_trades['result'])):
#             try:                                                                                            # might take out try since the error with the bellow if statement has been corrected
#                 if sell_order['orderId'] == closed_trades['result'][i]['orderId']:               
#                     print("****************************** sell_order loop ***************************")
#                     print("trade is closed")
#                     print("old sell_orders")
#                     print(sell_orders)
#                     print(sell_order['price'])
#                     print(f"sell_order orderId = {sell_order['orderId']}")
#                     new_buy_price = float(sell_order['price']) - config.grid_size
#                     print(f"**************test************ {new_buy_price}")
#                     time.sleep(1)
#                     new_buy_order = place_order(new_buy_price, config.position_size, side = "BUY")



#                     while new_buy_order['success'] == False:                     # 2 errors fixed here ( currently testing ) - invalid signature parameter, pending process need to finish
#                         print("************** BUY ERROR*************")           # this will give an infiniate loop if not enough balance, will add if statement 
#                         time.sleep(1)                        
#                         new_buy_order = place_order(new_buy_price, config.position_size, side = "BUY")




#                     buy_orders.append(new_buy_order['result'])
#                     print(f"buy_orders - {buy_orders}")
                    
#                     break
#             except Exception as e:
#                 print("/////////////////////// if error //////////////")
#                 continue	




#     for buy_order in buy_orders:
#         for i in range(len(closed_trades['result'])):
#             if buy_order['orderId'] == closed_trades['result'][i]['orderId']:
#                 print("**********************************************  buy_order loop ****************************")
#                 print("trade is closed")
#                 print("old buy_orders")
#                 print(buy_orders)
#                 print(buy_order['price'])
#                 print(f"buy_order orderId = {buy_order['orderId']}")
#                 new_sell_price = float(buy_order['price']) + config.grid_size
#                 print(f"********test********** {new_sell_price}")
#                 time.sleep(1)
#                 new_sell_order = place_order(new_sell_price, config.position_size, side = "SELL")





#                 while new_sell_order['success'] == False:
#                     print("**************pending process need to finish ERROR*************")     # 2 errors fixed here ( currently testing ) - invalid signature parameter, pending process need to finish
#                     time.sleep(1)                                                                # this will give an infiniate loop if not enough balance, will add if statement
#                     new_sell_order = place_order(new_sell_price, config.position_size, side = "SELL")



#                 sell_orders.append(new_sell_order['result'])
#                 print(f"sell_orders - {sell_orders}")
                
#                 break


#     for order_id in closed_ids:  # need try here?
#         buy_orders = [buy_order for buy_order in buy_orders if buy_order['orderId'] != order_id]

#         sell_orders = [sell_order for sell_order in sell_orders if sell_order['orderId'] != order_id]

#     print(f"pausing {config.trading_pair}")
#     time.sleep(12)



