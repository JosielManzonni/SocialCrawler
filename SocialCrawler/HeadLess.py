# -*- coding: UTF-8 -*-
"""Extractor class to retrieve data from Foursquare.

# (c) J.Wirlino and A.Adativa
# Date Dec 22th 2016
# https://github.com/JosielWirlino/SocialCrawler

"""

from termcolor import colored
import sys
import urllib.request
from urllib.error import URLError
from pip._vendor.requests.exceptions import HTTPError
import time
import requests
import json

from SocialCrawler import HackFoursquare


f_client_id = 0
f_client_secret = 1
c_index = 0


class HeadLess:

    """Read log file from Collector .
    ( or files that contains a swarm url code)
    This class use tools and keywords from Foursquare API Endpoints.
        Note:
            If has a another file that was not created by Collector you must
            have set.column parameter with a integer saying the file column that
            has swarm url. All file input must be *.tsv .
        
    """

    def __init__(self,
                 developer_email=None,
                 developer_password=None,
                 mode="show",
                 debug=False
                 ):
        """Class constructor.
        
        Method to init all minimum settings necessary to get data froum Foursquare.
        
        Note:
            foursquare_mode and foursquare_version parameter are two specials parameters 
            to control over the kind of that Foursquare returns.
            see https://developer.foursquare.com/overview/versioning
        
            To see how can get crendetials see https://developer.foursquare.com/overview/auth
        
        Args:
            foursquare_version (str): kind of Foursquare returns, by default "20140806%20" .
            foursquare_mode (str): foursquare mode answer. Valid value: "swarm"  or "foursquare" by default "swarm"
            developer_email (None, optional): Description
            developer_password (str) : password of email
        
        Attributes:
            foursquare_version (str): kind of Foursquare returns
            foursquare_mode (str): foursquare mode answer
                                    valid value: "swarm"  or "foursquare"
            developer_email (str): email registed in developer foursquare web site
            developer_password (str) : if developer_email is passed this field must be too, otherwise will be ignored.
        
        """
        self.DEBUG = debug
        
        foursquare_mode_valid_value = {'swarm','foursquare'}
        
        if ( developer_email is not None and developer_password is not None ):
        #     self.hacking_enable = True
            self._hacking = HackFoursquare.Hacking(developer_email, developer_password,mode)
            self._hacking.open_browser()
        
        if self.DEBUG:
            print("[HEADLESS] Setup okay",flush=True)

    def settings(self,mode=None,out_file_name=None,out_path_file=None,column=4,input_file=None):
        """Class constructor.
        
        Method to read log file created by Collector class
        and get Swarm's url code and consult Foursquare to retrieve
        information about avenue, local type, shared_count and all information that is
        returned than will save in a file called log_<out_file_name>.tsv
        
        Args:
            mode (str): json file version.
                         mode valid value:
                         - v1 if the file was created from Collector class or CollectorV2 class
                         - v2 if was not created by any Collector but has the Swarm url
                                  if the value is v2 the "column" parameter must be setted
            out_file_name (str): File name to be created.
            out_path_file (str): File path where the file must be saved.
            column (int): column that contain the Swarm url. This field is only
                           verified if "mode" is v2 .
            input_file (None, optional): Description
        
        Deleted Parameters:
            input_file(str): file that contains swarm url code
        
        """
        mode_valid_value = {'v1','v2'}

        if(mode is None or out_file_name is None or out_path_file is None or input_file is None):
            print(colored('Any parameter can be None except column field iff mode is not v2. ','red'),flush=True)
            sys.exit()

        if(mode not in mode_valid_value ):
            print(colored('mode value invalid.','red'),flush=True)
            sys.exit()

        self._file_name = out_file_name
        self._path_file = out_path_file
        self._mode = mode
        self._input_file = input_file
        self._column = column
        if(mode == "v2"):
            if(column is None ):
                print(colored("When mode is v2, column field must be assigned",'red'),flush=True)
                sys.exit()
            self._column = column


    def consult_foursquare(self):
        """Method to access foursquare and use resolveId.
        
        This method is called to each line read from input file, so
        all attributes of credentials function must be setted correctly
        
        resolvedId is a function from Foursquare API Endpoints to get data from a swarm url code.
        see https://developer.foursquare.com/docs/
        """
        self.swarm_prefix = "https://www.swarmapp.com/c/"
        self.url_venue = 'https://api.foursquare.com/v2/venues/'
        self.url_resolveID = 'https://api.foursquare.com/v2/checkins/resolve?shortId='

        if(self._mode is None or self._file_name is None or self._path_file is None or self._input_file is None):
            print(colored('One or more attributes are None. Firstly you must call settings method and than you call this method ','red'),flush=True)
            sys.exit()

        self.__out = open( self._path_file + '/' + self._file_name + '.tsv','w')
        
        #set file header
        self.__out.write( 'checkin_createdAt' \
                    + '\t' + 'twitter_user_id' \
                    + '\t' + '4square_user_id' \
                    + '\t' + 'user_gender' \
                    + '\t' + 'venue_city' \
                    + '\t' + 'venue_id' \
                    + '\t' + 'venue_lat' \
                    + '\t' + 'venue_lng' \
                    + '\t' + 'venue_categories_id' \
                    + '\t' + 'venue_categories_name' \
                    + '\t' + 'venue_stats_checkinsCount' \
                    + '\t' + 'venue_stats_userCount' \
                    + '\t' + 'venue_rating' \
                    + '\t' + 'venue_parent_id' \
                    + '\t' + 'venue_parent_categories_id' \
                    +'\n')
        self.__out.flush()
        
        number_line = 0
        for line in open(self._input_file, 'r'):
            number_line = number_line + 1
            # print("File opened",flush=True)
            # print(line,flush=True)
            # try:
            venue_id = self.get_swarm_data(line,number_line)
            if venue_id is "NONE":
                print("ERROR SWARM DATA",flush=True)
                self.__out.write("\n")
                self.__out.flush()
                continue
            r = self.get_4square_data(venue_id)
            if(r is False):
                print("ERROR 4SQUARE DATA",flush=True)
                self.__out.write("\n")
                self.__out.flush()

            # except :
            #     print(colored('[UNKOWN] ERROR ','red' ),flush=True)
            #     continue
        self.__out.close()

    def get_swarm_data(self,file_line=None,number_line=None,):
        """Method to get swarm data from a t.co url
        Args:
            file_line: line from file that contains
            number_line: line of file that are being read
            __out (TYPE): Description
            t.co url
        Return 
            venue_id
        
        """
        # print("SWARM ",flush=True)
        line_splitted = file_line.split('\t')
        swarm_t_co_resolved = "NONE"
        try:
            # print('Looking for t.co ...',flush=True)
            t_co_url = line_splitted[self._column]
            
            if self.DEBUG:
                print('Found t.co ' +  t_co_url,flush=True)
            
            idx = t_co_url.index('https://t.co/')#get where start the url
            t_co_url = t_co_url[idx:idx+23]
            
            if self.DEBUG:
                print('Trying resolve '+t_co_url,flush=True)
            
            swarm_t_co_resolved = urllib.request.urlopen(t_co_url)

        except HTTPError as e:
                print(colored('URLLIB URLOPEN FAILED ERROR CODE %s' %e.code,'red'),flush=True)
        except ValueError as e:
            print(colored(' SWARM SHORT URL ERROR ','red'),flush=True)
            print(e,flush=True)
            return "NONE"

        except URLError as e:
            print(colored(' URL ERROR ','red'),flush=True)
            print(e,flush=True)
            return "NONE"
        except ConnectionResetError as e:
            print(colored(' CONNECTION RESET ERROR ','red'),flush=True)
            print(e,flush=True)
            return "NONE"
        except ConnectionError as e:
            print(colored(' CONNECTION ERROR ','red'),flush=True)
            print(e,flush=True)
            return "NONE"
        except ConnectionAbortedError as e:
            print(colored(' CONNECTION ABORTED ERROR ','red'),flush=True)
            print(e,flush=True)
            return "NONE"
        except ConnectionRefusedError as e:
            print(colored(' CONNECTION REFUSED ERROR ','red'),flush=True)
            print(e,flush=True)
            return "NONE"
        except :
            print(colored(' URLLIB ERROR','red'),flush=True)
            return "NONE"

        if self.DEBUG:
            print(colored("SWARM SOLVED",'green'),flush=True)

        if self.swarm_prefix not in swarm_t_co_resolved.url:
            print(swarm_t_co_resolved.url,flush=True)
            print(colored('SWARM URL ERROR','red') ,flush=True)
            return "NONE"

        if self.DEBUG:
            print("resolved sucessfully. Link resolved is "+swarm_t_co_resolved.url ,flush=True)
        
        key =  swarm_t_co_resolved.url[ len(swarm_t_co_resolved.url) - 11 : ] #get string after www.swarmapp.com/
        
        global f_client_id
        global f_client_secret
        global c_index

        api_rate_limit = True
        
        while api_rate_limit:
            api_rate_limit = False
            try:
                response = self._hacking.get_info_detail(v="swarm",key_id=key)
                # print(response)
                swarm_data = json.loads(response)
                # swarm_data = response.json()

            except HTTPError as e:
                # print(colored('HTTPERROR ','red'),flush=True)
                print(colored('[CHECK RESOLVE ID] ERROR ','red'),flush=True)
                print(colored(e,'red'),flush=True)
                
            except :
                
                print(colored('[BROWSER FAIL] SLEEP FOR 5 SECONDS ','red'),flush=True)
                # self._hacking.debug()
                self._hacking.rebuild()
                time.sleep(5)
                print(colored('[BROWSER FAIL] I AM BACK ','red'),flush=True)
                api_rate_limit = True

        try:
            checkin_user_id=swarm_data['response']['checkin']['user']['id']
        except:
            print(colored('SWARM CHECKIN ERROR [PARSER CHECKIN_ID]','red'),flush=True)
            checkin_user_id = "NULL"
            
        try:
            checkin_user_gender=swarm_data['response']['checkin']['user']['gender']
        except:
            print(colored('SWARM CHECKIN ERROR [PARSER CHECKIN_ID]','red'),flush=True)
            checkin_user_gender = "NULL"
            
        if self.DEBUG:
            print(self._path_file + '/' + self._file_name + '.tsv',flush=True)

        self.__out.write( line_splitted[3] \
                    +"\t"+str(line_splitted[1]) \
                    +"\t"+str(checkin_user_id) \
                    +"\t"+checkin_user_gender \
                    +"\t"+line_splitted[2] \
                    +"\t")
        self.__out.flush()

        swarm_data_venue_id = "None"
        # if swarm_data['meta']['code'] == 200:
        try:
            print("Saved swarm data. Going to retrieve Foursquare data.",flush=True)
            swarm_data_venue_id = swarm_data['response']['checkin']['venue']['id']
            return swarm_data_venue_id
        except:
            return "NONE"

    def get_4square_data(self, venue_id=None):
        """Method to retrieve venue information
        
        Args:
            venue_id (TYPE): venue id
            __out (TYPE): output file
        
        Returns:
            TYPE: Description
        """
        api_venue_rate_limit = True
        
        global f_client_id
        global f_client_secret
        global c_index

        while api_venue_rate_limit:
            api_venue_rate_limit = False
            venue_data = "NONE"
            try:
                response = self._hacking.get_info_detail(v="v",key_id=venue_id)
                venue_data = json.loads(response)

            except HTTPError as e:
                print(colored('[HTTP ERROR] VENUE DETAIL ','red'),flush=True)
                print(colored(e,'red'),flush=True)
                # return False
            except :
                print(colored('[VENUE DETAIL] RATE LIMIT','red'),flush=True)
                # if self.hacking_enable==True:
                #     print(colored('STARTING HACKING BROWSER','green'),flush=True)
                #     response = self._hacking.get_venue_detail(venue_id)
                #     venue_data = json.loads(response)
                #     # api_venue_rate_limit =  False

                # else:
                # result = self.get_next_credential()
                # if(result is False):
                #     # print(colored('Wait one 5 minutes to request again ','red'),flush=True)
                print(colored('[VENUE DETAIL] SLEEP FOR 5 SECONDS','red'),flush=True)
                
                # self._hacking.debug()
                self._hacking.rebuild()
                time.sleep(5) #sleep 10 seconds
                #     print(colored('[VENUE DETAIL] I AM BACK','red'),flush=True)
                #     # api_venue_rate_limit =  True
                # else:
                #     print(colored('[VENUE DETAIL] GET ANOTHER CREDENTIAL','red'),flush=True)
                #     print(colored('[VENUE DETAIL] TRYING REQUEST THE LAST URL','red'),flush=True)

                api_venue_rate_limit =  True
                # rebuild

                # return False


        try:
            venue_lat = venue_data['response']['venue']['location']['lat']
        except:
            venue_lat = "NULL"

        try:
            venue_lng = venue_data['response']['venue']['location']['lng']
        except:
            venue_lng = "NULL"

        try:
            venue_categories_id = venue_data['response']['venue']['categories'][0]['id']
        except:
            venue_categories_id = "NULL"

        try:
            venue_categories_name = venue_data['response']['venue']['categories'][0]['name']
        except:
            venue_categories_name = "NULL"

        try:
            venue_stats_checkinsCount = venue_data['response']['venue']['stats']['checkinsCount']
        except:
            venue_stats_checkinsCount = "NULL"

        try:
            venue_stats_users_counts = venue_data['response']['venue']['stats']['usersCount']
        except:
            venue_stats_users_counts = "NULL"

        try:
            venue_rating = venue_data['response']['venue']['rating']
        except:
            venue_rating = "NULL"

        try:
            venue_parent_id = venue_data['response']['venue']['parent']['id']
        except:
            venue_parent_id = "NULL"

        try:
            venue_parent_categories_id = venue_data['response']['venue']['parent']['categories']['id']
        except:
            venue_parent_categories_id = "NULL"

        if self.DEBUG:
            print(self._path_file + '/' + self._file_name + '.tsv',flush=True)

        self.__out.write( venue_id \
                    +"\t"+str(venue_lat) \
                    +"\t"+str(venue_lng) \
                    +"\t"+str(venue_categories_id) \
                    +"\t"+str(venue_categories_name) \
                    +"\t"+str(venue_stats_checkinsCount) \
                    +"\t"+str(venue_stats_users_counts) \
                    +"\t"+str(venue_rating) \
                    +"\t"+str(venue_parent_id) \
                    +"\t"+str(venue_parent_categories_id) \
                    +"\n")
        self.__out.flush()
        return True