# -*- coding: utf-8 -*-
"""SocialCrawler.

This modules import all classes from SocialCrawler package.

 (c) J.Wirlino and A.Adativa
 Date Sept 1th 2016
 https://github.com/JosielWirlino/SocialCrawler

"""

# from colorama import init #do termcolor work in Windows
# init()

from . import HistoricalCollector
from . import ExtractorData
from . import NewExtractorData
from . import HeadLess
from . import HackFoursquare
from . import HTTPResponseError
# from  . import ExtractorData


__version__ = "0.4.0"
__author__ = "A.Adativa and J.Wirlino"

__all__ = [	
			"HistoricalCollector",
			"ExtractorData",
			"HackFoursquare",
			"NewExtractorData",
			"HeadLess",
			"HTTPResponseError"
		]
