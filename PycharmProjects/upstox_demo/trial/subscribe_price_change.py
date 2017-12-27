from upstox_api.api import *
from datetime import datetime

def event_handler_quote_update(message):
    print "Message: " + str(message) + " Time: " + str(datetime.now().time())

# Api key , access token
u = Upstox('JMJueJYcG05yrycTa4tBX3zP5KGqOl2c8dAZ31Ay', '62ff9fba37e042744c14a1f35bc04cbc46188bc3')

u.get_master_contract('MCX_FO')  # get contracts for MCX FO
crude_oil_instrument = u.get_instrument_by_symbol('MCX_FO', 'crudeoilm17decfut')
u.set_on_quote_update(event_handler_quote_update)
u.unsubscribe(crude_oil_instrument, LiveFeedType.LTP)
u.subscribe(crude_oil_instrument, LiveFeedType.LTP)
u.start_websocket(False)



