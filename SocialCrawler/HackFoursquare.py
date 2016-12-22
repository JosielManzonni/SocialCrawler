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

class Hacking:
	def __init__(self,developer_email,developer_password):
		self.developer_email = developer_email
		self.developer_password = developer_password
	def open_browser(self):
		self.driver = webdriver.Firefox()
		login_developer_4square = 'https://foursquare.com/login'
		
		login_field = driver.find_element_by_id("username")
		login_field.clear()
		login_field.send_keys(developer_email)

		password_field = driver.find_element_by_id("password")
		password_field.clear()
		password_field.send_keys(developer_password)

		#do login
		driver.find_element_by_id("loginFormButton").click()



