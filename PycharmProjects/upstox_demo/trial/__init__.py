from upstox_api.api import *

from strategy_VWAP import order_buy_and_sell_niftyVWAP
from auto_login_selenium import login_to_upstox

api_key = '7QQDdOIHNxatXDiRIHbyv2sG3J8QOozU7o8UYKmu'
s = Session(api_key)
s.set_redirect_uri('http://127.0.0.0')
s.set_api_secret('jwz8wlhe14')


# use below url to login and get code
print (s.get_login_url())


code = login_to_upstox(s.get_login_url())

# # code goes here
s.set_code (code)


# use code to generate access token
access_token = s.retrieve_access_token()
print "access_token %s" % str(access_token)
print "api_key %s" % str(api_key)


order_buy_and_sell_niftyVWAP(api_key,access_token,'nifty17decfut')
order_buy_and_sell_niftyVWAP(api_key,access_token,'banknifty17decfut')

