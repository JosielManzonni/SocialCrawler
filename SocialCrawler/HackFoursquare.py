# -*- coding: UTF-8 -*-
"""Extractor class to retrieve data from Foursquare.

# (c) J.Wirlino and A.Adativa
# Date Dec 22th 2016
# https://github.com/JosielWirlino/SocialCrawler

"""

from selenium import webdriver
from pyvirtualdisplay import Display #allow run without a display
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

class Hacking:
	"""Summary
	"""
	login_url = "https://foursquare.com/login"
	venue_url = "https://developer.foursquare.com/docs/explore#req=venues/"

	def __init__(self,developer_email,developer_password):
		
		self.developer_email = developer_email
		self.developer_password = developer_password
		self.back_to_main_class = False
	def open_browser(self):
		"""Summary
			Method that set up Foursquare Developer IDs
		
		"""
		self.driver = webdriver.Firefox()
		
		self.driver.get(self.login_url)

		login_field = self.driver.find_element_by_id("username")
		login_field.clear()
		login_field.send_keys(self.developer_email)

		password_field = self.driver.find_element_by_id("password")	
		password_field.clear()
		password_field.send_keys(self.developer_password)
		self.driver.find_element_by_id("loginFormButton").click()
		time.sleep(5)
		#do login
	def get_venue_detail(self, venue_id=None):
		"""Summary
			Method to get venue detail using WebBrowser. Useful when
			you got rate limit from Foursquare VENUE API
		Args:
		    venue_id (None, optional): venue id
		
		Returns:
		    TYPE: string
		"""
		if(venue_id is None):
			return
		self.driver.get(self.venue_url+venue_id)
		# html_source = self.driver.page_source
		# print(html_source)
		#get OAuth generate from Fousquare
		# result = self.driver.find_element_by_id("results").text
		# return result
		completeUrl = self.driver.find_element_by_id("completeUrl")
		self.driver.get(completeUrl.text)
		return self.driver.find_element_by_tag_name("body").text
	
	def set_call_back(self,value):
		self.back_to_main_class = value




