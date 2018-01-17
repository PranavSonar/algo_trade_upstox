# CLL = current close - lowest low (14 periods)
# HLLL = highest high - lowest low
# %k= (CLL/HLL)*100  .... fast stocastics
# (sum of previous 3 CLL/sum of previous 3 HLLL)*100 >> %D or slow stocastics
# Signal line> simple average of previous 3 %D line
from datetime import timedelta, datetime

from upstox_api.api import *

from formulas.pivot_points import calculate_pivot_points


# to calculate stocastics
# 1 fetch last 20 candles and store them
# 2 calculate above things
# 3 after every 10 mins fetch new 10 min . Using prcandle and add it to above and recalculate things
#

# first calculate pivot points



########################################################################################################################

def calculate_percent_d(cll, hlll):
    per_d = []
    count = 0
    while count < 3:
        perd = ((cll[count] + cll[count + 1] + cll[count + 2]) / 3) / (
        (hlll[count] + hlll[count + 1] + hlll[count + 2]) / 3)
        perd = perd * 100
        per_d.insert(count, perd)
        count = count + 1
    return per_d


def calculate_stocastics():
    last_20_candles = upstox.get_ohlc(banknifty_instu, OHLCInterval.Minute_10,
                                      (datetime.today() - timedelta(5)).date(), datetime.today().date())
    last_20_candles = last_20_candles[-20:]
    first_14 = last_20_candles[14:0]
    # print first_14[0]
    # highest_high_14, lowest_low_14 = highest_high_and_lowest_low(first_14)
    # cll = first_14[13]-lowest_low_14
    # hlll = highest_high_14-lowest_low_14
    # per_k = (cll/hlll)*100
    # per_d=0
    cll, hlll = get_6_cll_hll(last_20_candles)
    # print 'CLL'
    # print cll
    # print 'HLLL'
    # print hlll
    per_d = calculate_percent_d(cll, hlll)
    return per_d

def get_6_cll_hll(last_20_candles):
    cll = []
    hlll = []
    count = 0
    while (count < 7):
        print '############################## count: ' + str(count)
        fourteen_candles = last_20_candles[count:(14 + count)]
        highest_high_14, lowest_low_14 = highest_high_and_lowest_low(fourteen_candles)
        cll.insert(count, fourteen_candles[13]['close'] - lowest_low_14)
        hlll.insert(count, highest_high_14 - lowest_low_14)
        count = count + 1
    return cll, hlll


def highest_high_and_lowest_low(first_14):
    lowest_low_14 = first_14[0]['low']
    highest_high_14 = first_14[0]['high']
    for f in first_14:
        if (lowest_low_14 > f['low']):
            lowest_low_14 = f['low']
        if (highest_high_14 < f['high']):
            highest_high_14 = f['high']
    print "highest" + str(highest_high_14)
    print "lowest" + str(lowest_low_14)
    return highest_high_14, lowest_low_14


def place_buy_order():
    print "####################### Buy order CO and limit ###################"
    print (upstox.place_order(TransactionType.Buy,  # transaction_type
                         banknifty_instu,  # instrument
                         int(banknifty_instu[9]),  # quantity
                         OrderType.Market,  # order_type
                         ProductType.CoverOrder,  # product_type
                         None,  # price
                         0.0,  # trigger_price
                         0,  # disclosed_quantity
                         DurationType.DAY,  # duration
                         50.0,  # stop_loss
                         70.0,  # square_off
                         None)  # trailing_ticks
           )
    upstox.unsubscribe(banknifty_instu, LiveFeedType.LTP)


def check_for_oversold_then_buy():
    per_d = calculate_stocastics()
    if(per_d[2]<25):
        place_buy_order()


def place_sell_order():
    print "####################### Sell order CO and limit ###################"
    print (upstox.place_order(TransactionType.Sell,  # transaction_type
                         banknifty_instu,  # instrument
                         int(banknifty_instu[9]),  # quantity
                         OrderType.Market,  # order_type
                         ProductType.CoverOrder,  # product_type
                         None,  # price
                         0.0,  # trigger_price
                         0,  # disclosed_quantity
                         DurationType.DAY,  # duration
                         50.0,  # stop_loss
                         70.0,  # square_off
                         None)  # trailing_ticks
           )
    upstox.unsubscribe(banknifty_instu, LiveFeedType.LTP)
    upstox.unsubscribe(banknifty_instu, LiveFeedType.LTP)
    pass


def check_for_overbought_then_sell():
    per_d = calculate_stocastics()
    if (per_d[2] < 70):
        place_sell_order()


def banknifty_price_change(message):
    if (message['ltp'] >= (pivots['pp_r1'] - 6) and message['ltp'] <= (pivots['pp_r1'] + 6)):
        check_for_overbought_then_sell()
    elif (message['ltp'] >= (pivots['pp_r2'] - 6) and message['ltp'] <= (pivots['pp_r2'] + 6)):
        check_for_overbought_then_sell()
    elif (message['ltp'] >= (pivots['pp_s1'] - 6) and message['ltp'] <= (pivots['pp_s1'] + 6)):
        check_for_oversold_then_buy()
    elif (message['ltp'] >= (pivots['pp_s2'] - 6) and message['ltp'] <= (pivots['pp_s2'] + 6)):
        check_for_oversold_then_buy()
        pass


########################################################################################################################

# get previous day high low and close
def previous_day_data_ohlc():
    # this takes close of last 15 mins candle instead of close provided by exchange
    banknifty_daily_data = upstox.get_ohlc(banknifty_instu, OHLCInterval.Day_1,
                                           (datetime.today() - timedelta(5)).date(), datetime.today().date())
    day = 2
    time_last_10min_candle = (banknifty_daily_data[len(banknifty_daily_data) - day]['timestamp'] + 55200000) / 1000
    last_candle_close = upstox.get_ohlc(banknifty_instu, OHLCInterval.Minute_10,
                                        (datetime.fromtimestamp(time_last_10min_candle).date()),
                                        (datetime.fromtimestamp(time_last_10min_candle).date()))
    ohlc = {}
    ohlc['high'] = banknifty_daily_data[len(banknifty_daily_data) - day]['high']
    ohlc['low'] = banknifty_daily_data[len(banknifty_daily_data) - day]['low']
    ohlc['open'] = banknifty_daily_data[len(banknifty_daily_data) - day]['open']
    ohlc['close'] = last_candle_close[len(last_candle_close) - 1]['close']
    return ohlc


########################################################################################################################


########## main function #############
upstox = Upstox('7QQDdOIHNxatXDiRIHbyv2sG3J8QOozU7o8UYKmu', 'f5e8644720e2060eb062ae7f803ae80f2c5092c0')
upstox.get_master_contract('NSE_FO')  # get contracts for NSE FO
banknifty_instu = upstox.get_instrument_by_symbol('NSE_FO', 'banknifty18janfut')
# upstox.get_


bn_prev_day_data = previous_day_data_ohlc()
# calculate pivot points
global pivots
pivots = calculate_pivot_points(bn_prev_day_data['high'], bn_prev_day_data['low'], bn_prev_day_data['close'])

upstox.set_on_quote_update(banknifty_price_change)
upstox.unsubscribe(banknifty_instu, LiveFeedType.LTP)
upstox.subscribe(banknifty_instu, LiveFeedType.LTP)
upstox.start_websocket(False)
