# -*- coding: UTF-8 -*-
"""Extractor class to retrieve data from Foursquare.

# (c) J.Wirlino and A.Adativa
# Date Sept 1th 2016
# https://github.com/JosielWirlino/SocialCrawler

"""

from termcolor import colored
# import json
import sys
# import time


class Extractor:
    """Read log file from Collector .

    ( or files that contains a swarm url code).s

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
    
    def settings(self,mode=None,out_file_name=None,out_path_file=None,column=None,input_file=None):
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
