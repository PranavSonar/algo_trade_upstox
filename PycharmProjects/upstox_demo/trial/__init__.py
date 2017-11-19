from upstox_api.api import *


s = Session('vsmym5Dcv13SJVZT0yhqA5lfXDHakUJt3ShWj5bd')
s.set_redirect_uri('http://127.0.0.1')
s.set_api_secret('2vf3l4vcgi')


# use below url to login and get code
print (s.get_login_url())


# # code goes here
s.set_code ('ea994b10d7afa24a6c0753754f28d46ec73f0bf8')

# use code to generate access token
access_token = s.retrieve_access_token()

print access_token

