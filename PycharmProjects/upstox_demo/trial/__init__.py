from upstox_api.api import *


s = Session('JMJueJYcG05yrycTa4tBX3zP5KGqOl2c8dAZ31Ay')
s.set_redirect_uri('http://127.0.0.0')
s.set_api_secret('on8l8gvped')


# use below url to login and get code
print (s.get_login_url())


# # code goes here
s.set_code ('bd2660401135803d826776b4bd21bf6f03e7031c')

# use code to generate access token
access_token = s.retrieve_access_token()

print access_token

