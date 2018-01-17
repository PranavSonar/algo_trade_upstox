from datetime import timedelta

from upstox_api.api import *





u = Upstox('7QQDdOIHNxatXDiRIHbyv2sG3J8QOozU7o8UYKmu', '4e8532c96bf13efcc72648e594d8fe58ebbf5eee')

u.get_master_contract('NSE_FO')  # get contracts for NSE FO
# u.get_master_contract('NSE_INDEX')  # get contracts for NSE_INDEX
# t= u.get_ohlc(u.get_instrument_by_symbol('NSE_FO', 'binknifty18janfut'), OHLCInterval.Minute_10, datetime.today().date(), datetime.today().date())
# print u
# t=  u.search_instruments('NSE_INDEX','NIFTY_50')
# print t
# for i in t:
# print t['name']
banknifty_instu = u.get_instrument_by_symbol('NSE_FO', 'banknifty18janfut')
# t = u.get_ohlc(banknifty_instu, OHLCInterval.Minute_10,
#                datetime.strptime('26/12/2017', '%d/%m/%Y').date(), datetime.strptime('26/12/2017', '%d/%m/%Y').date())
# print t[0]

banknifty_month_data = u.get_ohlc(banknifty_instu, OHLCInterval.Minute_10,
                                  (datetime.today() - timedelta(30)).date(), datetime.today().date())


def long_bn_here(bn):
    if (datetime.fromtimestamp((int(bn['timestamp']) / 1000)).strftime('%H:%M:%S') == '09:25:00'):
        bn[high]

    pass

def short_bn_here(bn):
    pass
for bn in banknifty_month_data:
    if (datetime.fromtimestamp((int(bn['timestamp']) / 1000)).strftime('%H:%M:%S') == '09:15:00'):
        if (bn['open']-bn['close'] >0):
            short_bn_here(bn)
        else:
            long_bn_here(bn)


#
#     pass
