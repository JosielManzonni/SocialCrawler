#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# (c) Wirlino

import json
import tweepy
import sys
class StreamListenerHandler(tweepy.StreamListener):
	def on_data(self,data):
		j = json.loads(data)
		print j["user"]["id"],j["user"]["lang"]
		# print (str(data.created_at) + ' '+data.user.id+ ' '+ data.tex+ ' '+data.city)
		return True
	def on_error(self,status):
		print(status)

class TwitterStreamAPI:
	'''
	When instatiated must be pass all parameters.
	If only one is wrong return ERROR_PARAMETER_INVALID 
	'''
	def __init__(self, api_key=None, api_secret=None,access_token=None,access_secret=None):
		#set OAuth
		self.auth = tweepy.OAuthHandler(api_key,api_secret)
		self.auth.set_access_token(access_token,access_secret)
		self.listenerhandler = StreamListenerHandler()

	
	'''
	Query using track parameters
	'''
	def query(self,trackv=None):
		self.streamdata=tweepy.Stream(self.auth,self.listenerhandler)
		self.streamdata.filter(track=trackv)