import math
from datetime import datetime
from threading import Timer

from upstox_api.api import *



def order_buy_and_sell_niftyVWAP(apiKey, accessToken):
    global u
    u = Upstox(apiKey, accessToken)

    u.get_master_contract('NSE_FO')  # get contracts for NSE FO
    u.get_master_contract('NSE_INDEX')  # get contracts for NSE_INDEX
    global india_vix_nse_index
    india_vix_nse_index = u.get_instrument_by_symbol('NSE_INDEX', 'INDIA_VIX')
    global nifty_nse_future
    nifty_nse_future = u.get_instrument_by_symbol('NSE_FO', 'nifty17decfut')

    today = datetime.today()

    fetch_open_time = today.replace(day=today.day + 1, hour=9, minute=33, second=30, microsecond=0)

    delta_t = fetch_open_time - today

    time_for_open_prices = delta_t.seconds + 1
    ############# place buy and buy target ####################
    u.set_on_trade_update(buy_order_triggered_event_handler)
    place_buy_order_set_timer = Timer(time_for_open_prices, place_nifty_buy_order)
    place_buy_order_set_timer.start()
    u.start_websocket(False)
    # place_buy_order_target_set_timer = Timer(time_for_order, place_nifty_buy_target_order)
    # place_buy_order_target_set_timer.start()


def place_nifty_buy_order():
    print "####################### Buy order ###################"
    print (u.place_order(TransactionType.Buy,  # transaction_type
                         nifty_nse_future,  # instrument
                         75,  # quantity
                         OrderType.Market,  # order_type
                         ProductType.Intraday,  # product_type
                         0.0,  # price
                         0.0,  # trigger_price
                         0,  # disclosed_quantity
                         DurationType.DAY,  # duration
                         0.0,  # stop_loss
                         0.0,  # square_off
                         None)  # trailing_ticks
           )



def buy_order_triggered_event_handler(event):
    print ("Event: %s" % str(event))
    # stop_loss_order_for_buy()
    # if (event['aa'] == 'aa'):
    # return


order_buy_and_sell_niftyVWAP('7QQDdOIHNxatXDiRIHbyv2sG3J8QOozU7o8UYKmu','192c89cf743ae3e0d313f70bfa28bb47cdcdb76d')
