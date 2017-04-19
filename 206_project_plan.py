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

CACHE_FNAME = "206_FinalProject_cache.json" #CACHE SYSTYEM
# Put the rest of your caching setup here:
try: 
	cache_file = open(CACHE_FNAME, 'r')
	cache_contents = cache_file.read()
	CACHE_DICTION = json.loads(cache_contents)
	cache_file.close()

except:
	CACHE_DICTION = {}

def requestURL(base_url, params = {}):    #PREP FOR REQUESTING DATA
	response = requests.Request(method = 'GET', url = base_url, params = params)
	prep = response.prepare()
	return prep.url

#GET MOVIE DATA
def get_movie_info(movie_title): #GET MOVIE DATA
	movie_dict = {}
	base_url = 'http://www.omdbapi.com/'
	full_url = requestURL(base_url, params = {"t": movie_title})
	
	if movie_title in CACHE_DICTION:
		print("Getting data from Cache...")
		omdb_response_text = CACHE_DICTION[movie_title]
	else:
		print("Getting data from internet...")

		omdb_response = requests.get(full_url)  #GETS DATA IN VARIABLE omdb resposne
		CACHE_DICTION[movie_title] = omdb_response.text #puts data into dictionary wiht url as key
		omdb_response_text = omdb_response.text
		cache_file = open(CACHE_FNAME, 'w')
		cache_file.write(json.dumps(CACHE_DICTION))
		cache_file.close
	movie_dict = json.loads(omdb_response_text)
	#print("test")
	return movie_dict

#CREATE MOVIE CLASS
class Movie():
	def __init__(self, movie_dict):
		self.movie_title = movie_dict["Title"]
		self.movie_director = movie_dict["Director"]
		self.movie_IMBD_rating = movie_dict["Ratings"][0]["Value"]
		self.movie_release_date = movie_dict["Released"]
		self.movie_plot = movie_dict["Plot"]

	def __str__(self):
		return "{} is directed by {} and received a an IMBD rating of {}".format(self.movie.title, self.movie_director, self.movie_IMBD)


	def get_actors(movie_dict):
		actors = movie_dict["Actors"]
		print("test")
		return actors
	
	def get_twitter_info(actors):				#Need to Fix CACHE System
		actor_tweets = {}
		# for actor in actors.split(", "):
		# 	print(actor)
		# 	tweets = api.search(q=str(actor))
		# 	actor_tweets[actor] = tweets
		# return actor_tweets

		for actor in actors.split(","):
			if actor in CACHE_DICTION:
				print("Using Cached Data...")
				tweets = CACHE_DICTION[actor]
				return tweets
			else:
				print("Finding Data online...")
				#for actor in actors.split(","):
				#actor = actor.replace(" ", '')
				#print(actor)
				tweets = api.search(q=str(actor))
				CACHE_DICTION[actor] = tweets
				print(tweets)
				f = open(CACHE_FNAME, 'w')
				f.write(json.dumps(CACHE_DICTION))
				f.close()
			return tweets


# CACHE_DICTION[unique_identifier] = twitter_results
# 		f = open(CACHE_FNAME, 'w')
# 		f.write(json.dumps(CACHE_DICTION))
# 		f.close()
# 	tweets = twitter_results['statuses']
# 	return tweets



data = get_movie_info("Pulp Fiction")
actors = Movie.get_actors(data)
twitter = Movie.get_twitter_info(actors)
print (twitter)


#2 of 2 Examples of tables to show proficiency 
conn = sqlite3.connect('FinalProjectData.db')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS FinalProjectData')
#TweetTable
table_spec = 'CREATE TABLE IF NOT EXISTS '
table_spec += 'Tweets (tweet_id TEXT PRIMARY KEY, '
table_spec += 'text TEXT, user_id TEXT, retweets INTEGER)'
cur.execute(table_spec)

#MovieTable
table_spec = 'CREATE TABLE IF NOT EXISTS '
table_spec += 'Movies (movie_id TEXT PRIMARY KEY, '
table_spec += 'title TEXT, director TEXT, rating INTEGER, num_languages INTEGER, box_office_num TEXT, main_actor TEXT)'
cur.execute(table_spec)

#To input data
statement = 'INSERT OR IGNORE INTO Movies VALUES (?, ?, ?, ?, ?, ?)'
statement1 = 'INSERT OR IGNORE INTO Tweets VALUES (?, ?, ?, ?)'


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


