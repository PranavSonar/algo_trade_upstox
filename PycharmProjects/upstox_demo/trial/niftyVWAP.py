from upstox_api.api import *

#Api key , access token
u = Upstox ('vsmym5Dcv13SJVZT0yhqA5lfXDHakUJt3ShWj5bd', '8fb958b52437c680083fbff877f05057be42d848')

u.get_master_contract('NSE_FO') # get contracts for NSE FO
u.get_master_contract('NSE_INDEX') # get contracts for NSE_INDEX


india_vix_nse_index = u.get_instrument_by_symbol('NSE_INDEX', 'INDIA_VIX')
nifty_nse_future = u.get_instrument_by_symbol('NSE_FO', 'nifty17novfut')


india_vix = u.get_live_feed(india_vix_nse_index, LiveFeedType.Full)
india_vix_open = india_vix["open"]
nifty_nse_future_full = u.get_live_feed(nifty_nse_future, LiveFeedType.Full)
nifty_open = nifty_nse_future_full["open"]


#####################################################
# Formula to calculate nifty buy and target price   #
#####################################################
