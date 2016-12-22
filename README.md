# SocialCrawler
It is a python package to help get data from Twitter, Foursquare.

This package was created to facilitate the data mining from Twitter and Foursquare. (**Only Linux**)

## Install (generic way)

```shell
	$ python3.5 -m pip install SocialCrawler
```

## How work ?

#### Requirements

 - Python >= 3 
 - setuptools
 - Foursquare developer  credentials ( if you wanna work with)
 - Twitter developer credentials ( if you wanna work with )


#### Possibility

 - As the package use tweepy as framework to connect with Twitter we can use [Twitter Stream API](https://dev.twitter.com/streaming/overview). Therefore you can search based in :
    -  delimited
    -  stall_warnings
    -  filter_level
    -  language
    -  follow
    -  track
    -  locations
    -  count
    -  with
    -  replies
    -  stringift_friend_id


As shown in Stream Overview

- Getting **check-ins** shared in Twitter or the check-ins of the last week.
    -  If you have a Foursquare credential you will be able to track data from specific locations and others. 

**See Wiki!**

- **v 0.0.8**
    - added selenium as requirements to use foursquare browser request (to avoid rate limit), **can not work**
    - update ExtractorData to a full version to allow get (almost) full VENUE info
    - removed urlib2 as requirements

    
- **v 0.0.7**
    - when VENUE or FOURSQUARE get requests error the program thread will wait 15 minutes to request again
    - Added new except treatments 
    - separeted foursquare request and venue request in two try-except blocks
    - fixed write categorie_id bug, missing int to str convert
    - **yet** in ExtractorData possibility of use other file (non a created by Collector or CollectorV2 ) to consult
    Foursquare. (**not available yet**)
    

- **v 0.0.6**
	- Formatted to PEP257 and PEP8 (almost)
	- Implementaded ExtractorData: a simple way to get data from Foursquare using the swarm url code
	- Add  HistoricalCollector.CollectorV2 that get all data from json tweet and save as tsv file
    - Add in ExtractorData possibility of use other file (non a created by Collector or CollectorV2 ) to consult
    Foursquare. (**not available yet**)
    - added urllib2 as Requirements


- **v 0.0.5**
	- Fixed bug in ***getStoredData*** function that allow some parameter be None
	- Updated format file name generated 
	- Increased time wait request from 15 minutos to 16. ( Sometimes when was tried request again -after 15 minutes - the server responded that don't finished the 15 minutes.
	- Updated the fields saved. Now all field is saved in a file using \tab format as is shown in Wiki.
