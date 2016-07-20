from stream_api import TwitterStreamAPI

api_key = "----"
api_secret = "----"
access_token = "-----"
access_secret = "---"

test = TwitterStreamAPI(api_key,api_secret,access_token,access_secret)
track=['partiu','#partiu','Oi','Boa tarde']
test.query(track)
