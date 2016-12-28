# -*- coding: UTF-8 -*-
"""Extractor class to retrieve data from Foursquare.

# (c) J.Wirlino and A.Adativa
# Date Dec 22th 2016
# https://github.com/JosielWirlino/SocialCrawler

"""

from selenium import webdriver
from pyvirtualdisplay import Display #allow run without a display
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from pyvirtualdisplay import Display
import time
from termcolor import colored

class Hacking:
	"""Summary
	"""

	def __init__(self,developer_email,developer_password,mode="hired"):
		"""Summary
		
		Args:
		    developer_email (TYPE): Description
		    developer_password (TYPE): Description
		"""
		
		self.login_url = "https://foursquare.com/login"
		self.venue_url = "https://developer.foursquare.com/docs/explore#req=venues/"
		self.resolveId_url = "https://developer.foursquare.com/docs/explore#req=checkins/resolve%3FshortId%3D"

		self.developer_email = developer_email
		self.developer_password = developer_password
		
		self.mode = mode

		# self.back_to_main_class = False

	def open_browser(self):
		"""Summary
		Method that set up Foursquare Developer IDs
		
		"""
		if self.mode is "hired":
			self.virtual_display = None
			self.virtual_display = Display(visible=0,size=(800,600))
			self.virtual_display.start()

		self.browser_login()
	
	def browser_login(self):
		self.browser = None
		self.browser = webdriver.Firefox()
		self.browser.get(self.login_url)

		login_field = self.browser.find_element_by_id("username")
		login_field.clear()
		login_field.send_keys(self.developer_email)

		password_field = self.browser.find_element_by_id("password")	
		password_field.clear()
		password_field.send_keys(self.developer_password)
		self.browser.find_element_by_id("loginFormButton").click()
		time.sleep(5)
		#do login
	

	def get_info_detail(self,v=None,key_id=None):
		"""Summary
			Method to get venue detail using WebBrowser. Useful when
			you got rate limit from Foursquare VENUE API
		
		Args:
		    v (None, optional): Description
		    key_id (None, optional): s for swarm_id or v for venue_id
		
		Returns:
		    TYPE: string
		"""
		self.version = v
		self.key_id = key_id

		count=0
		if(key_id is None):
			print(colored("key_id must be setted",'red'))
			return
		
		going = True
		while going:
			# count +=1
			if v is "v":
				self.browser.get(self.venue_url+key_id)
			else:
				self.browser.get(self.resolveId_url+key_id)

			timeout = 15
			going = False
			try:
				element_present = EC.presence_of_element_located(self.browser.find_element_by_id('completeUrl'))
				WebDriverWait(self.browser, timeout).until(element_present)
				count = 0
			except TimeoutException:
				print(colored("Time Out! Doing request again"))
				# if( count == 5 ):
				self.rebuild()
				# self.browser.quit()
				# self.browser_login()

				going = True


		# html_source = self.browser.page_source
		# print(html_source)
		#get OAuth generate from Fousquare
		# result = self.browser.find_element_by_id("results").text
		# return result
		completeUrl = self.browser.find_element_by_id("completeUrl")
		self.browser.get(completeUrl.text)
		return self.browser.find_element_by_tag_name("body").text
	

	# def get_swarm_resolve_id(self, swarm_id=None):
	# 	if(swarm_id is None):
	# 		return
	# 	self.browser.get(self.resolveId_url+swarm_id)
	# 	# html_source = self.browser.page_source
	# 	# print(html_source)
	# 	#get OAuth generate from Fousquare
	# 	# result = self.browser.find_element_by_id("results").text
	# 	# return result
	# 	completeUrl = self.browser.find_element_by_id("completeUrl")
	# 	self.browser.get(completeUrl.text)
	# 	return self.browser.find_element_by_tag_name("body").text
	
	# def destroy(self):
	# 	# self.virtual_display.stop()
	# 	self.browser.quit()

	def rebuild(self):
		"""Summary
		
		Args:
		    value (TYPE): Description
		
		Returns:
		    TYPE: Description
		"""
		self.browser.quit()
		self.browser_login()



