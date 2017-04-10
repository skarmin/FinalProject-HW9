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