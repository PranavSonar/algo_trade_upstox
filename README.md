# algo_trade_upstox
Scripts for algo trading for upstox apis


api key: b729ef456e66ee0e6f996720489a3c153d52fb32
api secret:   2vf3l4vcgi

// get the code
https://api.upstox.com/index/dialog/authorize?apiKey=vsmym5Dcv13SJVZT0yhqA5lfXDHakUJt3ShWj5bd&redirect_uri=http://127.0.0.1&response_type=code



//below is not saved in postman
//get the access token using below thing
curl \
-u vsmym5Dcv13SJVZT0yhqA5lfXDHakUJt3ShWj5bd:2vf3l4vcgi \
-H 'Content-Type: application/json' \
-H 'x-api-key: vsmym5Dcv13SJVZT0yhqA5lfXDHakUJt3ShWj5bd' \
-d '{"code" : "b729ef456e66ee0e6f996720489a3c153d52fb32", "grant_type" : "authorization_code", "redirect_uri" : "http://127.0.0.1"}' \
-X POST 'https://api.upstox.com/index/oauth/token'

696bb6510428e9120ed338ba1b1a159c611a579c


// below is saved in postman
// get basic user information
curl \
-H 'authorization: Bearer f5e8644720e2060eb062ae7f803ae80f2c5092c0' \
-H 'x-api-key:7QQDdOIHNxatXDiRIHbyv2sG3J8QOozU7o8UYKmu ' \
-X GET 'https://api.upstox.com/index/profile'


//


curl \
-H 'authorization: Bearer 696bb6510428e9120ed338ba1b1a159c611a579c' \
-H 'x-api-key: {your_api_key}' \
-X GET 'https://api.upstox.com/live/profile/balance'

cd /System/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7