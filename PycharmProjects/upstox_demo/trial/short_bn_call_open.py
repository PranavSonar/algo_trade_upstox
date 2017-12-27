import calendar
import math
from datetime import datetime
from datetime import timedelta
from threading import Timer
from upstox_api.api import *

#banknifty17122125300ce
#banknifty year month date strikeprice ce/pe
u=''
banknifty_future=0.0
banknifty_open_price=0.0
banknifty_option_instru=''

def next_thursday():
    days_ahead = 3 - datetime.today().weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return datetime.today() + timedelta(days_ahead)

def fetch_open_prices():
    banknifty_future_full = u.get_live_feed(banknifty_future, LiveFeedType.Full)
    global banknifty_open_price
    banknifty_open_price = banknifty_future_full["open"]
    print "bank nifty open %s" % str(banknifty_open_price)

def get_banknifty_option_symbol():
    fetch_open_prices()
    strike_price=get_strike_price_for_ce_short()
    name = 'banknifty'
    year = str(datetime.today().year)
    year = year[-2:]
    month = datetime.today().month
    day=next_thursday().day
    name=name+year+str(month)+str(day)+'ce'
    name='banknifty17122125300ce'
    return name

# print get_banknifty_option_symbol()

def get_strike_price_for_ce_short():
    strike_price = banknifty_open_price + banknifty_open_price*0.006
    strike_price = (math.ceil(strike_price/100))*100
    print "Strike price: %s" % str(strike_price)
    return strike_price


def order_triggered(event):
    if (event['transaction_type'] == 'S'):
        sl = math.ceil(event['traded_price'] + event['traded_price']*0.5)
        print '####################### placing stop loss##################'
        print (u.place_order(TransactionType.Buy,  # transaction_type
                             banknifty_option_instru,  # instrument
                             40,  # quantity
                             OrderType.StopLossMarket,  # order_type
                             ProductType.Intraday,  # product_type
                             0.0,  # price
                             float(sl),  # trigger_price
                             0,  # disclosed_quantity
                             DurationType.DAY,  # duration
                             None,  # stop_loss
                             None,  # square_off
                             None)  # trailing_ticks
               )


def place_order():
    print "################ bank nifty ce write at open ###################"
    banknifty_option = u.get_live_feed(banknifty_option_instru, LiveFeedType.Full)
    banknifty_open_price_option = banknifty_option["open"]
    print "bank nifty open option %s" % str(banknifty_open_price_option)

    print (u.place_order(TransactionType.Sell,  # transaction_type
                         banknifty_option_instru,  # instrument
                         40,  # quantity
                         OrderType.Market,  # order_type
                         ProductType.Intraday,  # product_type
                         0.0,  # price
                         0.0,  # trigger_price
                         0,  # disclosed_quantity
                         DurationType.DAY,  # duration
                         None,  # stop_loss
                         None,  # square_off
                         None)  # trailing_ticks
           )


def short_call_away_from_bn(apiKey, accessToken):
    global u
    u = Upstox(apiKey, accessToken)
    u.get_master_contract('NSE_FO')  # get contracts for NSE FO

    u.set_on_trade_update(order_triggered)
    u.start_websocket(False)
    global banknifty_future
    banknifty_future = u.get_instrument_by_symbol('NSE_FO', 'banknifty17decfut')


    banknifty_option_symbol =  get_banknifty_option_symbol()

    global banknifty_option_instru
    banknifty_option_instru = u.get_instrument_by_symbol('NSE_FO', banknifty_option_symbol)

    place_order()



    # fetch_open_time = today.replace(day=today.day + 1, hour=12, minute=15, second=30, microsecond=0)
    # calc_price_time = today.replace(day=today.day + 1, hour=9, minute=15, second=4, microsecond=0)
    # sell_order_time = today.replace(day=today.day + 1, hour=9, minute=15, second=5, microsecond=0)
    #
    # delta_t_open = fetch_open_time - today
    # delta_t_calculation = calc_price_time - today
    # delta_t_sell_place = sell_order_time - today
    #
    # time_for_open_prices = delta_t_open.seconds + 1
    # time_for_calculation = delta_t_calculation.seconds + 1
    # time_for_sell = delta_t_sell_place.seconds + 1
    # open_price_timer = Timer(time_for_open_prices, fetch_open_prices)
    # open_price_timer.start()
    #




short_call_away_from_bn('7QQDdOIHNxatXDiRIHbyv2sG3J8QOozU7o8UYKmu','5ee31f0ba766d83b739b16ffbff6d740db8b50ab')
