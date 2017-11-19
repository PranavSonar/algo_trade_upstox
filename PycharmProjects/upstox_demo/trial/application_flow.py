from upstox_api.api import *
def event_handler_quote_update(message):
    print("Quote Update: %s" % str(message))

#Api key , access token
u = Upstox ('vsmym5Dcv13SJVZT0yhqA5lfXDHakUJt3ShWj5bd', '2711b9258be03ec5e381c9de36cd6a57b75c9af4')

# print (u.get_balance()) # get balance / margin limits
# print (u.get_profile()) # get profile
# print (u.get_holdings()) # get holdings
# print (u.get_positions()) # get positions

u.get_master_contract('MCX_FO') # get contracts for MCX FO


crudeoil = u.get_instrument_by_symbol('MCX_FO','crudeoilm17novfut')

r= u.get_live_feed(crudeoil, LiveFeedType.LTP)

print r
print r["close"]

# u.set_on_quote_update(event_handler_quote_update)
# u.subscribe(crudeoil, LiveFeedType.LTP)
# u.start_websocket(True)


print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%1%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print(
   u.place_order(TransactionType.Buy,  #transaction_type
              crudeoil,  #instrument
              10,  # quantity
              OrderType.Market,  # order_type
              ProductType.Intraday,  # product_type
              0.0,  # price
              None,  # trigger_price
              0,  # disclosed_quantity
              DurationType.DAY, # duration
              None, # stop_loss
              None, # square_off
              None )# trailing_ticks
   )

# for key, value in r.items() :
#     print (key, value)





# u.set_on_quote_update(event_handler_quote_update)

# u.subscribe(crudeoil, LiveFeedType.LTP)

# u.start_websocket(True)
