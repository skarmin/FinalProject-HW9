## Your name: Sam Karmin
## The option you've chosen: Option 2

# Put import statements you expect to need here!
import tweepy
import twitter_info
import unittest
import itertools
import re
import json
import sqlite3
import requests

#### TWEEPY SETUP CODE:
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Set up library to grab stuff from twitter with your authentication, and return it in a JSON format 
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

##### END TWEEPY SETUP CODE

#CACHING SYSTEM

CACHE_FNAME = "206_FinalProject_cache.json"
# Put the rest of your caching setup here:
try: 
	cache_file = open(CACHE_FNAME, 'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}


#CREATE MOVIE CLASS
class Movie():
	def __init__(self, movie_title):
		self.movie_title = movie_title
        # self.movie_director = movie_director
        # self.movie_IMBD = movie_IMBD

	def __str__(self):
		return "{} is directed by {} and received a an IMBD rating of {}".format(self.movie.title, self.movie_director, self.movie_IMBD)

	def get_movie_info(self):
		base_url = 'http://www.omdbapi.com/'
		full_url = requests.get(base_url, params = {"t": self.movie_title}).text

		if self.movie_title in CACHE_FNAME:
			omdb_response_text = CACHE_DICTION[self.movie_title] #Why response_text vs just response
		else:
			CACHE_DICTION[self.movie_title] = full_url
			omdb_response_text = full_url
			cache_file = open(CACHE_FNAME, 'w')
			cache_file.write(json.dumps(CACHE_DICTION))
			cache_file.close
		movie_dict = json.loads(omdb_response_text)
		
		actors = movie_dict['Actors']
		director = movie_dict['Director']
		rating = movie_dict['Ratings'][0]['Value']
		return actors, director, rating
	
	def get_twitter_info(self, actors):
		actor_tweets = {}
		for actor in actors:
			tweets = api.search(actor)
			actor_tweets[actor] = tweets

		return actor_tweets



Miracle = Movie("Miracle On Ice")
movie_info = Miracle.get_movie_info()
print (Miracle.get_twitter_info(movie_info[0]))


#GET TWitter info




# Write your test cases here.
# class CacheTesting(unittest.TestCase):
# 	def test_movie_cache(self):
# 		cache_file = open("SI206_FinalProject_cache.json","r").read()
# 		self.assertTrue("Movies" in cache_file)
# 	def test_twitter_cache(self):
# 		cache_file = open("SI206_FinalProject_cache.json","r").read()
# 		self.assertTrue("Tweets" in cache_file)
# class MovieTesting(unittest.TestCase):
# 	def test_Movie_str_method(self):
# 		movie_instance = Movie(movie_dic)
# 		self.assertEqual(type(movie_instance.__str__(), str))
# 	def test_get_actors_method(self):
# 		movie_instance = Movie(movie_instance)
# 		self.assertEqual(type(movie_instance.get_movie_actors()), list))
# 	def test_get_actors_method2(self):
# 		movie_instance = Movie(movie_instance)
# 		actors = movie_instance.get_movie_actors()[0]
# 		self.assertEqual(type(actors), list))
# 	def test_title_of_movie(self):
# 		movie_instance = Movie(movie_instance)
# 		self.assertEqual(type(movie_instance.tittle), str)
# 	def test_movie_tweets(self):
#  		self.assertEqual(type(movie_tweets),type([]))
#  	def test_actor(self):
#  		self.assertEqual(type(get_movie_actors[18]),type({"hi":3}))




## Remember to invoke all your tests...
# if __name__ == "__main__":
# 	unittest.main(verbosity=2)


