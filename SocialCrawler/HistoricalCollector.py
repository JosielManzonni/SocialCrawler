# -*- coding: UTF-8 -*-
"""HistoricalCollector.

Class responsible to collect data from Twitter database or real-time post.

 (c) J.Wirlino and A.Adativa
 Date July 15th 2016
 https://github.com/JosielWirlino/SocialCrawler

"""

from termcolor import colored
import tweepy
import json
import sys
import time


class Collector:
    """Class to connect with TWitter to get data.

    Note:
        More information about Twitter's crentials
        see https://dev.twitter.com/overview/documentation

    Args:
        api_key (str) : api key Twitter's credential.
        api_secret (str) : api secret Twitter's credential.
        access_token (str) : Twitter's crential acess token.
        access_secret (str) : Twitter's crential acess secret.

    Attributes:
        api_key (str) : api key Twitter's credential.
        api_secret (str) : api secret Twitter's credential.
        access_token (str) : Twitter's crential acess token.
        access_secret (str) : Twitter's crential acess secret.

    """

    #   Global variable to count the tweets received

    stored_data_count = 0
    stream_data_count = 0

    def __init__(self, api_key=None, api_secret=None, access_token=None, access_secret=None):
        """When instatiated must be pass all parameters.
        
        If some parameter is None will be throw an error message and
        will be called sys.exit()

        Args:
            api_key (str) : api key Twitter's credential.
            api_secret (str) : api secret Twitter's credential.
            access_token (str) : Twitter's crential acess token.
            access_secret (str) : Twitter's crential acess secret.

        Attributes:
            api_key (str) : api key Twitter's credential.
            api_secret (str) : api secret Twitter's credential.
            access_token (str) : Twitter's crential acess token.
            access_secret (str) : Twitter's crential acess secret.
        
        """
        if(api_key is None or api_secret is None or access_token is None or access_secret is None):
            print(colored('Error: Any parameter can not be None', 'red'))
            sys.exit()

        # setting all parameters
        self.api_key = api_key
        self.api_secret = api_secret
        self.access_token = access_token
        self.access_secret = access_secret

        # requesting authentication

        self.auth = tweepy.OAuthHandler(self.api_key, self.api_secret)
        self.auth.set_access_token(self.access_token, self.access_secret)
        self.twitter = tweepy.API(self.auth)


    def getStoredData(self, query=None, since=None, until=None,city=None, geocode=None, save_path=None,result_limits='infinite', mode='items'):
        """Method to get data stored in Twitter dataset.

        There are two ways to get data: stored and stream
        This method (getStoredData) use Cursor to get all data
        
        #see http://tweepy.readthedocs.io/en/v3.5.0/cursor_tutorial.html
        
        Args:
            query (str) : string content your consult
            since (str) : begin date to start collect data
            until (str) : end date of the tweets to be collected
            city  (str) : specific city data
            geocode (str) : specific region of the city
            mode  (str) : define if you want items or page

        """
        if(query is None or since is None or until is None or save_path is None):
            print(colored('Error: query, since, until, and save_path parameters can not be None', 'red'))
            sys.exit()

        try:
            if(city is not None):
                log_file = open(save_path + 'log_from_' + city.replace(" ", "") +
                                '__' + since + '__' + until + '.tsv', 'a', encoding='utf8')
            else:
                log_file = open(save_path + 'log_' + since +
                                '__' + until + '.tsv', 'a', encoding='utf8')
        except IOError:
            print(colored('Cound not open file!'))
            sys.exit()
        # check if the query is about a specific city
        if(city is None):
            if(mode == 'items'):
                results = tweepy.Cursor(self.twitter.search,
                                        q=query,
                                        since=since,
                                        until=until).items()
            else:
                results = tweepy.Cursor(self.twitter.search,
                                        q=query,
                                        since=since,
                                        until=until).pages()
        else:
            if(mode == 'items'):
                results = tweepy.Cursor(self.twitter.search,
                                        q=query,
                                        since=since,
                                        until=until,
                                        geocode=geocode).items()
            else:
                results = tweepy.Cursor(self.twitter.search,
                                        q=query,
                                        since=since,
                                        until=until,
                                        geocode=geocode).pages()
        #writing column headers
        log_file.write("data_count"+"\t"+"twitter_user_id"+"\t"+"city"+"\t"+"tweet_created_at"+"\t"+"tweet.text"+"\n")
        while True:
            try:
                tweet = results.next()
                self.stored_data_count += 1

                print(colored(self.stored_data_count, 'red'), colored(
                    city, 'green'), colored(tweet.created_at, 'red'), tweet.text)
                # print ('\n')

                log_file.write(str(self.stored_data_count) + '\t' + str(tweet.user.id) + '\t' + str(
                    city) + '\t' + str(tweet.created_at) + '\t' + str(tweet.text.encode('utf-8')) + '\n')

            # wait 16 minute to search again
            # https://dev.twitter.com/rest/public/rate-limiting
            except tweepy.TweepError:
                print('\n')
                print(
                    colored('Twitter API rate limit. Wait 16 minutes to request again.\n ', 'red'))
                time.sleep(960)
                continue
            except StopIteration:
                break
        # when arrive in this point self.stored_data must be reseted because
        # will be a new city information
        self.stored_data_count = 0

    def getStreamData(self, query=None, save_path=None):
        """Method to get data in almost real-time.

        The tweets that match with query will be saved as json data in a *.tsv file
        
        Args:
            query (str) : Keywords or expression that a tweet must has.
            save_path (str) : path to be saved the file generated with json data

        """
        if(save_path is None):
            print(colored('Error: You must define save_path', 'red'))
            sys.exit()

        self.listenerHanlder = StreamListenerHandler(save_path)
        self.streamData = tweepy.Stream(self.auth, self.listenerHanlder)
        self.streamData.filter(track=query)


# Method use only Stream Mode
class StreamListenerHandler(tweepy.StreamListener):
    """Listener Method to be listen Twitter's server.
    
    When the Twitter's server get a tweet that match with a query passed in getStreamData method
    will be send for our app, the data is sent with json data format.

    """

    def __init__(self, save_path):
        """Method to set log file path."""
        self.log_file = open(save_path + 'log_.tsv', 'a', encoding='utf8')

    def on_data(self, data):
        """Method called each data sent from TWitter's server ."""
        jsonencoded = json.loads(data)

        print(jsonencoded["created_at"], str(jsonencoded["user"][
              "id"]), jsonencoded["id_str"], jsonencoded["user"]["name"])

        self.log_file.write((jsonencoded["created_at"]) + '\t' + str(jsonencoded["user"]["id"]) + '\t' +
                            (jsonencoded["user"]["lang"]) + '\t' + (jsonencoded["text"]) + '\t' +
                            str(jsonencoded["id_str"]) + '\t' + str(jsonencoded["user"]["screen_name"]) + '\t' + str(jsonencoded["user"]["name"]) + '\n')
        return True

    def on_error(self, status):
        """Method to print the error message ."""
        print(colored(status), 'red')

    # def removeNone(self, var):
    #     try:
    #         var = var + "1"
    #     except (AttributeError, ValueError, TypeError):
    #         print(colored('NoneType detected', 'red'))
