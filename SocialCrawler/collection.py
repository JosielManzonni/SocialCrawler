
'''    
Class responsible in get data from 4Square from a checking data or
4Square dataset of the last week
'''
class CollectorHistorical:
	#Global variable to count the tweets received
	data_count = 0
	'''
	When instatiated must be pass all parameters.
	If only one is wrong return ERROR_PARAMETER_INVALID 
	'''
	def __init__(self, api_key=None, api_secret=None, acess_token=None, acess_secret=None):
		self.api_key = api_key
		self.api_secret = api_secret
		self.acess_token = acess_token
		self.acess_secret = acess_secret
	def 