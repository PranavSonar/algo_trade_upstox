banknifty_month_data = u.get_ohlc(banknifty_instu, OHLCInterval.Minute_10,
                                  (datetime.today() - timedelta(30)).date(), datetime.today().date())