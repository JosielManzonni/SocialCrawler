#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# (c) J.Wirlino
# Date July 15th 2016
# https://github.com/JosielWirlino/SocialCrawler

from setuptools import setup

setup( name='SocialCrawler',
	version='0.2',
	description='This package allow get data from Twitter, Swarm and Foursquare',
	url='http://github.com/JosielWirlino/TwitterSwarm4Square-DataMining',
	author='J.Wirlino and A. Adativa',
	author_email='josiel.wirlino@gmail.com, alice.adativa@gmail.com',
	license='GNU',
	packages=['SocialCrawler'],
	install_requires=['tweepy',
					  'requests',
					  'termcolor',
					  'requests>=2.4.3'],
	zip_safe=False
	)