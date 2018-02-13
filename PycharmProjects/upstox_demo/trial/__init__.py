from threading import Timer

from upstox_api.api import *

from auto_login_selenium import login_to_upstox
from strategy_VWAP import order_buy_and_sell_niftyVWAP


def main_code():
    api_key = '7QQDdOIHNxatXDiRIHbyv2sG3J8QOozU7o8UYKmu'
    s = Session(api_key)
    s.set_redirect_uri('http://127.0.0.0')
    s.set_api_secret('jwz8wlhe14')

    # use below url to login and get code
    print (s.get_login_url())

    code = login_to_upstox(s.get_login_url())

    # # code goes here
    s.set_code(code)

    # use code to generate access token
    access_token = s.retrieve_access_token()
    print "access_token %s" % str(access_token)
    print "api_key %s" % str(api_key)

    u = Upstox(api_key, access_token)

    u.get_master_contract('NSE_FO')  # get contracts for NSE FO
    u.get_master_contract('NSE_INDEX')  # get contracts for NSE_INDEX

    # def nifty():
    order_buy_and_sell_niftyVWAP(u, 'nifty18febfut', 45)


    # def banknifty():
    #     order_buy_and_sell_niftyVWAP(u, 'banknifty18janfut', 15)
    #
    #
    # t1 = threading.Thread(target=nifty, args=[])
    # t2 = threading.Thread(target=banknifty, args=[])
    # t1.start()
    # t2.start()
# fetch_open_time = toda0y.replace(day=1, hour=8, minute=53 , second=0, microsecond=500)

# today = datetime.today()
# fetch_open_time = today.replace(day=today.day + 1, hour=4, minute=15 , second=0, microsecond=500)
# delta_t = fetch_open_time - today
# time_for_open_prices = delta_t.seconds + 1
# open_price_timer = Timer(time_for_open_prices, main_code)
# open_price_timer.start()

main_code()
