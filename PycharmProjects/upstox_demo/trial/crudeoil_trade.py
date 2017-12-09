from upstox_api.api import *
from datetime import datetime
from threading import Timer
import math

#Api key , access token
u = Upstox ('JMJueJYcG05yrycTa4tBX3zP5KGqOl2c8dAZ31Ay', '6f8a3953ec1da31059c9292d20a38e0f538ff725')

u.get_master_contract('MCX_FO') # get contracts for MCX FO


crude_oil_instrument = u.get_instrument_by_symbol('MCX_FO', 'crudeoilm17decfut')
# r= u.get_live_feed(crue_oil_instrument, LiveFeedType.LTP)

# def event_handler_quote_update(message):
#     print "Last Trade price: %s" % str(message['ltp'])
#     print("Quote Update: %s" % str(message))

today=datetime.today()

fetch_open_time=today.replace(day=today.day + 1, hour=10, minute=0, second=10, microsecond=0)
calculate_prices_time=today.replace(day=today.day + 1, hour=10, minute=0, second=20, microsecond=0)
buy_order_time=today.replace(day=today.day + 1, hour=10, minute=0, second=30, microsecond=0)

previous_day_crude_open = 0
previous_day_crude_high = 0
previous_day_crude_low = 0
previous_day_crude_close = 0

delta_t= fetch_open_time - today
delta_t_calculation = calculate_prices_time - today
delta_t_order_place = buy_order_time - today
time_for_open_prices= delta_t.seconds + 1
time_for_calculation = delta_t_calculation.seconds + 1
time_for_order = delta_t_order_place.seconds+1


buy_above=0
buy_target=0
sl_for_buy=0
sell_below=0
sell_target=0
sl_for_sell=0

crudeoil_open=0;

def fetch_open_prices():
    crudeoil_future_full = u.get_live_feed(crude_oil_instrument, LiveFeedType.Full)
    global crudeoil_open
    crudeoil_open = crudeoil_future_full["open"]
    print "crudeoil open"
    print crudeoil_open


def calculate_target_and_sl():
    first_sd = crudeoil_open * 0.01360902198734
    global buy_above
    buy_above = 0.236 * first_sd + crudeoil_open
    buy_above = math.ceil(buy_above)
    global buy_target
    buy_target = 0.382 * first_sd + crudeoil_open
    buy_target = math.ceil(buy_target)
    global sl_for_buy
    sl_for_buy = crudeoil_open - 1
    sl_for_buy = math.ceil(sl_for_buy)
    global sell_below
    sell_below = crudeoil_open - 0.236 * first_sd
    sell_below = math.ceil(sell_below)
    global sell_target
    sell_target = crudeoil_open - 0.382 * first_sd
    sell_target=math.ceil(sell_target)
    global sl_for_sell
    sl_for_sell = crudeoil_open + 1
    sl_for_sell = math.ceil(sl_for_sell)
    print buy_above
    print buy_target
    print sl_for_buy
    print sell_below
    print sell_target
    print sl_for_sell

fetch_open_prices()
calculate_target_and_sl()

def place_crude_buy_order():
    print "####################### Buy order ###################"
    print (u.place_order(TransactionType.Buy,  # transaction_type
                  crude_oil_instrument,  # instrument
                  1,  # quantity
                  OrderType.StopLossMarket,  # order_type
                  ProductType.Intraday,  # product_type
                  0.0,  # price
                  float(buy_above),  # trigger_price
                  0,  # disclosed_quantity
                  DurationType.DAY,  # duration
                  0.0,  # stop_loss
                  0.0,  # square_off
                  None)  # trailing_ticks
           )

def place_crude_buy_target_order():
    print "####################### Buy target order ###################"
    print (u.place_order(TransactionType.Buy,  # transaction_type
                  crude_oil_instrument,  # instrument
                  1,  # quantity
                  OrderType.StopLossMarket,  # order_type
                  ProductType.Intraday,  # product_type
                  0.0,  # price
                  float(buy_target),  # trigger_price
                  0,  # disclosed_quantity
                  DurationType.DAY,  # duration
                  0.0,  # stop_loss
                  0.0,  # square_off
                  None)  # trailing_ticks
           )

def stop_loss_order_for_buy():
    print "####################### stop loss for buy ###################"
    print (u.place_order(TransactionType.Sell,  # transaction_type
                         crude_oil_instrument,  # instrument
                         1,  # quantity
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

def place_crude_sell_order():
    print "####################### Sell order ###################"
    u.place_order(TransactionType.Sell,  # transaction_type
                  crude_oil_instrument,  # instrument
                  1,  # quantity
                  OrderType.Limit,  # order_type
                  ProductType.Intraday,  # product_type
                  float(sell_below),  # price
                  None,  # trigger_price
                  0,  # disclosed_quantity
                  DurationType.DAY,  # duration
                  None,  # stop_loss
                  None,  # square_off
                  None)  # trailing_ticks

def place_crude_sell_target_order():
    print "####################### Sell target order ###################"
    u.place_order(TransactionType.Buy,  # transaction_type
                  crude_oil_instrument,  # instrument
                  1,  # quantity
                  OrderType.Limit,  # order_type
                  ProductType.Intraday,  # product_type
                  float(sell_target),  # price
                  None,  # trigger_price
                  0,  # disclosed_quantity
                  DurationType.DAY,  # duration
                  None,  # stop_loss
                  None,  # square_off
                  None)  # trailing_ticks

def stop_loss_order_for_sell():
    print "####################### stop loss for sell ###################"
    print (u.place_order(TransactionType.Buy,  # transaction_type
                         crude_oil_instrument,  # instrument
                         1,  # quantity
                         OrderType.StopLossMarket,  # order_type
                         ProductType.Intraday,  # product_type
                         0.0,  # price
                         float(sl_for_sell),  # trigger_price
                         0,  # disclosed_quantity
                         DurationType.DAY,  # duration
                         None,  # stop_loss
                         None,  # square_off
                         None)  # trailing_ticks
           )

def buy_order_triggered_event_handler (event):
    print ("Event: %s" % str(event))
    stop_loss_order_for_buy()
    # if (event['aa'] == 'aa'):
    # return
