from threading import Timer

from upstox_api.api import *  # Api key , access token


u = ''
instrument_to_be_traded=''

def normal_sell_at_open(instu):
    print "####################### Sell at open ###################"
    print (u.place_order(TransactionType.Sell,  # transaction_type
                     instu,  # instrument
                     instu['quantity'],  # quantity
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


def order_buy_and_sell_niftyVWAP(apiKey, accessToken,contract_string_value):
    global u
    u = Upstox(apiKey, accessToken)
    u.get_master_contract('NSE_FO')  # get contracts for NSE FO
    global instrument_to_be_traded
    instrument_to_be_traded = u.get_instrument_by_symbol('NSE_FO', contract_string_value)

    today = datetime.today()

    place_order_time = today.replace(day=today.day + 1, hour=9, minute=15, second=0, microsecond=500)
    delta_t = place_order_time - today
    order_place_time = delta_t.seconds + 1
    open_price_timer = Timer(order_place_time, normal_sell_at_open)
    open_price_timer.start()

nifty_instu = u.get_instrument_by_symbol('NSE_FO', 'nifty17decfut')
instu = u.get_instrument_by_symbol('NSE_FO','ssss')
normal_sell_at_open(nifty_instu)
normal_sell_at_open(instu)