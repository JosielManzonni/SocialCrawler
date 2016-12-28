# from SocialCrawler import NewExtractorData

# client_id = "GEQQO0MJPKLUTBIZHERRYQJUCTU5W2MGFAHZKCDB3LYB1GZI"
# client_secret = "QMXESMEH1VKEEKUQ0EBXNCJ4IWCK0EYHA0MUHNVBMGSWXRUZ"

# file_name = "Brasillog_from_Cuiaba__2016-08-28__2016-09-05.tsv"



# test = NewExtractorData.NewExtractor(client_id,client_secret,developer_email="josiel.wirlino@gmail.com",developer_password ="j0sielengenheiro")

# indice = 0
# # while( indice < 4):

# test.settings(mode="v1",
# 			  out_file_name="cuiaba_final_agosto",
# 			  out_path_file="/home/wirlino/Documents/Git/SocialCrawler/SocialCrawler/",
# 			  input_file="/home/wirlino/Documents/Git/SocialCrawler/SocialCrawler/"+file_name			  
# 			  )

# """ We are setting mode to v1 that means the file was created by or Collector or CollectorV2
#     output file created will be log_new_york.tsv and will be saved in ./Log/
#     the input file ( that contains t.co url ) are localed in ./Log/Brasil/ folder
# """

# test.consult_foursquare()

import threading
import re
import os,glob
import unicodedata
from SocialCrawler.NewExtractorData import NewExtractor
from termcolor import colored

def remove_accents(input_str):
    """
    get from http://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-in-a-python-unicode-string
    """

    enconding = 'utf-8'
    b_string = input_str.decode(enconding)
    nfkd_form = unicodedata.normalize('NFKD', b_string)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def get_file_output_name(input_file):
    # ifile = remove_accents(input_file)
    # regex = "(?<=from_)\w+_?\d{2}-\d{2}-\d{2}"
    regex = "(?<=from_).+"
    r_compiled = re.compile(regex)
    matched = r_compiled.search(input_file)
    # if matched.group())
    # print(input_file)
    if matched:
        return matched.group(0)
    else:
        return None
credentials = []

credentials =[ ["GEQQO0MJPKLUTBIZHERRYQJUCTU5W2MGFAHZKCDB3LYB1GZI",
                "QMXESMEH1VKEEKUQ0EBXNCJ4IWCK0EYHA0MUHNVBMGSWXRUZ"],

                ["JGX5VIAPVC25BZ4Y1LFIPX2JEJDKXAB3XMDAHBOYAXBNDFEV",
                "VVWNSTM1G2CFTEEL21ENRDOLUYJY5JWKOBYBPO4WYUZIPTWF"],
                
                ["AUU4MDBWNNTWSWF00QUVFOIOWLYK1ASZUXGUCOMZQGBB52OX",
                "R1O1MXOUZ3EHDNXSJFNJI5DTWMZFRDYKJX5SKE3DU5CAXXKI"],
                
                ["TOJ5E0V0ECJSXJUJOJOINPHGSLCKK1CGEBVGZXVE3JPNLP0R",
                "N4ZDB2KOPUOCRSHI3K12UFZ0VOJOVGE0H44WX4NG4Y1L1W0P"],

                ["NP3N1NYNYNFRE4JHE4G1SK44WGENYYC4HB4YFADDAFB5GM1M",
                "AXGB42JOEQADTXRU304UAZAJ5DQNIND15KEPVN4ZWMDNMPRN"]
              ]

path_from = "/home/paradox/Documents/"
path_to = "/home/paradox/Documents/Brasil_4Square"


#file_name_list = [path+"log_from_Aracaju__2016-11-14__2016-11-19.tsv",
#                  path+"Brasillog_from_Belem__2016-08-28__2016-09-05.tsv",
#                  path+"Brasillog_from_CampoGrande__2016-08-28__2016-09-05.tsv",
#                  path+"Brasillog_from_SaoPaulo__2016-08-28__2016-09-05.tsv",
#                  path+"log_from_Belem__2016-08-28__2016-09-05.tsv"
#                  ]

retrieve_item = 0

os.chdir(path_from+"Brasil_Data")
brasil_file_list = []
inter_file_list = []

for file in glob.glob("*.tsv"):
    brasil_file_list.append(file)
    # print(file )
    # retrieve_item += 1

r_1 = NewExtractor(credentials=credentials)

def get_thread( thread_api_4square, thread_id):
    global retrieve_item
    global brasil_file_list
    print("Thread %s started " %thread_id)
    print("Retrieve item: %s"%retrieve_item)
    print("File list contains %s elements"%len(brasil_file_list))
    while retrieve_item < len(brasil_file_list):
        retrieve_item += 1
        f_name = get_file_output_name( brasil_file_list[retrieve_item-1])
        
        if f_name is None:
        	f_name = brasil_file_list[retrieve_item-1]
        f_name = f_name[:len(f_name)-4]

        print(colored("Thread "+str(thread_id) +" reading " + brasil_file_list[retrieve_item-1],'red'))
        
        thread_api_4square.settings(mode="v1",
			  out_file_name="foursquare_"+f_name,
			  out_path_file=path_to,
			  input_file=path_from+"Brasil_Data/"+brasil_file_list[retrieve_item-1] 
			  )
        # for line in open(file_name_list[retrieve_item-1],'r'):
        #     a = 1
        thread_api_4square.consult_foursquare()
        
        print(colored("Thread "+str(thread_id) + " done",'red') )


t1 = threading.Thread(target=get_thread,args=(r_1,"t1",))
# t2 = threading.Thread(target=get_thread,args=(r_2,"t2",))
# t3 = threading.Thread(target=get_thread,args=(r_3,"t3",))
# t4 = threading.Thread(target=get_thread,args=(r_4,"t4",))
# t5 = threading.Thread(target=get_thread,args=(r_5,"t5",))

t1.start()
# t2.start()
# t3.start()
# t4.start()
# t5.start()

# t2.start()





