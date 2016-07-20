#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# (c) J.Wirlino and A.Adativa
# Date July 15th 2016
# https://github.com/JosielWirlino/SocialCrawler
from termcolor import colored
import tweepy
import json
import sys
import time
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
			print (colored('Cound not open file!'))
		#check if the query is about a specific city	
		if( city is None ):
			if(mode=='items'):
				results = tweepy.Cursor(self.twitter.search,
									q=query,
									since=since,
									until=until).items()
			else:
				results = tweepy.Cursor(self.twitter.search,
									q=query,
									since=since,
									until=until).pages()
		else:
			if(mode=='items'):
				results = tweepy.Cursor(self.twitter.search,
									q=query,
									since=since,
									until=until,
									geocode=geocode).items()
			else:
				results = tweepy.Cursor(self.twitter.search,
									q=query,
									since=since,
									until=until,
									geocode=geocode).pages()
		while True:
			try:
				tweet = results.next()
				self.stored_data_count+=1

				print (colored(self.stored_data_count,'red') , colored(city,'green'), colored(tweet.created_at,'red'), tweet.text)
				# print ('\n')

				log_file.write(str(self.stored_data_count)+'\t' + str(tweet.user.id)+ '\t' + str(city) +'\t' + str(tweet.created_at) + '\t' + str(tweet.text.encode('utf-8')) +'\n' )
			
			#wait 15 minute to search again
			#https://dev.twitter.com/rest/public/rate-limiting
			except tweepy.TweepError:
				print('\n')
				print (colored('Twitter API rate limit. Wait 15 minutes to request again.\n ','red'))
				time.sleep(900)
				continue
			except StopIteration:
				break
		#when arrive in this point self.stored_data must be reseted because
		#will be a new city information
		self.stored_data_count = 0 
	'''
	Get almost real-time tweets
	@query
	@save_path
	'''
	def getStreamData(self, query=None,save_path=None):
		if( save_path is None):
			print(colored('Error: You must define save_path','red'))
			sys.exit()

		self.listenerHanlder = StreamListenerHandler(save_path)
		self.streamData = tweepy.Stream(self.auth,self.listenerHanlder)
		self.streamData.filter(track=query)
		


##Method use only Stream Mode
class StreamListenerHandler(tweepy.StreamListener):
	
	def __init__(self,save_path):
		self.log_file = open(save_path+'log_.tsv','a',encoding='utf8')

	def on_data(self,data):
		
		jsonencoded = json.loads(data)

		# print (' geo '+str(jsonencoded["geo"]))
		# print (' coord '+str(jsonencoded["coordinates"]))
		# print (' place country '+str(jsonencoded["place"]["country"]))
		# print (' place name '+str(jsonencoded["place"]["name"]))
		#print (data

		#jsonencoded["coordinates"] = self.removeNone(jsonencoded["coordinates"])
		# jsonencoded["place"]["country"] = self.removeNone(jsonencoded["place"]["country"])
		# jsonencoded["place"]["name"] = self.removeNone(jsonencoded["place"]["name"])
		print (jsonencoded["created_at"] , str(jsonencoded["user"]["id"]), jsonencoded["id_str"], jsonencoded["user"]["name"])
		
		# print( jsonencoded["created_at"],'\t' , jsonencoded["user"]["id"], '\t' , 
									 # jsonencoded["user"]["lang"] ,'\t' , jsonencoded["geo"] , 
									 # '\t' , jsonencoded["text"].encode('utf-8') ,'\t' , jsonencoded["coordinates"])

		self.log_file.write( (jsonencoded["created_at"])+'\t' + str(jsonencoded["user"]["id"])+ '\t' + 
							 (jsonencoded["user"]["lang"]) +'\t' + (jsonencoded["text"]) + '\t' +
							 str(jsonencoded["id_str"])+ '\t' + str(jsonencoded["user"]["screen_name"]) +'\t'+ str(jsonencoded["user"]["name"]) +'\n')
		return True
	
	def on_error(self,status):
		print( colored(status),'red')

	def removeNone(self, var):
		try:
			var = var + "1"
		except (AttributeError, ValueError,TypeError):
			print ( colored('NoneType detected','red'))
		
