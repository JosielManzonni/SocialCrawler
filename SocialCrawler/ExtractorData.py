# -*- coding: UTF-8 -*-
"""Extractor class to retrieve data from Foursquare.

# (c) J.Wirlino and A.Adativa
# Date Sept 1th 2016
# https://github.com/JosielWirlino/SocialCrawler

"""

from termcolor import colored
# import json
import sys
import urllib.request
from urllib.error import URLError
from pip._vendor.requests.exceptions import HTTPError
import time
import requests

class Extractor:
    """Read log file from Collector .

    ( or files that contains a swarm url code)

    This class use tools and keywords from Foursquare API Endpoints.

        Note:
            If has a another file that was not created by Collector you must
            have set.column parameter with a integer saying the file column that
            has swarm url. All file input must be *.tsv .

        Args:
            see def __init__ docstring
    """
   
    def __init__(self,foursquare_client_id=None, foursquare_client_secret=None,foursquare_version="20140806%20", foursquare_mode="swarm"):
        """Class constructor.
        
        Method to init all minimum settings necessary to get data froum Foursquare.
        
        Note:
            
            foursquare_mode and foursquare_version parameter are two specials parameters 
            to control over the kind of that Foursquare returns.
            see https://developer.foursquare.com/overview/versioning

            To see how can get crendetials see https://developer.foursquare.com/overview/auth

        Args:
            foursquare_client_id (str) : Foursquare's app client id
            foursquare_client_secret (str) : Foursquare's app client secret
            foursquare_version (str) : kind of Foursquare returns, by default "20140806%20" .
            foursquare_mode (str) : foursquare mode answer. Valid value: "swarm"  or "foursquare" by default "swarm"

        Attributes:
            foursquare_client_id (str) : Foursquare's app client id
            foursquare_client_secret (str) : Foursquare's app client secret
            foursquare_version (str) : kind of Foursquare returns
            foursquare_mode (str) : foursquare mode answer
                                    valid value: "swarm"  or "foursquare"
        """
        foursquare_mode_valid_value = {'swarm','foursquare'}

        if( foursquare_client_id is None or foursquare_client_secret is None ):
            print(colored('Any parameter can be None.','red'))
            sys.exit()

        if( foursquare_mode not in foursquare_mode_valid_value ):
            print(colored('fourquare_mode invalid value.','red'))
            sys.exit()

        self._foursquare_client_id = foursquare_client_id
        self._foursquare_client_secret = foursquare_client_secret
        self._foursquare_version = foursquare_version
        self._foursquare_mode = foursquare_mode

    # @property
    # def file_name(self):
    #     """File name that will be used to save the file created when run."""
    #     return self._file_name
    
    # @property
    # def mode(self):
    # 	"""Mode that class was setted."""
    # 	return self._mode
    
    # @property
    # def path_file(self):
    # 	"""folder where the file will be saved."""
    # 	return self._path_file
    
    def settings(self,mode=None,out_file_name=None,out_path_file=None,column=4,input_file=None):
        """Class constructor.

        Method to read log file created by Collector class
        and get Swarm's url code and consult Foursquare to retrieve
        information about avenue, local type, shared_count and all information that is
        returned than will save in a file called log_<out_file_name>.tsv

        Args:
            out_file_name (str) : File name to be created.
            out_path_file (str) : File path where the file must be saved.
            mode (str) : json file version.
                         mode valid value:
                         - v1 if the file was created from Collector class or CollectorV2 class
                         - v2 if was not created by any Collector but has the Swarm url
                                  if the value is v2 the "column" parameter must be setted
            column (int) : column that contain the Swarm url. This field is only
                           verified if "mode" is v2 .
            input_file(str) : file that contains swarm url code

        """
        mode_valid_value = {'v1','v2'}

        if(mode is None or out_file_name is None or out_path_file is None or input_file is None):
            print(colored('Any parameter can be None except column field iff mode is not v2. ','red'))
            sys.exit()

        if(mode not in mode_valid_value ):
            print(colored('mode value invalid.','red'))
            sys.exit()

        self._file_name = out_file_name
        self._path_file = out_path_file
        self._mode = mode
        self._input_file = input_file
        self._column = column
        if(mode == "v2"):
            if(column is None ):
                print(colored("When mode is v2, column field must be assigned",'red'))
                sys.exit()
            self._column = column

    def consultFoursquare(self):
        """Method to access foursquare and use resolveId.

        This method is called to each line read from input file, so
        all attributes of credentials function must be setted correctly

        resolvedId is a function from Foursquare API Endpoints to get data from a swarm url code.
        see https://developer.foursquare.com/docs/
        """
        swarm_prefix = "https://www.swarmapp.com/c/"
        url_venue = 'https://api.foursquare.com/v2/venues/'
        url_resolveID = 'https://api.foursquare.com/v2/checkins/resolve?shortId='

        if(self._mode is None or self._file_name is None or self._path_file is None or self._input_file is None):
            print(colored('One or more attributes are None. Firstly you must call settings method and than you call this method ','red'))
            sys.exit()

        __out = open( self._path_file + '/' + self._file_name + '.tsv','a')
        
        #set header
        __out.write( 'checkin_id' \
                    + '\t' + 'checkin_createdAt' \
                    + '\t' + 'user_id' \
                    + '\t' + 'user_gender' \
                    + '\t' + 'swarm_key' \
                    + '\t' + 'venue_id' \
                    + '\t' + 'venue_coord' \
                    + '\t' + 'venue_categories_id' \
                    + '\t' + 'venue_categories_name' \
                    + '\t' + 'venue_stats_checkinsCount' \
                    + '\t' + 'venue_stats_userCount' \
                    +'\n')

        for line in open( self._input_file,'r'): #read each line from input file
            
            line_split = line.split('\t')
            
            # print(line + "URL T.CO " + line_split[self._column])
            try:
            
                t_co_url = line_split[self._column] #get tweet text
                
                idx = t_co_url.index('https://t.co/')

                t_co_url = t_co_url[ idx : idx+23 ] #get all t.co url

                print("Trying resolve "+t_co_url)

                swarm_resolved_url =  urllib.request.urlopen( t_co_url ) # try resolve swarm short url 
            
            except HTTPError as e:
                print(colored('URLLIB URLOPEN FAILED ERROR CODE %s' %e.code,'red'))
                continue
            
            except ValueError as e:
                print(colored(' SWARM SHORT URL ERROR ','red'))
                print(e)
                continue
            except URLError as e:
                print(colored(' URL ERROR ','red'))
                print(e)
                continue
            except ConnectionResetError as e:
                print(colored(' CONNECTION RESET ERROR ','red'))
                print(e)
                continue
            except ConnectionError as e:
                print(colored(' CONNECTION ERROR ','red'))
                print(e)
                continue
            except ConnectionAbortedError as e:
                print(colored(' CONNECTION ABORTED ERROR ','red'))
                print(e)
                continue
            except ConnectionRefusedError as e:
                print(colored(' CONNECTION REFUSED ERROR ','red'))
                print(e)
                continue
            except :
                print(colored(' URLLIB ERROR','red'))
                continue

            if swarm_prefix not in swarm_resolved_url.url: #if do not have swarm key code
                print(swarm_resolved_url.url)
                print(colored('SWARM URL ERROR','red') )
                continue

            print("resolved sucessfully. Link resolved is "+swarm_resolved_url.url )

            key =  swarm_resolved_url.url[ len(swarm_resolved_url.url) - 11 : ] #get string after www.swarmapp.com/
            
            try:

                response = requests.get( url_resolveID + key + 
                                      '&client_id=' + self._foursquare_client_id +
                                      '&client_secret=' + self._foursquare_client_secret +
                                      '&v=' + self._foursquare_version +
                                      '&m=' + self._foursquare_mode )

                swarm_4square_data = response.json()
                

            except HTTPError as e:
                print(colored('HTTPERROR ','red'))
                print(colored(e,'red'))
                continue
            except :
                print(colored('FOURSQUARE REQUESTS GET ERROR ','red'))
                # hour = time.strftime("%H")
                # minute = time.strftime("%M")
                # second = time.strftime("%S")
                # print(colored('STOP REQUEST IN ' + str(hour+1) + ':' + str(minute+1) + ':' + str(second) , 'red' ) )
                print(colored('Wait 15 minutes to request again ','red'))
                time.sleep(960) #sleep 1 hour and 1 minute

                continue

            try:
                v_id = swarm_4square_data['response']['checkin']['venue']['id']
                venue_request = requests.get( url_venue + v_id +
                                                  '?client_id=' + self._foursquare_client_id +
                                                  '&client_secret=' + self._foursquare_client_secret +
                                                  '&v=' + self._foursquare_version)

                venue_data = venue_request.json()
            except HTTPError as e:
                print(colored('HTTPERROR ','red'))
                print(colored(e,'red'))
                continue

            except :
                print(colored('VENUE REQUESTS GET ERROR ','red'))
                # print(colored('STOP REQUEST IN ' + str(time.strftime("%H:%M:%S"),'red') ) )
                
                # hour = time.strftime("%H")
                # minute = time.strftime("%M")
                # second = time.strftime("%S")
                print(colored('Wait one 15 minutes to request again ','red'))
                # print('Next request '+ str(hour+1) + ':' + str(minute+1) + ':' + str(second))
                # print(colored('STOP REQUEST IN ' + str(hour+1) + ':' + str(minute+1) + ':' + str(second) , 'red' ) )
                time.sleep(960) #sleep 15 minutes
                continue    
                # if( swarm_4square_data['meta']['code'] == "200"): #data yet available in foursquare dataset

            try:
                checkin_id = swarm_4square_data['response']['checkin']['id']
            except:
                print(colored('SWARM CHECKIN ERROR [PARSER CHECKIN_ID]','red'))
                continue
            
            try:    
                checkin_createdAt = swarm_4square_data['response']['checkin']['createdAt']
            except:
                print(colored('SWARM CHECKIN ERROR [PARSER CREATEDAT]','red'))
                continue

            try:
                user_id = swarm_4square_data['response']['checkin']['user']['id']
            except:
                print(colored('SWARM CHECKIN ERROR [PARSER USER_ID]','red'))
                continue

            try:
                user_gender = swarm_4square_data['response']['checkin']['user']['gender']
            except:
                print(colored('SWARM CHECKIN ERROR [PARSER USER_GENDER]','red'))
                continue

            print("Foursquare and Venue requests success.")
            print("Saving Foursquare data.")
            __out.write( str(checkin_id) + \
                        '\t' + str(checkin_createdAt) \
                        + '\t' + str(user_id) + '\t' \
                        + user_gender \
                        + '\t' + key + '\t' )
            # write data about user

            try:
                venue_id = venue_data['response']['venue']['id']
            except:
                print(colored('VENUE ERROR [PARSER VENUE_ID]','red'))
                continue

            try:
                venue_lat = venue_data['response']['venue']['location']['lat']
            except:
                print(colored('VENUE ERROR [PARSER VENUE_LOCATION_LAT]','red'))
                __out.write('\n')
                continue

            try:
                venue_lng = venue_data['response']['venue']['location']['lng']
            except:
                print(colored('VENUE ERROR [PARSER VENUE_LOCATION_LNG]','red'))
                __out.write('\n')
                continue

            try:
                categorie_id = venue_data['response']['venue']['categories'][0]['id']
            except:
                print(colored('VENUE ERROR [PARSER VENUE_CATEGORIE_ID]','red'))
                __out.write('\n')
                continue

            try:
                categorie_name = venue_data['response']['venue']['categories'][0]['name']
            except:
                print(colored('VENUE ERROR [PARSER VENUE_CATEGORIE_NAME]','red'))
                __out.write('\n')
                continue

            try:
                stats_checkins_count = venue_data['response']['venue']['stats']['checkinsCount']
            except:
                print(colored('VENUE ERROR [PARSER VENUE_STATS_CHECKINSCOUNT]','red'))
                __out.write('\n')
                continue

            try:
                stats_user_count = venue_data['response']['venue']['stats']['usersCount']
            except:
                print(colored('VENUE ERROR [PARSER VENUE_STATS_USERSCOUNT]','red'))
                __out.write('\n')
                continue
            
            print("Saving Venue data.")
            __out.write( str(venue_id) \
                        + '\t' + str(venue_lat) + ',' + str(venue_lng) \
                        + '\t' + str(categorie_id) + '\t' \
                        + categorie_name + '\t' \
                        + str(stats_checkins_count) \
                        + '\t' + str(stats_user_count) \
                        + '\n')
            # break
        __out.close()












