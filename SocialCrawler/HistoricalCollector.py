#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# (c) J.Wirlino
# Date July 15th 2016
# https://github.com/JosielWirlino/TwitterSwarm4Square-DataMining

import tweepy
import time

'''    
Class responsible in get data (check-ins) from last week
'''
class HistoricalCollector:
	#Global variable to count the tweets received
	data_count = 0
	'''
	When instatiated must be pass all parameters.
	If only one is wrong return ERROR_PARAMETER_INVALID 
	'''
	def __init__(self, api_key=None, api_secret=None, acess_token=None, acess_secret=None):
		
		#set credentials

		self.api_key = api_key
		self.api_secret = api_secret
		self.acess_token = acess_token
		self.acess_secret = acess_secret

		#trying get access

		self.auth = tweepy.OAuthHandler( self.api_key, self.api_secret)
		self.auth.set_acess_token(self.acess_token, self.acess_secret)
		self.twitter_api = tweepy.API(self.auth)

	def 