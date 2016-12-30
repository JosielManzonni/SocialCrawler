# -*- coding: UTF-8 -*-
"""Test of Extractor class to retrieve data from Foursquare.

# (c) J.Wirlino and A.Adativa
# Date Dec 29th 2016
# https://github.com/JosielWirlino/SocialCrawler

"""

from SocialCrawler import NewExtractorData

client_id = "--"
client_secret = "--"

credentials = [
				[client_id,client_secret]
			  ]

file_name = "log_from_Vitoria2016-08-17__2016-08-22.tsv"

 #debug_mode enable or disable ALL output message in run flow
 ##We agree that is more interisting be setted to False, True it is more debug step-by-step
test = ExtractorData.NewExtractor(credentials=credentials, debug_mode=False)

test.settings(mode="v1", \
			  out_file_name="log_new_york", \
			  out_path_file="Log", \
			  input_file='Log/Brasil/'+file_name, \
			  )

""" We are setting mode to v1 that means the file was created by or Collector or CollectorV2
    output file created will be log_new_york.tsv and will be saved in ./Log/
    the input file ( that contains t.co url ) are localed in ./Log/Brasil/ folder
"""

test.consult_foursquare()

"""Call this metho will start te foursquare consult. """

# print("Mensagem ", end="")
# print(" mesma linha")