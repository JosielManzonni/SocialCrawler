from setuptools import setuptools

setup( name='TwitterSwarm4Square-DataMining',
	version='0.1',
	description='This package allow get data from Twitter, Swarm and Foursquare',
	url='http://github.com/JosielWirlino/TwitterSwarm4Square-DataMining',
	author='J.Wirlino',
	author_email='josiel.wirlino@gmail.com',
	license='GNU',
	packages=['twesquarearm'],
	install_requires=['tweepy',
					  ],
	zip_safe=False
	)