#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# (c) J.Wirlino
# Date July 15th 2016
# https://github.com/JosielWirlino/SocialCrawler
from termcolor import colored
import tweepy
import sys
'''    
Class responsible in get data from 4Square from a checking data or
4Square dataset of the last week
'''
class Collector:
	#Global variable to count the tweets received
	stored_data_count = 0
	stream_data_count = 0
	'''
	When instatiated must be pass all parameters.
	If only one is wrong return ERROR_PARAMETER_INVALID 

	@param api_key
	@param api_secret
	@access_token
	@access_secret
	'''
	def __init__(self, api_key=None, api_secret=None, access_token=None, access_secret=None):
		
		if( api_key is  None or api_secret is  None or access_token is  None or access_secret is  None ):
			print (colored('Error: Any parameter can not be None','red'))


		#setting all parameters
		self.api_key = api_key
		self.api_secret = api_secret
		self.access_token = access_token
		self.access_secret = access_secret

		#requesting authentication

		self.auth = tweepy.OAuthHandler(self.api_key, self.api_secret)
		self.auth.set_access_token(self.access_token,self.access_secret)
		self.twitter = tweepy.API(self.auth)



	'''
	Method to get data stored in Twitter dataset
	-There are two ways to get data: stored and stream
	This method use Cursor to get all data
	#see http://tweepy.readthedocs.io/en/v3.5.0/cursor_tutorial.html

	@param query string content your consult
	@param since begin date to start collect data
	@param until end date of the tweets to be collected
	@city specific city data
	@param geocode specific region of the city
	@param mode define if you want items or page
	'''
	def getStoredData( self, query=None, since=None, until=None, 
					   city=None, geocode=None, save_path = None,
					   result_limits='infinite', mode='items'):
		if( query is None or since is None or until is None or save_path is None):
			print (colored('Error: query, since, until, and save_path parameters can not be None','red'))
			sys.exit()
		
		try:
			if( city is not None ):
				log_file = open(save_path+'log_from_'+city.replace(" ","")+since+'__'+until+'.tsv','a',encoding='utf8')
			else:
				log_file = open(save_path+'log_'+since+'__'+until+'.tsv','a',encoding='utf8')
		except IOError:
			print colored('Cound not open file!')
		#check if the query is about a specific city	
		if( city is None ):
			if(mode=='items'):
				results = tweepy.Cursor(self.twitter.search,
									q=query,
									since=since,
									until=until).items
			else:
				results = tweepy.Cursor(self.twitter.search,
									q=query,
									since=since,
									until=until).pages
		else:
			if(mode=='items'):
				results = tweepy.Cursor(self.twitter.search,
									q=query,
									since=since,
									until=until,
									geocode=geocode).items
			else:
				results = tweepy.Cursor(self.twitter.search,
									q=query,
									since=since,
									until=until,
									geocode=geocode).pages
		while True:
			try:
				tweet = results.next()
				self.stored_data_count+=1

				print (colored(self.tweet_count,'red') , colored(city,'green'), colored(tweet.created_at,'red'), tweet.text)
				print ('\n')

				log_file.write(str(self.stored_data_count)+'\t' + str(tweet.user.id)+ '\t' + str(city) +'\t' + str(tweet.created_at) + '\t' + str(tweet.text.encode('utf-8')) +'\n' )
			
			#wait 15 minute to search again
			#https://dev.twitter.com/rest/public/rate-limiting
			except tweepy.TweepError:
				print colored('Twitter API rate limit. Wait 15 minutes to request again.\n ','red')
				time.sleep(900)
				continue
			except StopIteration:
				break
