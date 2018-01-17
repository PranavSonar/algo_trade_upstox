#CLL = current close - lowest low (14 periods)
#HLLL = highest high - lowest low
#%k= (CLL/HLL)*100  .... fast stocastics
# (sum of previous 3 CLL/sum of previous 3 HLLL)*100 >> %D or slow stocastics
#Signal line> simple average of previous 3 %D line
import threading
from datetime import timedelta, datetime

from upstox_api.api import Upstox, OHLCInterval

# to calculate stocastics
# 1 fetch last 20 candles and store them
# 2 calculate above things
# 3 after every 10 mins fetch new 10 min . Using prcandle and add it to above and recalculate things
#






u = Upstox('7QQDdOIHNxatXDiRIHbyv2sG3J8QOozU7o8UYKmu', '4e8532c96bf13efcc72648e594d8fe58ebbf5eee')

u.get_master_contract('NSE_FO')  # get contracts for NSE FO
banknifty_instu = u.get_instrument_by_symbol('NSE_FO', 'banknifty18janfut')


def fetch_previous_n_candles(n):
    bn = u.get_ohlc(banknifty_instu, OHLCInterval.Minute_10,
               (datetime.today() - timedelta(4)).date(), datetime.today().date())
    return bn[-n:]


bn_last_20 = fetch_previous_n_candles(20)
print bn_last_20
for bn in bn_last_20:
    print bn['open']
# banknifty_month_data = u.get_ohlc(banknifty_instu, OHLCInterval.Minute_10,
#                                   (datetime.today() - datetime.timedelta(30)).date(), datetime.today().date())