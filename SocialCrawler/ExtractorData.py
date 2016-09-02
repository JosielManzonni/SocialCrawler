# -*- coding: UTF-8 -*-
"""Extractor class to retrieve data from Foursquare.

# (c) J.Wirlino and A.Adativa
# Date Sept 1th 2016
# https://github.com/JosielWirlino/SocialCrawler

"""

from termcolor import colored
import json
import sys
import urllib2
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

    @property
    def file_name(self):
        """File name that will be used to save the file created when run."""
        return self._file_name
    
    @property
    def mode(self):
    	"""Mode that class was setted."""
    	return self._mode
    
    @property
    def path_file(self):
    	"""folder where the file will be saved."""
    	return self._path_file
    
    def settings(self,mode=None,out_file_name=None,out_path_file=None,column=3,input_file=None):
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
        swarm_prefix = "https://swarmapp.com/c/"
        url_venue = 'https://api.foursquare.com/v2/venues/'
        url_resolveID = 'https://api.foursquare.com/v2/checkins/resolve?shortId='

        if(self._mode is None or self._file_name is None or self._path_file is None or self._input_file is None):
            print(colored('One or more attributes are None. Firstly you must call settings method and than you call this method ','red'))
            sys.exit()

        __out = open( self._path_file + '/' + self._file_name + '.tsv' )
        
        #set header
        __out.write( 'checkin_id' 
                    + '\t' + 'checkin_createdAt' 
                    + '\t' + 'user_id' 
                    + '\t' + 'user_gender' 
                    + '\t' + 'swarm_key'
                    + '\t' + 'venue_id'
                    + '\t' + 'venue_coord'
                    + '\t' + 'venue_categories_id'
                    + '\t' + 'venue_categories_name'
                    + '\t' + 'venue_stats_checkinsCount'
                    + '\t' + 'venue_stats_userCount'
                    +'\n')

        for line in open( self._input_file,'r'): #read each line from input file
            line_split = line.split('\t')
            try:
            
                t_co_url = line_split[self._column] #get tweet text
                
                idx = t_co_url.index('https://t.co/')

                t_co_url = t_co_url[ idx : idx+23 ] #get all t.co url

                swarm_resolved_url =  urllib2.urlopen( t_co_url ) # try resolve swarm short url 
            
            except urllib2.HTTPError as e:
                print(colored('URLLIB2 URLOPEN FAILED ERROR CODE %s' %e.code,'red'))
                continue
            
            except ValueError as e:
                print(colored(' SWARM SHORT URL ERROR ','red'))
            
            except :
                print(colored(' URLLIB2 EROR','red'))

            if swarm_prefix not in swarm_resolved_url.url: #if do not have swarm key code
                print(colored('SWARM URL ERROR','red') )
                continue

            key =  swarm_resolved_url.url[ len(swarm_resolved_url.url) - 11 : ] #get string after www.swarmapp.com/
            
            try:

                response = requests.get( url_resolveID + key + 
                                      '&client_id=' + self.foursquare_client_id +
                                      '&client_secret=' + self.foursquare_client_secret +
                                      '&v=' + self.foursquare_version +
                                      '&m=' + self.foursquare_mode )

                swarm_4square_data = response.json()
                
                v_id = swarm_4square_data['response']['checkin']['venue']['id']

                venue_request = self.requests.get( url_venue + v_id +
                                                  '?client_id=' + self.foursquare_client_id +
                                                  '&client_secret=' + self.foursquare_client_secret +
                                                  '&v=' + self.foursquare_version)

                venue_data = venue_request.json()
                
                # if( swarm_4square_data['meta']['code'] == "200"): #data yet available in foursquare dataset
            except :
                print(colored('REQUESTS GET ERROR ','red'))
                continue

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

            __out.write( checkin_id 
                        + '\t' + checkin_createdAt 
                        + '\t' + user_id 
                        + '\t' + user_gender 
                        + '\t' + key + '\t' ) # write data about user

            try:
                venue_id = venue_data['response']['venue']['id']
            except:
                print(colored('VENUE ERROR [PARSER VENUE_ID]','red'))
                continue

            try:
                venue_lat = venue_data['response']['venue']['location']['lat']
            except:
                print(colored('VENUE ERROR [PARSER VENUE_LOCATION_LAT]','red'))
                continue

            try:
                venue_lng = venue_data['response']['venue']['location']['lng']
            except:
                print(colored('VENUE ERROR [PARSER VENUE_LOCATION_LNG]','red'))
                continue

            try:
                categorie_id = venue_data['response']['venue']['categories'][0]['id']
            except:
                print(colored('VENUE ERROR [PARSER VENUE_CATEGORIE_ID]','red'))
                continue

            try:
                categorie_name = venue_data['response']['venue']['categories'][0]['name']
            except:
                print(colored('VENUE ERROR [PARSER VENUE_CATEGORIE_NAME]','red'))
                continue

            try:
                stats_checkins_count = venue_data['response']['venue']['stats']['checkinsCount']
            except:
                print(colored('VENUE ERROR [PARSER VENUE_STATS_CHECKINSCOUNT]','red'))
                continue

            try:
                stats_user_count = venue_data['response']['venue']['stats']['usersCount']
            except:
                print(colored('VENUE ERROR [PARSER VENUE_STATS_USERSCOUNT]','red'))
                continue

            __out.write( venue_id 
                        + '\t' + venue_lat + ',' + venue_lng 
                        + '\t' + categorie_id 
                        + '\t' + categorie_name 
                        + '\t' + stats_checkins_count
                        + '\t' + stats_user_count
                        + '\n')
        __out.close()












