from threading import Timer

from upstox_api.api import *

# Stragegy
# wait for banknifty to open
# wait for 5 min candle to form.
# till 9:45 if 5 mins range is broken then buy above high or sell below low.
# Target is length of candle. SL is high or low of candle

# Api key , access token
u = ""
bn_5_min_open = 0.0
bn_5_min_close = 0.0
bn_5_min_high = 0.0
bn_5_min_low = 0.0
bank_nifty_fut_instu = ''

buy_order = 0
sell_order = 0


def place_order_for_sell():
    print "####################### Sell order OCO and limit ###################"
    global sell_order
    sell_order = u.place_order(TransactionType.Sell,  # transaction_type
                               bank_nifty_fut_instu,  # instrument
                               bank_nifty_fut_instu['lot_size'],  # quantity
                               OrderType.StopLossLimit,  # order_type
                               ProductType.OneCancelsOther,  # product_type
                               float(bn_5_min_low - 0.1),  # price
                               float(bn_5_min_low),  # trigger_price
                               0,  # disclosed_quantity
                               DurationType.DAY,  # duration
                               float(bn_5_min_high + 1),  # stop_loss
                               float(2 * bn_5_min_high - bn_5_min_low - 1),  # square_off
                               None)  # trailing_ticks
    print sell_order


def place_order_for_buy():
    print "####################### Buy order OCO and limit ###################"
    global buy_order
    buy_order = u.place_order(TransactionType.Buy,  # transaction_type
                              bank_nifty_fut_instu,  # instrument
                              bank_nifty_fut_instu['lot_size'],  # quantity
                              OrderType.StopLossLimit,  # order_type
                              ProductType.OneCancelsOther,  # product_type
                              float(bn_5_min_high + 0.1),  # price
                              float(bn_5_min_high),  # trigger_price
                              0,  # disclosed_quantity
                              DurationType.DAY,  # duration
                              float(bn_5_min_low - 1),  # stop_loss
                              float(2 * bn_5_min_high - bn_5_min_low - 1),  # square_off
                              None)  # trailing_ticks

    print buy_order


def update_ohlc_5min():
    global bn_5_min_open
    global bn_5_min_close
    global bn_5_min_high
    global bn_5_min_low
    ohlc = u.get_ohlc(u.get_instrument_by_symbol('NSE_FO', bank_nifty_fut_instu), OHLCInterval.Minute_5,
                      datetime.today().date(),
                      datetime.today().date())
    print "Bank nifty OHLC>>>>>>>>>"
    print ohlc
    bn_5_min_open = ohlc['open']
    bn_5_min_close = ohlc['close']
    bn_5_min_high = ohlc['high']
    bn_5_min_low = ohlc['low']
    if bn_5_min_open > bn_5_min_close & (bn_5_min_open - bn_5_min_close) >= 20:
        place_order_for_buy()
    else:
        place_order_for_sell()


def cancel_order_if_not_traded():
    buy_order_id = buy_order['order_id']
    u.cancel_order(buy_order['order_id'], sell_order['order_id'])
    pass


def order_buy_or_sell_bn_range_breakout(upstox, symbol_string):
    global u
    u = upstox
    global bank_nifty_fut_instu
    bank_nifty_fut_instu = upstox.get_instrument_by_symbol('NSE_FO', symbol_string)
    print bank_nifty_fut_instu

    today = datetime.today()

    fetch_open_time = today.replace(day=today.day + 1, hour=9, minute=20, second=0, microsecond=100)

    delta_t = fetch_open_time - today
    time_for_open_prices = delta_t.seconds + 1
    open_price_timer = Timer(time_for_open_prices, update_ohlc_5min)
    open_price_timer.start()

    fetch_cancel_order_trade_time = today.replace(day=today.day + 1, hour=9, minute=45, second=0, microsecond=100)

    delta_cancel_trade = fetch_cancel_order_trade_time - today
    time_to_cancel = delta_cancel_trade.seconds + 1
    open_price_timer = Timer(time_to_cancel, cancel_order_if_not_traded)
    open_price_timer.start()


def buy_order_triggered_event_handler(event):
    print ("Event: %s" % str(event))
    if (event['transaction_type'] == 'B'):
        print event
    if (event['transaction_type'] == 'S'):
        print event
        # stop_loss_order_for_buy()
        # if (event['aa'] == 'aa'):
        # return


def event_handler_quote_update(message):
    print "Last Trade price" + str(message['ltp']) + " time " + str(datetime.now().time())


# order_buy_and_sell_niftyVWAP('7QQDdOIHNxatXDiRIHbyv2sG3J8QOozU7o8UYKmu','51fc5fe83c9282296b1d592be0678fd25ca4d6b8')
p = Upstox('7QQDdOIHNxatXDiRIHbyv2sG3J8QOozU7o8UYKmu', '9df872c1fac4b5962f421930a7458c46cd51a65a')

p.get_master_contract('NSE_FO')  # get contracts for NSE FO
p.get_master_contract('NSE_INDEX')  # get contracts for NSE_INDEX

order_buy_or_sell_bn_range_breakout(p, 'banknifty17decfut')
