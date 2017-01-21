# -*- coding: UTF-8 -*-"
"""Extractor class to retrieve data from Foursquare.

# (c) J.Wirlino and A.Adativa
# Date Jan 14th 2017
# https://github.com/JosielWirlino/SocialCrawler

This file take all message error from response and translate to 
human version

more information: https://developer.foursquare.com/overview/responses
				  https://docs.python.org/3.1/howto/urllib2.html

"""

#ERRORS:

from termcolor import colored

CODE_ERROR = [
				[400,"BAD REQUEST"],
				[401,"The OAuth token was provided but was invalid."],
				[403,"The requested information cannot be viewed by the acting user, for example, because they \
						are not friends with the user whose date they are trying to read."],
				[404,"Endpoint does not exist."],
				[405,"[METHOD NOT ALLOWED] Attempting to use POST with a GET-only endpoint, or vice-versa."],
				[409,"[CONFLICT] The request could not be completed as it is. Use the information \
						 included in the response to modify the request and retry."],
				[500,"[INTERNAL SERVER ERROR] Foursquare's servers are unhappy. The request is probably \
					valid but needs to be retried later."]
			]


#ERRORTYPE DESCRIPTION
ERROR_TYPE = [
				["invalid_auth","OAuth token was not provided or was invalid."],

				["param_error","A required parameter was missing or a parameter was malformed. This is also used if the resource ID in the path is incorrect."],

				["endpoint_error","The requested path does not exist."],

				["not_authorized","Although authentication succeeded, the acting user is not allowed to see this information due to privacy restrictions."],

				["rate_limit_exceeded","Rate limit for this hour exceeded."],

				["deprecated","Something about this request is using deprecated functionality, or the response format may be about to change."],

				["server_error","Server is currently experiencing issues. Check status.foursquare.com for updates."],

				["other","Some other type of error occurred."]

			 ]

def parse_error(status_code, error_type):
	
	error_code = 0
	error_detail = 1
	error_type_detail = 0
	error_type_detail_msg = 1

	ret = False

	for error in CODE_ERROR:
		if error[error_code] == status_code:
			print(

					colored("ERROR CODE: \t["+str(error[error_code]) + "] \nERROR DETAIL: \t"+error[error_detail],"red")

				 )
			break
	for type_error in ERROR_TYPE:
		# print(type_error[error_type_detail])
		if type_error[error_type_detail] == error_type:
			print (
						colored("ERROR TYPE: \t["+str(type_error[error_type_detail]) + "] \nERROR MSG: \t"+type_error[error_type_detail_msg],"red")
					)
			break
	

	if error_type is "rate_limit_exceeded":
		ret = True
	
	return ret

# parse_error(600, "error_type")