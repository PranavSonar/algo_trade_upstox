import math
from datetime import datetime
from threading import Timer

from upstox_api.api import *

# Api key , access token
u = ""
india_vix_open = 0
nifty_open = 0
buy_above = 0.0
buy_target = 0.0
sl_for_buy = 0.0
sell_below = 0.0
sell_target = 0.0
sl_for_sell = 0.0
india_vix_nse_index = 0
nifty_nse_future = 0


def order_buy_and_sell_niftyVWAP(apiKey, accessToken, symbol_string):
    global u
    u = Upstox(apiKey, accessToken)

    u.get_master_contract('NSE_FO')  # get contracts for NSE FO
    u.get_master_contract('NSE_INDEX')  # get contracts for NSE_INDEX
    global india_vix_nse_index
    india_vix_nse_index = u.get_instrument_by_symbol('NSE_INDEX', 'INDIA_VIX')
    global nifty_nse_future
    nifty_nse_future = u.get_instrument_by_symbol('NSE_FO', symbol_string)
    print nifty_nse_future

    today = datetime.today()

    fetch_open_time = today.replace(day=today.day + 1, hour=9, minute=15, second=0, microsecond=500)
    # calc_price_time = today.replace(day=today.day + 1, hour=9, minute=15, second=5, microsecond=0)
    # buy_order_time_ = today.replace(day=today.day + 1, hour=9, minute=15, second=6, microsecond=0)
    # sell_order_time = today.replace(day=today.day + 1, hour=9, minute=15, second=9, microsecond=0)

    delta_t = fetch_open_time - today
    # delta_t_calculation = calc_price_time - today
    # delta_t_order_place = buy_order_time_ - today
    # delta_t_sell_place = sell_order_time - today
    time_for_open_prices = delta_t.seconds + 1
    # time_for_calculation = delta_t_calculation.seconds + 1
    # time_for_buy = delta_t_order_place.seconds + 1
    # time_for_sell = delta_t_sell_place.seconds + 1
    open_price_timer = Timer(time_for_open_prices, fetch_open_prices)
    open_price_timer.start()

    # target_set_timer = Timer(time_for_calculation, calculate_target_and_sl)
    # target_set_timer.start()

    ###################### subscribe to order trigger event ##################
    u.set_on_trade_update(buy_order_triggered_event_handler)

    ###################### subscribe to price change event ##################

    # u.set_on_quote_update(event_handler_quote_update)
    u.unsubscribe(nifty_nse_future, LiveFeedType.LTP)
    u.subscribe(nifty_nse_future, LiveFeedType.LTP)


    ############# place buy and buy target ####################

    # place_buy_order_set_timer = Timer(time_for_buy, nifty_oco_buy_order)
    # place_buy_order_set_timer.start()



    ############# place sell and sell target ####################
    # place_sell_order_set_timer = Timer(time_for_sell, nifty_oco_sell_order)
    # place_sell_order_set_timer.start()

    #Start the websocket here
    u.start_websocket(False)

def fetch_open_prices():
    india_vix = u.get_live_feed(india_vix_nse_index, LiveFeedType.Full)
    global india_vix_open
    india_vix_open = india_vix["open"]
    if(india_vix_open==0):
        fetch_open_prices()
    else:
        nifty_nse_future_full = u.get_live_feed(nifty_nse_future, LiveFeedType.Full)
        global nifty_open
        nifty_open = nifty_nse_future_full["open"]
        if (nifty_open == 0):
            fetch_open_prices()
        else:
            print "nifty open "
            print nifty_open
            print "vix open"
            print india_vix_open
            calculate_target_and_sl()




def calculate_target_and_sl():
    first_sd = nifty_open * india_vix_open * 0.00104684784518
    global buy_above
    buy_above = 0.236 * first_sd + nifty_open
    buy_above = math.ceil(buy_above)
    global buy_target
    buy_target = 0.382 * first_sd + nifty_open
    buy_target = math.ceil(buy_target)
    global sl_for_buy
    sl_for_buy = nifty_open - 1
    sl_for_buy = math.ceil(sl_for_buy)
    global sell_below
    sell_below = nifty_open - 0.236 * first_sd
    sell_below = math.ceil(sell_below)
    global sell_target
    sell_target = nifty_open - 0.382 * first_sd
    sell_target = math.ceil(sell_target)
    global sl_for_sell
    sl_for_sell = nifty_open + 1
    sl_for_sell = math.ceil(sl_for_sell)
    print 'buy above: %s' % str(buy_above)
    print 'buy_target: %s'% str(buy_target)
    print 'sl_for_buy: %s' %str(sl_for_buy)
    print 'sell_below: %s' %str(sell_below)
    print 'sell_target: %s' %str(sell_target)
    print 'sl_for_sell: %s' %str(sl_for_sell)
    nifty_oco_buy_order()



def nifty_oco_buy_order():
    print "####################### Buy order OCO and limit ###################"
    print (u.place_order(TransactionType.Buy,  # transaction_type
                         nifty_nse_future,  # instrument
                         nifty_nse_future['lot_size'],  # quantity
                         OrderType.StopLossLimit,  # order_type
                         ProductType.OneCancelsOther,  # product_type
                         float(buy_above+1),  # price
                         float(buy_above),  # trigger_price
                         0,  # disclosed_quantity
                         DurationType.DAY,  # duration
                         float(buy_above-sl_for_buy),  # stop_loss
                         float(buy_target-buy_above),  # square_off
                         None)  # trailing_ticks
           )
    nifty_oco_sell_order()

def nifty_oco_sell_order():
    print "####################### Sell order OCO and limit ###################"
    print (u.place_order(TransactionType.Sell,  # transaction_type
                         nifty_nse_future,  # instrument
                         nifty_nse_future['lot_size'],  # quantity
                         OrderType.StopLossLimit,  # order_type
                         ProductType.OneCancelsOther,  # product_type
                         float(sell_below-1),  # price
                         float(sell_below),  # trigger_price
                         0,  # disclosed_quantity
                         DurationType.DAY,  # duration
                         float(sl_for_sell-sell_below),  # stop_loss
                         float(sell_below-sell_target),  # square_off
                         None)  # trailing_ticks
           )


def buy_order_triggered_event_handler(event):
    print ("Event: %s" % str(event))
    if(event['transaction_type'] == 'B'):
        print event
    if (event['transaction_type'] == 'S'):
        print event
    # stop_loss_order_for_buy()
    # if (event['aa'] == 'aa'):
    # return


def event_handler_quote_update(message):
    print "Last Trade price" + str(message['ltp']) + " time " + str(datetime.now().time())

# order_buy_and_sell_niftyVWAP('7QQDdOIHNxatXDiRIHbyv2sG3J8QOozU7o8UYKmu','51fc5fe83c9282296b1d592be0678fd25ca4d6b8')
order_buy_and_sell_niftyVWAP('7QQDdOIHNxatXDiRIHbyv2sG3J8QOozU7o8UYKmu','9df872c1fac4b5962f421930a7458c46cd51a65a','banknifty17decfut')