from stream_api import TwitterStreamAPI

api_key = "udF1vZod9mIWADiwCS5GwMjNI"
api_secret = "omR4g3tfFciQvgraNHnL4ur2cOo3x7viGdBypog5EdNwnK1NZh"
access_token = "4717654877-x2rcMWisECAD0peOEvmFRANLQnKUMICdMvh1HCJ"
access_secret = "pK7CBPJHFXgSKZNrg2ohibNWRQS0sNX0cbXIcSfcL6guB"

test = TwitterStreamAPI(api_key,api_secret,access_token,access_secret)
track=['partiu','#partiu','Oi','Boa tarde']
test.query(track)