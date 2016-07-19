from SocialCrawler import HistoricalCollector

api_key = "udF1vZod9mIWADiwCS5GwMjNI"
api_secret = "omR4g3tfFciQvgraNHnL4ur2cOo3x7viGdBypog5EdNwnK1NZh"
access_token = "4717654877-x2rcMWisECAD0peOEvmFRANLQnKUMICdMvh1HCJ"
access_secret = "pK7CBPJHFXgSKZNrg2ohibNWRQS0sNX0cbXIcSfcL6guB"

test = HistoricalCollector.Collector(api_key,api_secret, access_token, access_secret)
since='2016-07-11'
until='2016-07-18'
# test.getStoredData('swarmapp.com',since,until,'Rio de Janeiro','-22.911233,-43.448334,100km','Log/')


international_capitals_geocode_dict = {}
international_capitals_geocode_dict.update({'Bandung': '-6.903449,107.643158,100km'}) # Indonesia
international_capitals_geocode_dict.update({'Bangkok': '13.724601,100.633111,100km'}) # Thailand
international_capitals_geocode_dict.update({'Barcelona': '41.39479,2.148768,100km'}) # Spain
international_capitals_geocode_dict.update({'Buenos Aires': '-34.615824,-58.43332,100km'}) # Argentina
international_capitals_geocode_dict.update({'Chicago': '41.833733,-87.732155,100km'}) # USA
international_capitals_geocode_dict.update({'Istanbul': '41.005322,29.012179,100km'}) # Turkey
international_capitals_geocode_dict.update({'Jakarta': '6.229746,106.829518,100km'}) # Indonesia
international_capitals_geocode_dict.update({'Kuala Lumpur': '3.139003,101.686855,100km'}) # Malaysia
international_capitals_geocode_dict.update({'Kuwait City': '29.376065,47.981867,100km'}) # Kuwait
international_capitals_geocode_dict.update({'London': '51.528642,-0.101599,100km'}) # UK
international_capitals_geocode_dict.update({'Los Angeles': '34.020499,-118.411732,100km'}) # USA
international_capitals_geocode_dict.update({'Madrid': '40.437954,-3.679537,100km'}) # Spain
international_capitals_geocode_dict.update({'Manila': '14.598072,120.979651,100km'}) # Philippines
international_capitals_geocode_dict.update({'Melbourne': '37.860283,145.079616,100km'}) # Australia
international_capitals_geocode_dict.update({'Mexico City': '19.390734,-99.143613,100km'}) # Mexico
international_capitals_geocode_dict.update({'Moscow': '55.749792,37.632495,100km'}) # Russia
international_capitals_geocode_dict.update({'New York': '40.70565,-73.978003,100km'}) # USA
international_capitals_geocode_dict.update({'Osaka': '34.6784,135.49515,100km'}) # Japan
international_capitals_geocode_dict.update({'Paris': '48.858859,2.347557,100km'}) # France
international_capitals_geocode_dict.update({'San Francisco': '37.7577,-122.4376,100km'}) # USA
international_capitals_geocode_dict.update({'Santiago': '-33.472788,-70.629831,100km'}) # Chile
international_capitals_geocode_dict.update({'Semarang': '-7.024775,110.418848,100km'}) # Indonesia
international_capitals_geocode_dict.update({'Seoul': '37.5651,126.98955,100km'}) # Korea
international_capitals_geocode_dict.update({'Singapore': '1.314731,103.847019,100km'}) # Singapore
international_capitals_geocode_dict.update({'Surabaya': '-7.275619,112.711684,100km'}) # Indonesia
international_capitals_geocode_dict.update({'Sidney': '33.796923,150.922433,100km'}) # Australia
international_capitals_geocode_dict.update({'Tokyo': '35.673343,139.710388,100km'}) # Japan

# Brazilian capitals geocode list
brazilian_capitals_geocode_dict = {}
brazilian_capitals_geocode_dict.update({'Rio Branco': '-9.986331,-67.831097,100km'})  # Acre
brazilian_capitals_geocode_dict.update({'Maceio': '-9.593443,-35.686679,100km'})  # Alagoas
brazilian_capitals_geocode_dict.update({'Macapa': '0.101772,-51.096861,100km'})  # Amapá
brazilian_capitals_geocode_dict.update({'Manaus': '-3.044662,-59.967104,100km'})  # Amazonas
brazilian_capitals_geocode_dict.update({'Salvador': '13.802994,-88.905336,100km'})  # Bahia
brazilian_capitals_geocode_dict.update({'Fortaleza': '-3.791351,-38.519271,100km'})  # Ceará
brazilian_capitals_geocode_dict.update({'Brasilia': '-15.721762,-47.938236,100km'})  # Distrito Federal
brazilian_capitals_geocode_dict.update({'Vitoria': '-20.282192,-40.286247,100km'})  # Espírito Santo
brazilian_capitals_geocode_dict.update({'Goiania': '-16.695876,-49.304267,100km'})  # Goiás
brazilian_capitals_geocode_dict.update({'Sao Luis': '-2.560632,-44.258122,100km'})  # Maranhão
brazilian_capitals_geocode_dict.update({'Cuiaba': '-15.614407,-56.041807,100km'})  # Mato Grosso
brazilian_capitals_geocode_dict.update({'Campo Grande': '-20.4811,-54.635534,100km'})  # Mato Grosso do Sul
brazilian_capitals_geocode_dict.update({'Belo Horizonte': '-19.902716,-43.96405,100km'})  # Minas Gerais
brazilian_capitals_geocode_dict.update({'Belem': '-1.267194,-48.417908,100km'})  # Pará
brazilian_capitals_geocode_dict.update({'João Pessoa': '-7.146609,-34.881636,100km'})  # Paraíba
brazilian_capitals_geocode_dict.update({'Curitiba': '-25.495117,-49.289798,100km'})  # Paraná
brazilian_capitals_geocode_dict.update({'Recife': '-8.043311,-34.936199,100km'})  # Pernambuco
brazilian_capitals_geocode_dict.update({'Teresina': '-5.09374,-42.741078,100km'})  # Piauí
brazilian_capitals_geocode_dict.update({'Rio de Janeiro': '-22.911233,-43.448334,100km'})  # Rio de Janeiro
brazilian_capitals_geocode_dict.update({'Natal': '-5.799919,-35.222245,100km'})  # Rio Grande do Norte
brazilian_capitals_geocode_dict.update({'Porto Alegre': '-30.10887,-51.176905,100km'})  # Rio Grande do Sul
brazilian_capitals_geocode_dict.update({'Porto Velho': '-8.756546,-63.854907,100km'})  # Rondônia
brazilian_capitals_geocode_dict.update({'Boa Vista': '2.807199,-60.696562,100km'})  # Roraima
brazilian_capitals_geocode_dict.update({'Florianopolis': '-27.610342,-48.484581,100km'})  # Santa Catarina
brazilian_capitals_geocode_dict.update({'Sao Paulo': '-23.572008,-46.609375,100km'})  # São Paulo
brazilian_capitals_geocode_dict.update({'Aracaju': '-11.001402,-37.103468,100km'})  # Sergipe
brazilian_capitals_geocode_dict.update({'Palmas': '-10.26006,-48.347234,100km'})  # Tocantins

international_cities = international_capitals_geocode_dict.keys()
# print( international_cities)
# print("\n",international_capitals_geocode_dict.get(international_geo))
for city in international_cities:
	test.getStoredData('swarmapp.com',
						since,
						until,
						city,
						international_capitals_geocode_dict.get(city),
						'Log/')

brazilian_capitals = brazilian_capitals_geocode_dict.keys()
for city in brazilian_capitals:
	test.getStoredData('swarmapp.com',
						since,
						until,
						city,
						brazilian_capitals_geocode_dict.get(city),
						'Log/')

#track=['partiu','#partiu','Oi','Boa Noite','noite','night',]
#test.getStreamData(track,'Log/')