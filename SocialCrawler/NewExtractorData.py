# -*- coding: UTF-8 -*-
"""Extractor class to retrieve data from Foursquare.

# (c) J.Wirlino and A.Adativa
# Date Dec 22th 2016
# https://github.com/JosielWirlino/SocialCrawler

"""

from termcolor import colored
import sys
import urllib.request
from urllib.error import URLError, HTTPError
import linecache
# from pip._vendor.requests.exceptions import HTTPError
from SocialCrawler import HTTPResponseError
from socket import timeout
import time
import requests
import sys
import json





class NewExtractor:

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

    def __init__(self,
                 credentials=None,
                 foursquare_version="20140806%20",
                 foursquare_mode="swarm",
                 debug_mode=False
                 ):
        """Class constructor.
        
        Method to init all minimum settings necessary to get data froum Foursquare.
        
        Note:
            foursquare_mode and foursquare_version parameter are two specials parameters 
            to control over the kind of that Foursquare returns.
            see https://developer.foursquare.com/overview/versioning
        
            To see how can get crendetials see https://developer.foursquare.com/overview/auth
        
        Args:
            (obsolete)foursquare_client_id (str): Foursquare's app client id
            (obsolete)foursquare_client_secret (str): Foursquare's app client secret
            credentials: Array that contains foursquare_credentials
            foursquare_version (str): kind of Foursquare returns, by default "20140806%20" .
            foursquare_mode (str): foursquare mode answer. Valid value: "swarm"  or "foursquare" by default "swarm"
            (obsolete)developer_email (None, optional): Description
            (obsolete) developer_password (str) : password of email
        
        Attributes:
            credentials: Array that contains foursquare_credentials
            (obsolete)foursquare_client_id (str): Foursquare's app client id
            (obsolete)foursquare_client_secret (str): Foursquare's app client secret
            foursquare_version (str): kind of Foursquare returns
            foursquare_mode (str): foursquare mode answer
                                    valid value: "swarm"  or "foursquare"
            (obsolete)developer_email (str): email registed in developer foursquare web site
            (obsolete) developer_password (str) : if developer_email is passed this field must be too, otherwise will be ignored.
        
        Deleted Parameters:
            (optional)developer_email (str): email registed in developer foursquare web site
        """
        self.f_client_id = 0
        self.f_client_secret = 1
        self.c_index = 0
        self.DEBUG = debug_mode
        if len(credentials) == 0:
            print(colored('[INVALID PARAMETER] credentials must be setted.','red'),flush=True)
            sys.exit()
        
        self._credentials = credentials

        if self.DEBUG:
           

            print(colored("[CREDENTIAL] Contain %s credentials" %len(credentials),'green'),flush=True)
            print(colored('GET FIRST CREDENTIAL','green'),flush=True)
            print(colored("\tCREDENTIAL [" +str(self.c_index)+"]",'green'),flush=True)
            print(colored("\t\t[CLIENT ID] "+str(self._credentials[self.c_index][self.f_client_id]),'green'),flush=True)
            print(colored("\t\t[SECRET ID] "+str(self._credentials[self.c_index][self.f_client_secret]),'green'),flush=True)

        foursquare_mode_valid_value = {'swarm','foursquare'}

        if( foursquare_mode not in foursquare_mode_valid_value ):
            print(colored('[INVALID PARAMETER] foursquare_mode.','red'),flush=True)
            sys.exit()

        self._foursquare_version = foursquare_version
        self._foursquare_mode = foursquare_mode
        
        print(colored("[SETUP] OKAY",'green'),flush=True)


    def get_next_credential(self):
        result = False
        
        if(self.c_index < (len(self._credentials)-1)):
            self.c_index +=1
            print(colored('GET ANOTHER CREDENTIAL','green'),flush=True)
            print(colored("\tCREDENTIAL [" +str(self.c_index)+"]",'green'),flush=True)
            print(colored("\t\t[CLIENT ID] "+str(self._credentials[self.c_index][self.f_client_id]),'green'),flush=True)
            print(colored("\t\t[SECRET ID] "+str(self._credentials[self.c_index][self.f_client_secret]),'green'),flush=True)
            result = True
        else:
            self.c_index = 0
        return result

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

        self.__out = open( self._path_file + '/' + self._file_name + '.tsv','a')
        
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
         
            venue_id = self.get_swarm_data(line,number_line)
            if venue_id is "NONE":
                print(colored("[SWARM] ERROR DATA",'red'),flush=True)
                self.__out.write("\n")
                self.__out.flush()
                continue
            r = self.get_4square_data(venue_id)
            if(r is False):
                print(colored("[VENUE] ERROR DATA",'red'),flush=True)
                self.__out.write("\n")
                self.__out.flush()

            # except :
            #     print(colored('[UNKOWN] ERROR ','red' ),flush=True)
            #     continue
        self.__out.close()

    def ExceptionDetail(self):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f= exc_tb.tb_frame
        lineno = exc_tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        print ('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj) )

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

        try_again = True
        while try_again:
            try_again = False
            try:
                # print('Looking for t.co ...',flush=True)
                t_co_url = line_splitted[self._column]
                idx = t_co_url.index('https://t.co/')#get where start the url
                t_co_url = t_co_url[idx:idx+23]
                
                if self.DEBUG:
                    print(colored('\n\nFound and trying resolve ' +  t_co_url,'green'),flush=True)
                    # print(colored('Trying resolve '+t_co_url,'green'),flush=True)

                # swarm_t_co_resolved = requests.get(t_co_url)
                print(colored("Requesting...","green"),flush=True)
                swarm_t_co_resolved = urllib.request.urlopen(t_co_url,timeout=5)


            #be careful
            #HTTPError must come first see more https://docs.python.org/3.1/howto/urllib2.html#number-1
            except HTTPError as e:
                print(colored('[HTTP ERROR] ERROR CODE %s' %e.code,'red'),flush=True)
                return "NONE"
            except ValueError as e:
                print(colored('[VALUE ERROR] SWARM SHORT URL ERROR ','red'),flush=True)
                print(colored(e,"red"),flush=True)
                return "NONE"
            except ConnectionResetError as e:
                print(colored('[CONNECTION] RESET ERROR ','red'),flush=True)
                print(colored(e,"red"),flush=True)
                return "NONE"
            except ConnectionError as e:
                print(colored('[CONNECTION] ERROR ','red'),flush=True)
                print(colored(e,"red"),flush=True)
                return "NONE"
            except ConnectionAbortedError as e:
                print(colored('[CONNECTION] ABORTED ERROR ','red'),flush=True)
                print(colored(e,"red"),flush=True)
                return "NONE"
            except ConnectionRefusedError as e:
                print(colored('[CONNECTION] REFUSED ERROR ','red'),flush=True)
                print(colored(e,"red"),flush=True)
                return "NONE"
            except KeyboardInterrupt:
                print(colored('[SWARM][KEYBOARD] INTERRUPTED BY USER ','red'),flush=True)
                sys.exit()
            except URLError as e:
                print(colored('[URL ERROR] ','red'),flush=True)
                print(colored(e.reason,'red'),flush=True)
                # print("INFOS REASON "+ colored(e.reason.args[0],"red"),flush=True)
                errno_code = e.reason.args[0]

                if errno_code == -3:
                    print(colored("[CONNECTION DISABLED] MAYBE YOUR ADAPTER IS OFF ","red"),flush=True)
                    try_again = True
                elif errno_code == 111:
                    print(colored("[CONNECTION REFUSED] CHECK YOUR CONNECTION ","red"),flush=True)
                    try_again = True
                else:
                    return "NONE"
                time.sleep(5)#wait 5 second
                
            except :
                print(colored("[URL LIB][UNKOWN ERROR] " + str(sys.exc_info()[0]),"red") )
                self.ExceptionDetail()
                return "NONE"

        print(colored("REQUEST OKAY!","green"),flush=True)

        if self.DEBUG:
            print(colored("SWARM LINK SOLVED",'green'),flush=True)

        if self.swarm_prefix not in swarm_t_co_resolved.url:
            print(swarm_t_co_resolved.url,flush=True)
            print(colored('SWARM URL ERROR','red') ,flush=True)
            return "NONE"
        
        if self.DEBUG:
            print(colored("[SWARM] LINK RESOLVED "+swarm_t_co_resolved.url ,'green'),flush=True)
        
        key =  swarm_t_co_resolved.url[ len(swarm_t_co_resolved.url) - 11 : ] #get string after www.swarmapp.com/

        api_rate_limit = True
        watch_dog_while = 0
        while api_rate_limit and watch_dog_while < 5 :
            api_rate_limit = False
            try:
                response = requests.get( self.url_resolveID + key + 
                                          '&client_id=' + self._credentials[self.c_index][self.f_client_id] +
                                          '&client_secret=' + self._credentials[self.c_index][self.f_client_secret] +
                                          '&v=' + self._foursquare_version +
                                          '&m=' + self._foursquare_mode )

                swarm_data = response.json()
                
                error_type = error_code = "NULL"
                
                if str(swarm_data['meta']['code']) != str(200): #if get some error code
                    try:
                        error_code = swarm_data['meta']['code']
                    except:
                        error_code = "NULL"
                    try:
                        error_code = swarm_data['meta']['errorType']
                    except:
                        error_type = "NULL"

                    if HTTPResponseError.parse_error(error_code, error_type):
                        print(colored("[HTTPResponseError] Get some error","red"),flush=True)
                        raise Exception('[request meta code]')
                    # continue
            except HTTPError as e:
                # print(colored('HTTPERROR ','red'),flush=True)
                print(colored('[FOURSQUARE RESOLVE ID] ERROR ','red'),flush=True)
                print(colored(e.code,'red'),flush=True)

            except KeyboardInterrupt:
                print(colored('[API FOURSQUARE][KEYBOARD] INTERRUPTED BY USER ','red'),flush=True)
                sys.exit()
            except Exception as e :

                result = self.get_next_credential()
                print(colored('[API FOURSQUARE RESOLVE ID] RATE LIMIT ','red'),flush=True)
                print(colored("[API FOURSQUARE RESOLVE ID][UNKOWN ERROR] " + str(sys.exc_info()[0]),"red") )
                
                self.ExceptionDetail()

                watch_dog_while +=1

                if(result is False):
                    # print(colored('Wait 5 minutes to request again ','red'),flush=True)
                    print(colored('[API FOURSQUARE RESOLVE ID] SLEEP FOR 10 MIN ','red'),flush=True)
                    time.sleep(600) #sleep 10 min
                    print(colored('[API FOURSQUARE RESOLVE ID] I AM BACK ','red'),flush=True)
                    # api_rate_limit = True
                else:
                    # print(colored('[API FOURSQUARE RESOLVE ID] GET ANOTHER CREDENTIAL ','red'),flush=True)
                    print(colored('[API FOURSQUARE RESOLVE ID] TRYING REQUEST THE LAST URL','red'),flush=True)
                api_rate_limit = True

        watch_dog_while = 0
        try:
            checkin_user_id=swarm_data['response']['checkin']['user']['id']
        except:
            print(colored('SWARM CHECKIN ERROR [PARSER USER_ID]','red'),flush=True)
            checkin_user_id = "NULL"
            if self.DEBUG:
                print("\n\n")
                print(swarm_data)
                print("\n\n")
            if HTTPResponseError.parse_error(swarm_data['meta']['code'], swarm_data['meta']['errorType']):
                print(colored("[HTTPResponseError] Get some error","red"),flush=True)
                result = self.get_next_credential()
                if(result is False):
                    time.sleep(600) #without new credential..wiat 10 minutes
                
                # raise Exception('[request meta code]')

                # sys.exit()
            
        try:
            checkin_user_gender=swarm_data['response']['checkin']['user']['gender']
        except:
            print(colored('SWARM CHECKIN ERROR [PARSER GENDER]','red'),flush=True)
            checkin_user_gender = "NULL"
            
        # if self.DEBUG:
        #     print(self._path_file + '/' + self._file_name + '.tsv',flush=True)
        print(colored("[SWARM DATA] WRITING IN THE FILE!","green"),flush=True)
        self.__out.write( line_splitted[3] \
                    +"\t"+str(line_splitted[1]) \
                    +"\t"+str(checkin_user_id) \
                    +"\t"+checkin_user_gender \
                    +"\t"+line_splitted[2] \
                    +"\t")
        self.__out.flush()

        swarm_data_venue_id = "NONE"
        try:
            # print(colored("",'red'))
            if self.DEBUG:
                print(colored("[SWARM] SAVED DATA.\n[VENUE DETAIL] RETRIEVING",'green'),flush=True)
            swarm_data_venue_id = swarm_data['response']['checkin']['venue']['id']

        except:
            print(colored("[SWARM] WITHOUT DATA OR VENUE ID",'red'))
            swarm_data_venue_id = "NONE"

        return swarm_data_venue_id

    def get_4square_data(self, venue_id=None):
        """Method to retrieve venue information
        
        Args:
            venue_id (TYPE): venue id
            __out (TYPE): output file
        
        Returns:
            TYPE: Description
        """
        api_venue_rate_limit = True
        
        

        while api_venue_rate_limit:
            api_venue_rate_limit = False
            # venue_data = []
            try:
                
                response = requests.get(self.url_venue \
                                        + venue_id \
                                        + '?client_id=' \
                                        + self._credentials[self.c_index][self.f_client_id] \
                                        + '&client_secret=' \
                                        + self._credentials[self.c_index][self.f_client_secret] \
                                        + '&v=' \
                                        + self._foursquare_version \
                                        )
                venue_data = response.json()

            except HTTPError as e:
                print(colored('[HTTP ERROR] VENUE DETAIL ','red'),flush=True)
                print(colored(e,'red'),flush=True)
                api_venue_rate_limit = False
                # return False
            except UnboundLocalError as e:
                print(colored('[UNBOUND]','red'),flush=True)
                print(colored(e,'red'),flush=True)
                api_venue_rate_limit = False

            except :
                c_id = str(self._credentials[self.c_index][self.f_client_id])
                s_id = str(self._credentials[self.c_index][self.f_client_secret])

                if self.DEBUG:
                    print(self.url_venue + venue_id +'?client_id=' + str(c_id) )

                print(colored('[VENUE DETAIL] RATE LIMIT','red'),flush=True)
                print(colored("[VENUE DETAIL][UNKOWN ERROR] " + str(sys.exc_info()[0]),'red') )
                self.ExceptionDetail()

                result = self.get_next_credential()

                if(result is False):
                    # print(colored('Wait one 5 minutes to request again ','red'),flush=True)
                    print(colored('[VENUE DETAIL] SLEEP FOR 5 MIN','red'),flush=True)
                    time.sleep(300) #sleep 5 minutes
                    print(colored('[VENUE DETAIL] I AM BACK','red'),flush=True)
                    # api_venue_rate_limit =  True
                else:
                    # print(colored('[VENUE DETAIL] GET ANOTHER CREDENTIAL','red'),flush=True)
                    print(colored('[VENUE DETAIL] TRYING REQUEST THE LAST URL','red'),flush=True)

                api_venue_rate_limit =  True

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
            print(colored("[VENUE DETAIL] SAVED DATA","green"),flush=True)

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