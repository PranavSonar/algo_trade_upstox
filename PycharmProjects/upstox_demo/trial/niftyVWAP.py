from upstox_api.api import *
from datetime import datetime
from threading import Timer

#Api key , access token
u = Upstox ('JMJueJYcG05yrycTa4tBX3zP5KGqOl2c8dAZ31Ay', '1cc0d35294ab77715886a44eee604907c63de010')

u.get_master_contract('NSE_FO') # get contracts for NSE FO
u.get_master_contract('NSE_INDEX') # get contracts for NSE_INDEX


india_vix_nse_index = u.get_instrument_by_symbol('NSE_INDEX', 'INDIA_VIX')
nifty_nse_future = u.get_instrument_by_symbol('NSE_FO', 'nifty17decfut')

w=datetime.today()

x=w.replace(day=w.day + 1, hour=9, minute=14, second=1, microsecond=0)
y=w.replace(day=w.day + 1, hour=9, minute=15, second=10, microsecond=0)
z=w.replace(day=w.day + 1, hour=9, minute=15, second=15, microsecond=0)

delta_t= x - w
delta_t_calculation = y - w
delta_t_order_place = z - w
time_for_open_prices= delta_t.seconds + 1
time_for_calculation = delta_t_calculation.seconds + 1
time_for_order = delta_t_order_place.seconds+1

india_vix_open=0
nifty_o= 0
buy_above=0
buy_target=0
sl_for_sell=0
sl_for_buy=0
sell_target=0

def fetch_open_prices():
    india_vix = u.get_live_feed(india_vix_nse_index, LiveFeedType.Full)
    global india_vix_open
    india_vix_open = india_vix["open"]
    nifty_nse_future_full = u.get_live_feed(nifty_nse_future, LiveFeedType.Full)
    global nifty_open
    nifty_open = nifty_nse_future_full["open"]



def calculate_target_and_sl():
    first_sd = nifty_open * india_vix_open * 0.00104684784518
    global buy_above
    buy_above = 0.236 * first_sd + nifty_open
    global buy_target
    buy_target = 0.382 * first_sd + nifty_open
    global sl_for_buy
    sl_for_buy = nifty_open - 1
    global sell_below
    sell_below = nifty_open - 0.236 * first_sd
    global sell_target
    sell_target = nifty_open - 0.382 * first_sd
    global sl_for_sell
    sl_for_sell = nifty_open + 1
    print 'buy_above : '  + buy_above
    print 'buy_target : '  + buy_target
    print 'sl_for_sell : '  + sl_for_sell
    print 'sl_for_buy : '  + sl_for_buy
    print 'sell_target : '  + sell_target




def place_nifty_buy_order():
    u.place_order(TransactionType.Buy,  # transaction_type
                  nifty_nse_future,  # instrument
                  1,  # quantity
                  OrderType.Limit,  # order_type
                  ProductType.Intraday,  # product_type
                  buy_above,  # price
                  None,  # trigger_price
                  0,  # disclosed_quantity
                  DurationType.DAY,  # duration
                  sl_for_buy,  # stop_loss
                  buy_target,  # square_off
                  None)  # trailing_ticks




open_price_timer = Timer(time_for_open_prices, fetch_open_prices)
open_price_timer.start()

target_set_timer = Timer(time_for_calculation, calculate_target_and_sl)
target_set_timer.start()

place_order_set_timer = Timer(time_for_order, place_nifty_buy_order)
place_order_set_timer.start()