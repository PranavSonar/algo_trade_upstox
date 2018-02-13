# print "Last Trade price" +str(333) +" time "+ str(datetime.now().time())
#
# # print str(datetime.now().time())
import math
from datetime import datetime

nifty_open = 10201
india_vix_open = 14


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
    print 'buy_target: %s' % str(buy_target)
    print 'sl_for_buy: %s' % str(sl_for_buy)
    print 'sell_below: %s' % str(sell_below)
    print 'sell_target: %s' % str(sell_target)
    print 'sl_for_sell: %s' % str(sl_for_sell)


# calculate_target_and_sl()
def current_day():
    print datetime.today().weekday()
    print datetime.day(2017, 12, 2017).weekday()

    # current_day()

# print datetime.fromtimestamp(
#     1514454300000/1000
# ).strftime('%d/%m/%Y')
# print datetime.fromtimestamp(1514454300).date()


nifty_open = 10820
india_vix_open = 13.96
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

# calculate_target_and_sl()
today = datetime.today()
fetch_open_time =  today.replace(day=today.day +1, hour=4, minute=45, second=0, microsecond=500)
delta_t = fetch_open_time - today
time_for_open_prices = delta_t.seconds + 2
print "fetch open time: " + str(fetch_open_time)
print "delta t: " + str(delta_t)
print "today: " + str(today.date())
print "time_for_open_prices: " + str(time_for_open_prices)