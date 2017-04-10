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

#### TWEEPY SETUP CODE:
# Authentication information should be in a twitter_info file...
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

CACHE_FNAME = "I206_FinalProject_cache.json"
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
	def __init__(self, movie_dict):
        self.movie_dict = movie_dict   #confused about this part
        self.movie_title = movie.title
        self.movie_director = movie_director
        self.movie_IMBD = movie_IMBD


    def __str__(self):
        return "{} is directed by {} and received a an IMBD rating of {}".format(self.movie.title, self.movie_director, self.movie_IMBD)

	def get_movie_actors(self):
		base_url = 'http://www.omdbapi.com/'
		full_url = requestURL(base_url, params = {"t": self.movie_title})

		if self.movie_title in CACHE_FNAME:
			omdb_response_text = CACHE_DICTION[full_url]
		else:
			omdb_response = requests.get(full_url)
			CACHE_DICTION[full_url] = omdb_response.text
			omdb_response_text = omdb_response.text

			cache_file = open(CACHE_FNAME, 'w')
			cache_file.write(json.dumps(CACHE_DICTION))
			cache_file.close
		return json.loads(omdb_response_text) #DOES THIS RETURN A DICTIOANRY?? IT SHOULD! Also, need to just grab the INFO aobut actors,not the entire movie!
		



		##########THIS EXAMPLE WORKS, DOES IT WORK FOR THIS METHOD AS WELL######
		# if full_url in omdb_cache_diction:
		# 	omdb_response_text = omdb_cache_diction[full_url]
		# else:
		# 	omdb_response = requests.get(full_url)
		# 	omdb_cache_diction[full_url] = omdb_response.text
		# 	omdb_response_text = omdb_response.text

		# 	cache_file = open(omdb_cached_data, 'w')
		# 	cache_file.write(json.dumps(omdb_cache_diction))
		# 	cache_file.close
		# return json.loads(omdb_response_text)


def requestURL(base_url, params = {}):
	r = requests.Request(method = 'GET', url = base_url, params = params)
	prep = r.prepare()
	return prep.url




# Write your test cases here.
class CacheTesting(unittest.TestCase):
	def test_movie_cache(self):
		cache_file = open("SI206_FinalProject_cache.json","r").read()
		self.assertTrue("Movies" in cache_file)
	def test_twitter_cache(self):
		cache_file = open("SI206_FinalProject_cache.json","r").read()
		self.assertTrue("Tweets" in cache_file)
class MovieTesting(unittest.TestCase):
	def test_Movie_str_method(self):
		movie_instance = Movie(movie_dic)
		self.assertEqual(type(movie_instance.__str__(), str))
	def test_get_actors_method(self):
		movie_instance = Movie(movie_instance)
		self.assertEqual(type(movie_instance.get_movie_actors()), list))
	def test_get_actors_method2(self):
		movie_instance = Movie(movie_instance)
		actors = movie_instance.get_movie_actors()[0]
		self.assertEqual(type(actors), list))
	def test_title_of_movie(self):
		movie_instance = Movie(movie_instance)
		self.assertEqual(type(movie_instance.tittle), str)
	def test_movie_tweets(self):
 		self.assertEqual(type(movie_tweets),type([]))
 	def test_actor(self):
 		self.assertEqual(type(get_movie_actors[18]),type({"hi":3}))




## Remember to invoke all your tests...
if __name__ == "__main__":
	unittest.main(verbosity=2)