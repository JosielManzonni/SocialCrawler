# SocialCrawler
It is a python package to help get data from Twitter, Foursquare.

This package was created to facilitate the data mining from Twitter and Foursquare.

## Install (generic way)

```python
	$ python3.5 -m pip install SocialCrawler
```

## How work ?

#### Requeriments

 - Python >= 3.5 
 - Foursquare developer  credentials ( if you wanna work with)
 - Twitter developer credentials ( if you wanna work with )
 - Facebook developer credentials (Optional)

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

 -->
- **v 0.0.6**
	- Formatted to PEP257 and PEP8 (almost)
	- Implementaded ExtractorData: a simple way to get data from Foursquare using the swarm url code
	- Add  HistoricalCollector.CollectorV2 that get all data from json tweet and save as tsv file
    - Add in ExtractorData possibility of use other file (non a created by Collector or CollectorV2 ) to consult
    Foursquare. (**not available yet**)
    - added urllib2 as requeriments


- **v 0.0.5**
	- Fixed bug in ***getStoredData*** function that allow some parameter be None
	- Updated format file name generated 
	- Increased time wait request from 15 minutos to 16. ( Sometimes when was tried request again -after 15 minutes - the server responded that don't finished the 15 minutes.
	- Updated the fields saved. Now all field is saved in a file using \tab format as is shown in Wiki.
