from upstox_api.api import *


s = Session('JMJueJYcG05yrycTa4tBX3zP5KGqOl2c8dAZ31Ay')
s.set_redirect_uri('http://127.0.0.0')
s.set_api_secret('on8l8gvped')


# use below url to login and get code
print (s.get_login_url())


# # code goes here
s.set_code ('a99652b595498b0e9f3d6a5d2762528e169d82cb')

# use code to generate access token
access_token = s.retrieve_access_token()

print access_token

