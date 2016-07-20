#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# (c) J.Wirlino and A.Adativa
# Date July 15th 2016
# https://github.com/JosielWirlino/SocialCrawler

from setuptools import setup

PACKAGE = "SocialCrawler"
NAME = "SocialCrawler"
DESCRIPTION = ""
AUTHOR = 'J.Wirlino and A. Adativa'
AUTHOR_EMAIL = 'josiel.wirlino@gmail.com, alice.adativa@gmail.com'
URL = 'http://github.com/JosielWirlino/SocialCrawler'
VERSION = __import__(PACKAGE).__version__

setup( name=NAME,
	version=VERSION,
	description='This package allow you get data from Twitter, Swarm(check-ins) and Foursquare',
	long_description=read("README.rst"),
	url=URL,
	author=AUTHOR
	author_email=AUTHOR_EMAIL,
	license='GNU',
	packages=[PACKAGE],
	install_requires=['tweepy',
					  'requests',
					  'termcolor',
					  'requests>=2.4.3'],
	classifiers=[
				'Intended Audience :: Developers',
				'Intended Audience :: Science/Research',
				'License :: OSI Approved :: GNU',
				'Programming Language :: Python :: 3.4',
				'Programming Language :: Python :: 3.5',
				'Topic :: Scientific/Engineering :: Information Analysis'
				],
	zip_safe=False
	)