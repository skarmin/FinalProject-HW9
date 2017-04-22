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


#GET MOVIE DATA
def requestURL(base_url, params = {}):    #PREP FOR REQUESTING DATA
	response = requests.Request(method = 'GET', url = base_url, params = params)
	prep = response.prepare()
	return prep.url
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
	# print (movie_dict)
	# print (type(movie_dict))
	return movie_dict
#CREATE MOVIE CLASS
class Movie():
	def __init__(self, tweet, movie_dict):
		self.movie_title = movie_dict["Title"]
		self.movie_director = movie_dict["Director"]
		self.movie_IMBD_rating = movie_dict["Ratings"][0]["Value"]
		self.movie_release_date = movie_dict["Released"]
		self.movie_plot = movie_dict["Plot"]
	def __str__(self):
		return "{} is directed by {} and received a an IMBD rating of {}".format(self.movie.title, self.movie_director, self.movie_IMBD)

	def get_actors(movie_dict):
		actors = movie_dict["Actors"]
		return actors
	
	def get_twitter_info(actors):				
		actors = actors.split(", ")
		for actor in actors:
			if actor in CACHE_DICTION:
				print("Using Cached Data...")
				tweets = CACHE_DICTION[actor]
				# print(actor)
				# print(tweets)
			else:
				print("Finding Data online...")
				tweets = api.search(q=str(actor))
				CACHE_DICTION[actor] = tweets
				
				f = open(CACHE_FNAME, 'w')
				f.write(json.dumps(CACHE_DICTION))
				f.close()
		tweets = tweets['statuses']
		return tweets

	def get_movie_table(movie_dict):
		actors = movie_dict["Actors"]
		actors = actors.split(",")
		MovieInfoTuple = (movie_dict['imdbID'], movie_dict['Title'], movie_dict["Director"], movie_dict["imdbRating"], len(movie_dict["Language"].split()), movie_dict["BoxOffice"], actors[0])	
		return MovieInfoTuple
	
	def get_user_table(tweets, movie_dict):
		user_lst = []
		for tweet in twitter:
			t2 = (tweet['user']['id_str'], tweet['user']['screen_name'], tweet['user']['favourites_count'])
			user_lst.append(t2)
		return user_lst 		

#CALLING!!!!!!!
movie_list = ["Frozen", "The Wolf of Wall Street", "Friends With Benefits"] #WHEN ADD USER INPUT, ADD TRY AND EXCEPT IN CASE MOVIE ISN'T FOUND
tuple_movie_lst = []
tweet_list = []
users = []
for movie in movie_list:
	movie_dict = get_movie_info(movie)
	ActorsOfMovie = Movie.get_actors(movie_dict)
	twitter = Movie.get_twitter_info(ActorsOfMovie)
	#Twitter = a list of dictionareis, each dictionary consisting of one tweet info
	movie_table = Movie.get_movie_table(movie_dict)
	user_table = Movie.get_user_table(twitter, movie_dict)
	
	tuple_movie_lst.append(movie_table)
	tweet_list.append(twitter)
	users.append(user_table)

#CREATE TABLE FILE
conn = sqlite3.connect('FinalProjectData.db', timeout=3)
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

#UserTable
table_spec = 'CREATE TABLE IF NOT EXISTS '
table_spec += 'User (user_id TEXT PRIMARY KEY, '
table_spec += 'screen_name TEXT, user_favorites INTEGER)'
cur.execute(table_spec)

#To input data
statement = 'INSERT OR IGNORE INTO Movies VALUES (?, ?, ?, ?, ?, ?, ?)'
statement1 = 'INSERT OR IGNORE INTO Tweets VALUES (?, ?, ?, ?)'
statement2 = 'INSERT OR IGNORE INTO User VALUES (?, ?, ?)'


for movie in tuple_movie_lst: #Movie
	# print(movie)
	cur.execute(statement, movie)

for tweet in tweet_list: #TWITTER
	print(tweet[0])
	for x in tweet:
		# print(x)
		t = (x['user']['id_str'], x['text'],x['user']['id_str'],x['retweet_count'])
		cur.execute(statement1,t)

for user in users: #User
	for x in user:
		cur.execute(statement2, x)

conn.commit()
#QUERY SECTION

#Get most popular tweets about a given actor by getting tweets with over 30 Retweets. Store in variable: pop_tweets
	#POSSIBLY ADD IN THE ACTORS NAME!!
statement = 'SELECT * FROM Tweets WHERE retweets > 30'
result = cur.execute(statement)
pop_tweets = []
for x in result.fetchall():
	pop_tweets.append(x)
# print(pop_tweets)

#Get most popualr tweeter (Join Query) by getting tweets with more than 25 retweets and favorites. Store in variable: pop_twitter_user
statement = 'SELECT screen_name, user_favorites FROM User INNER JOIN Tweets ON Tweets.tweet_id=User.user_id WHERE Tweets.retweets >20 and User.user_favorites >20'
result = cur.execute(statement)
pop_twitter_user = []
for x in result.fetchall():
	pop_twitter_user.append(x)
print(pop_tweets)


#Get info about movie outcome to declare the most succesful film. Store in variable: most_succesful_movie
statement = 'SELECT title, rating, box_office_num FROM Movies'
result = cur.execute(statement)
most_succesful_movies = []
for x in result.fetchall():
	most_succesful_movies.append(x)
print(most_succesful_movies)

#Closed Database
conn.close()
#Write your test cases hereself.                                            FIX TEST CASES
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
# 		self.assertEqual(type(movie_instance.get_movie_actors()), list)
# 	def test_get_actors_method2(self):
# 		movie_instance = Movie(movie_instance)
# 		actors = movie_instance.get_movie_actors()[0]
# 		self.assertEqual(type(actors), list)
# 	def test_title_of_movie(self):
# 		movie_instance = Movie(movie_instance)
# 		self.assertEqual(type(movie_instance.tittle), str)
# 	def test_movie_tweets(self):
#  		self.assertEqual(type(movie_tweets),type([]))
# 	def test_actor(self):
#  		self.assertEqual(type(get_movie_actors[18]),type({"hi":3}))




# Remember to invoke all your tests...
if __name__ == "__main__":
	unittest.main(verbosity=2)


