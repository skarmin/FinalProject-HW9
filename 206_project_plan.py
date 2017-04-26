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
CACHE_FNAME = "SI206_FinalProject_cache.json" #CACHE SYSTYEM
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
		cache_file.close()
	movie_dict = json.loads(omdb_response_text)
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
		self.movie_genre = movie_dict["Genre"]
	def __str__(self):
		return "{} is directed by {} and received a an IMBD rating of {}".format(self.movie_title, self.movie_director, self.movie_IMBD_rating)

	def get_actors(movie_dict):
		actors = movie_dict["Actors"]
		print("yoooo")
		print(type(actors))
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
				
				cache_file = open(CACHE_FNAME, 'w')
				cache_file.write(json.dumps(CACHE_DICTION))
				cache_file.close()
		tweets = tweets['statuses']
		print('TWEEEET')
		print(type(tweets))
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
movie_list = ["Moana", "Frozen", "The Wolf of Wall Street", "Friends With Benefits"] #WHEN ADD USER INPUT, ADD TRY AND EXCEPT IN CASE MOVIE ISN'T FOUND
tuple_movie_lst = []
tweet_list = []
users = []
for movie in movie_list:
	movie_dict = get_movie_info(movie)
	ActorsOfMovie = Movie.get_actors(movie_dict)
	twitter = Movie.get_twitter_info(ActorsOfMovie)
	#Twitter = a list of dictionareis, each dictionary consisting of one tweet info
	movie_table = Movie.get_movie_table(movie_dict)
	print(movie_table)
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

#Creating OUTPUT File
output = open("SI206_Final_Project_Summary.txt", 'w')
output.write("Created by Sam Karmin \n")
output.write("SI206 Final Project Summary Page")
output.write("Explain what this page should summerize!!!!!")


#To input data
statement3 = 'INSERT OR IGNORE INTO Movies VALUES (?, ?, ?, ?, ?, ?, ?)'
statement1 = 'INSERT OR IGNORE INTO Tweets VALUES (?, ?, ?, ?)'
statement2 = 'INSERT OR IGNORE INTO User VALUES (?, ?, ?)'


for movie in tuple_movie_lst: #Movie
	cur.execute(statement3, movie)

for tweet in tweet_list: #TWITTER
	for x in tweet:
		t = (x['user']['id_str'], x['text'],x['user']['id_str'],x['retweet_count'])
		cur.execute(statement1,t)

for user in users: #User
	for x in user:
		cur.execute(statement2, x)

conn.commit()
#QUERY SECTION

#Get most popular tweets about a given actor by getting tweets with over 30 Retweets. Store in variable: pop_tweets
	#POSSIBLY ADD IN THE ACTORS NAME!!
statement = 'SELECT * FROM Tweets WHERE retweets > 15'
result = cur.execute(statement)
pop_tweets = []
for x in result.fetchall():
	pop_tweets.append(x)
sorted_pop_tweets = sorted(pop_tweets, key = lambda x: x[-1])
Most_pop_tweets = sorted_pop_tweets[:3]
print("Most_pop_tweets")
print(Most_pop_tweets)
output.write("After finding, then sorting the most popular tweets generated by searching for the main actors of the three movies, bellow highlights the key information of each Tweet: \n")
for tweet in range(len(Most_pop_tweets)):
	output.write("The text of the Tweet consists of: " +str(Most_pop_tweets[tweet][1])+".\n")
	output.write("This tweet was Retweeted: " +str(Most_pop_tweets[tweet][-1])+"times.\n")
	output.write("If you wish to find more tweets from this user, search the user ID: " + str(Most_pop_tweets[tweet][0])+".\n")

#Get most popualr tweeter (Join Query) by getting tweets with more than 25 retweets and favorites. Store in variable: pop_twitter_user
statement = 'SELECT screen_name, user_favorites FROM User INNER JOIN Tweets ON Tweets.tweet_id=User.user_id WHERE Tweets.retweets >20 and User.user_favorites >20'
result1 = cur.execute(statement)
pop_twitter_user = {result[0]: (result[1]) for result in result1.fetchall()}
lst = []
for key in pop_twitter_user.keys():
	lst.append((key, pop_twitter_user[key]))
pop_twitter_user_SORT = sorted(lst, key = lambda x: x[0], reverse = True)
output.write("Below, consist of the most popular Tweeters (Their User_ID and and how often they are retweeted) who write about the main actors in each movie: This information can be utilized in order to find the most prominent of tweeters so you can get the most followed information:\n")
for k in pop_twitter_user_SORT:
	k = str(k)
	k = k.replace("(", '')
	k = k.replace(")", '')
	k = k.replace("'", '')
	k = k.split(",")
	print(k)

	for x in k:
		ID = k[0]
		num = k[-1]
	output.write("User_ID: " + ID + "\t Number of Retweets: " + str(num)+ "\n")

#Get info about movie outcome to declare the most succesful film. Store in variable: most_succesful_movie
statement = 'SELECT title, rating, box_office_num FROM Movies'
result = cur.execute(statement)
most_succesful_movies = [result for result in result.fetchall()]
sorted_most_succesful_movies = sorted(most_succesful_movies, key = lambda x: x[1], reverse = True)
print(sorted_most_succesful_movies)
output.write("Below are the Movies, their raitng, as well as the profits the movie brought in:\n")

for x in sorted_most_succesful_movies:
	titlerate = x[0:2]
	print ('DICK')
	for l in titlerate:
		name = x[0]
		rating = str(x[1])
	profit = x[2]
	output.write("Title: " + name + "\t Rating: " + rating + "\t Profits: " +profit +"\n")
output.write("After reviewing the data above, the ratings clearly do not reflect the profit that each movie will make \n")
output.write("Evidently, there is very little correlation between the popularity a star actor has on Twitter, and the how well a movie will sell. I believe this is due to the genre of a given move, the audience it is directed toward, and the people who use twitter. In turn, I do not suggest one looks for at the popularity of an actor on Twitter when determining a movie choice.")


#Closed Database
conn.close()



#Write your test cases hereself.                                            FIX TEST CASES
class CacheTesting(unittest.TestCase):
	def test_movie_cache(self):
		fle = "SI206_FinalProject_cache.json"
		cache_file = open(fle, 'r')
		self.assertTrue("Frozen" in cache_file.read())
		cache_file.close()
	def test_twitter_cache(self):
		fle = "SI206_FinalProject_cache.json"
		cache_file = open(fle, 'r')
		self.assertTrue("Josh Gad" in cache_file.read())
		cache_file.close()

class MovieTesting(unittest.TestCase):
	def test_Movie_str_method(self):
		movie_instance = Movie(tweet, movie_dict)
		self.assertEqual(type(movie_instance.__str__()), str)
	
	def test_get_actors_method(self):
		x = get_movie_info(movie_list[0])
		movie_instance = Movie.get_actors(x)
		self.assertEqual(type(movie_instance), str)

	def test_get_actors_method2(self):
		x = get_movie_info(movie_list[0])
		movie_instance = Movie.get_actors(x)
		self.assertTrue(len(movie_instance) >1 )

	def test_title_of_movie(self):
		movie_instance = Movie(tweet, movie_dict)
		self.assertEqual(type(movie_instance.movie_title), str)

	def test_objtype_tweet(self):
		x = get_movie_info(movie_list[0])
		actors = Movie.get_actors(x)
		movie_instance = Movie.get_twitter_info(actors)
		self.assertEqual(type(movie_instance), list)

	def test_movie_table_input(self):
		movie_instance = Movie(tweet, movie_dict)
		self.assertEqual(type(Movie.get_movie_table(movie_dict)), tuple)
	
	def test_movie_table_content(self):
		x = get_movie_info(movie_list[0]) #Returns movie_dict
		movie_instance = Movie.get_movie_table(x)
		self.assertIn("Auli'i Cravalho", movie_instance)
	
	def test_num_tweets(self):
		for movie in movie_list:
			x = get_movie_info(movie) #Returns movie_dict
			actors = Movie.get_actors(x)  
			movie_instance = Movie.get_twitter_info(actors)#Return twitter
			info = Movie.get_user_table(movie_instance,x)
			length = len(info)
			self.assertEqual(length, 15)
	
	def test_user_table_input(self):
		x = get_movie_info(movie_list[0])
		actors = Movie.get_actors(x)  
		movie_instance = Movie.get_twitter_info(actors)#Return twitter

		info = Movie.get_user_table(movie_instance,x)
		self.assertEqual(type(info[0]), tuple)

# Remember to invoke all your tests...
if __name__ == "__main__":
	unittest.main(verbosity=2)
