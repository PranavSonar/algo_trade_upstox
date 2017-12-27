import math
from datetime import datetime
from threading import Timer

from upstox_api.api import *

# Api key , access token
u = ""
india_vix_open = 0
banknifty_open_price = 0
buy_above = 0.0
buy_target = 0.0
sl_for_buy = 0.0
sell_below = 0.0
sell_target = 0.0
sl_for_sell = 0.0
india_vix_nse_index = 0
nifty_nse_future = 0

buy_order
sell_order


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

    fetch_open_time = today.replace(day=today.day + 1, hour=9, minute=15, second=3, microsecond=0)
    calc_price_time = today.replace(day=today.day + 1, hour=9, minute=15, second=5, microsecond=0)
    buy_order_time_ = today.replace(day=today.day + 1, hour=9, minute=15, second=7, microsecond=0)

    delta_t = fetch_open_time - today
    delta_t_calculation = calc_price_time - today
    delta_t_order_place = buy_order_time_ - today
    time_for_open_prices = delta_t.seconds + 1
    time_for_calculation = delta_t_calculation.seconds + 1
    time_for_order = delta_t_order_place.seconds + 1
    open_price_timer = Timer(time_for_open_prices, fetch_open_prices)
    open_price_timer.start()

    target_set_timer = Timer(time_for_calculation, calculate_target_and_sl)
    target_set_timer.start()

    ############# place buy and buy target ####################

    place_buy_order_set_timer = Timer(time_for_order, place_nifty_buy_order)
    place_buy_order_set_timer.start()

    # place_buy_order_target_set_timer = Timer(time_for_order, place_nifty_buy_target_order)
    # place_buy_order_target_set_timer.start()

    ###################### subscribe to order trigger event ##################
    # u.set_on_order_update (order_triggered_event_handler)
    u.set_on_trade_update(buy_order_triggered_event_handler)


    ###################### subscribe to price change event ##################

    u.set_on_quote_update(event_handler_quote_update)
    u.unsubscribe(nifty_nse_future, LiveFeedType.LTP)
    u.subscribe(nifty_nse_future, LiveFeedType.LTP)


    ############# place sell and sell target ####################
    place_sell_order_set_timer = Timer(time_for_order, place_nifty_sell_order)
    place_sell_order_set_timer.start()

    # place_sell_order_target_set_timer = Timer(time_for_order, place_nifty_sell_target_order)
    # place_sell_order_target_set_timer.start()

    #Start the websocket here
    u.start_websocket(False)

def fetch_open_prices():
    india_vix = u.get_live_feed(india_vix_nse_index, LiveFeedType.Full)
    global india_vix_open
    india_vix_open = india_vix["open"]
    nifty_nse_future_full = u.get_live_feed(nifty_nse_future, LiveFeedType.Full)
    global banknifty_open_price
    nifty_open = nifty_nse_future_full["open"]
    print "nifty open "
    print nifty_open
    print "vix open"
    print india_vix_open


def calculate_target_and_sl():
    first_sd = banknifty_open_price * india_vix_open * 0.00104684784518
    global buy_above
    buy_above = 0.236 * first_sd + banknifty_open_price
    buy_above = math.ceil(buy_above)
    global buy_target
    buy_target = 0.382 * first_sd + banknifty_open_price
    buy_target = math.ceil(buy_target)
    global sl_for_buy
    sl_for_buy = banknifty_open_price - 1
    sl_for_buy = math.ceil(sl_for_buy)
    global sell_below
    sell_below = banknifty_open_price - 0.236 * first_sd
    sell_below = math.ceil(sell_below)
    global sell_target
    sell_target = banknifty_open_price - 0.382 * first_sd
    sell_target = math.ceil(sell_target)
    global sl_for_sell
    sl_for_sell = banknifty_open_price + 1
    sl_for_sell = math.ceil(sl_for_sell)
    print buy_above
    print buy_target
    print sl_for_buy
    print sell_below
    print sell_target
    print sl_for_sell



def place_nifty_buy_order():
    print "####################### Buy order ###################"
    global buy_order
    buy_order = u.place_order(TransactionType.Buy,  # transaction_type
                         nifty_nse_future,  # instrument
                         75,  # quantity
                         OrderType.StopLossMarket,  # order_type
                         ProductType.Intraday,  # product_type
                         0.0,  # price
                         float(buy_above),  # trigger_price
                         0,  # disclosed_quantity
                         DurationType.DAY,  # duration
                         0.0,  # stop_loss
                         0.0,  # square_off
                         None)  # trailing_ticks

    print buy_order

def place_nifty_buy_target_order():
    print "####################### Buy target order ###################"
    print (u.place_order(TransactionType.Sell,  # transaction_type
                         nifty_nse_future,  # instrument
                         75,  # quantity
                         OrderType.Limit,  # order_type
                         ProductType.Intraday,  # product_type
                         float(buy_target),  # price
                         None,  # trigger_price
                         0,  # disclosed_quantity
                         DurationType.DAY,  # duration
                         0.0,  # stop_loss
                         0.0,  # square_off
                         None)  # trailing_ticks
           )


def stop_loss_order_for_buy():
    print "####################### stop loss for buy ###################"
    print (u.place_order(TransactionType.Sell,  # transaction_type
                         nifty_nse_future,  # instrument
                         75,  # quantity
                         OrderType.StopLossMarket,  # order_type
                         ProductType.Intraday,  # product_type
                         0.0,  # price
                         float(sl_for_buy),  # trigger_price
                         0,  # disclosed_quantity
                         DurationType.DAY,  # duration
                         None,  # stop_loss
                         None,  # square_off
                         None)  # trailing_ticks
           )


def place_nifty_sell_order():
    print "####################### Sell order ###################"
    u.place_order(TransactionType.Sell,  # transaction_type
                  nifty_nse_future,  # instrument
                  75,  # quantity
                  OrderType.StopLossMarket,  # order_type
                  ProductType.Intraday,  # product_type
                  0.0,  # price
                  float(sell_below),  # trigger_price
                  0,  # disclosed_quantity
                  DurationType.DAY,  # duration
                  None,  # stop_loss
                  None,  # square_off
                  None)  # trailing_ticks



def place_nifty_sell_target_order():
    print "####################### Sell target order ###################"
    u.place_order(TransactionType.Buy,  # transaction_type
                  nifty_nse_future,  # instrument
                  75,  # quantity
                  OrderType.Limit,  # order_type
                  ProductType.Intraday,  # product_type
                  float(sell_target),  # price
                  None,  # trigger_price
                  0,  # disclosed_quantity
                  DurationType.DAY,  # duration
                  0.0,  # stop_loss
                  0.0,  # square_off
                  None)  # trailing_ticks

def stop_loss_order_for_sell():
    print "####################### Sell SL order ###################"
    u.place_order(TransactionType.Buy,  # transaction_type
                  nifty_nse_future,  # instrument
                  75,  # quantity
                  OrderType.StopLossMarket,  # order_type
                  ProductType.Intraday,  # product_type
                  0.0,  # price
                  float(sell_target),  # trigger_price
                  0,  # disclosed_quantity
                  DurationType.DAY,  # duration
                  0.0,  # stop_loss
                  0.0,  # square_off
                  None)  # trailing_ticks



def buy_order_triggered_event_handler(event):
    print ("Event: %s" % str(event))
    if(event['transaction_type'] == 'B'):
        place_nifty_buy_target_order()
        stop_loss_order_for_buy()
    if (event['transaction_type'] == 'S'):
        place_nifty_sell_target_order()
        stop_loss_order_for_sell()
    # stop_loss_order_for_buy()
    # if (event['aa'] == 'aa'):
    # return


def event_handler_quote_update(message):
    print "Last Trade price" + str(message['ltp']) + " time " + str(datetime.now().time())

# order_buy_and_sell_niftyVWAP('JMJueJYcG05yrycTa4tBX3zP5KGqOl2c8dAZ31Ay','5b9e408076c36ef4bb8d60b50fa7d596b2de4507')
