#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# (c) J.Wirlino
# Date July 15th 2016
# https://github.com/JosielWirlino/SocialCrawler

from setuptools import setup

setup( name='SocialCrawler',
	version='0.1',
	description='This package allow get data from Twitter, Swarm and Foursquare',
	url='http://github.com/JosielWirlino/TwitterSwarm4Square-DataMining',
	author='J.Wirlino',
	author_email='josiel.wirlino@gmail.com',
	license='GNU',
	packages=['SocialCrawler'],
	install_requires=['tweepy',
					  'requests',
					  'termcolor'],
	zip_safe=False
	)