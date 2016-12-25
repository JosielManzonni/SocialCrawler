#!/bin/bash

#register the package
sudo python3 setup.py register
#publish a 'downloadble' version
sudo python3 setup.py sdist upload
running sdist
running egg_info
writing requirements to SocialCrawler.egg-info/requires.txt
writing top-level names to SocialCrawler.egg-info/top_level.txt
writing SocialCrawler.egg-info/PKG-INFO
writing dependency_links to SocialCrawler.egg-info/dependency_links.txt
reading manifest file 'SocialCrawler.egg-info/SOURCES.txt'
writing manifest file 'SocialCrawler.egg-info/SOURCES.txt'
running check
creating SocialCrawler-0.0.8
creating SocialCrawler-0.0.8/SocialCrawler
creating SocialCrawler-0.0.8/SocialCrawler.egg-info
copying files to SocialCrawler-0.0.8...
copying README.rst -> SocialCrawler-0.0.8
copying setup.py -> SocialCrawler-0.0.8
copying SocialCrawler/ExtractorData.py -> SocialCrawler-0.0.8/SocialCrawler
copying SocialCrawler/HackFoursquare.py -> SocialCrawler-0.0.8/SocialCrawler
copying SocialCrawler/HistoricalCollector.py -> SocialCrawler-0.0.8/SocialCrawler
copying SocialCrawler/NewExtractorData.py -> SocialCrawler-0.0.8/SocialCrawler
copying SocialCrawler/__init__.py -> SocialCrawler-0.0.8/SocialCrawler
copying SocialCrawler/test_ned.py -> SocialCrawler-0.0.8/SocialCrawler
copying SocialCrawler/test_sc_008.py -> SocialCrawler-0.0.8/SocialCrawler
copying SocialCrawler.egg-info/PKG-INFO -> SocialCrawler-0.0.8/SocialCrawler.egg-info
copying SocialCrawler.egg-info/SOURCES.txt -> SocialCrawler-0.0.8/SocialCrawler.egg-info
copying SocialCrawler.egg-info/dependency_links.txt -> SocialCrawler-0.0.8/SocialCrawler.egg-info
copying SocialCrawler.egg-info/not-zip-safe -> SocialCrawler-0.0.8/SocialCrawler.egg-info
copying SocialCrawler.egg-info/requires.txt -> SocialCrawler-0.0.8/SocialCrawler.egg-info
copying SocialCrawler.egg-info/top_level.txt -> SocialCrawler-0.0.8/SocialCrawler.egg-info
Writing SocialCrawler-0.0.8/setup.cfg
Creating tar archive
removing 'SocialCrawler-0.0.8' (and everything under it)
running bdist_wheel
running build
running build_py
copying SocialCrawler/__init__.py -> build/lib/SocialCrawler
copying SocialCrawler/test_sc_008.py -> build/lib/SocialCrawler
copying SocialCrawler/HackFoursquare.py -> build/lib/SocialCrawler
copying SocialCrawler/NewExtractorData.py -> build/lib/SocialCrawler
copying SocialCrawler/HistoricalCollector.py -> build/lib/SocialCrawler
installing to build/bdist.linux-x86_64/wheel
running install
running install_lib
creating build/bdist.linux-x86_64/wheel
creating build/bdist.linux-x86_64/wheel/SocialCrawler
copying build/lib/SocialCrawler/__init__.py -> build/bdist.linux-x86_64/wheel/SocialCrawler
copying build/lib/SocialCrawler/test_sc_008.py -> build/bdist.linux-x86_64/wheel/SocialCrawler
copying build/lib/SocialCrawler/HackFoursquare.py -> build/bdist.linux-x86_64/wheel/SocialCrawler
copying build/lib/SocialCrawler/NewExtractorData.py -> build/bdist.linux-x86_64/wheel/SocialCrawler
copying build/lib/SocialCrawler/ExtractorData.py -> build/bdist.linux-x86_64/wheel/SocialCrawler
copying build/lib/SocialCrawler/test_ned.py -> build/bdist.linux-x86_64/wheel/SocialCrawler
copying build/lib/SocialCrawler/HistoricalCollector.py -> build/bdist.linux-x86_64/wheel/SocialCrawler
running install_egg_info
Copying SocialCrawler.egg-info to build/bdist.linux-x86_64/wheel/SocialCrawler-0.0.8-py3.5.egg-info
running install_scripts
creating build/bdist.linux-x86_64/wheel/SocialCrawler-0.0.8.dist-info/WHEEL
