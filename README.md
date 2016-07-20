# SocialCrawler
It is a python package to help get data from Twitter, Foursquare.

This package was created to facilitate the data mining from Twitter and Foursquare.

## Install (generic way)

```python
	$ python3.4 -m pip install SocialCrawler
```

## How work ?

#### Requeriments

 - Python >= 3.4  ( only one )
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

- Getting **check-ins** shared in Twitter or the check ins of the last week.
    -  If you have a Foursquare credential you will be able to track data from specific locations and others. 

See Wiki!