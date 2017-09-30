# coding=utf-8
## SI 507 F17 Project 2 - Objects
import requests
import json
import unittest

## Instructions for each piece to be completed for this project can be found in the file, below.

## To see whether your problem solutions are passing the tests, you should run the Python file:
# si507f17_project2_objects_tests.py, which should be saved in the same directory as this file.

## (DO NOT change the name of this file! Make sure to re-save it with the name si507f17_project2_objects_code.py if you change the name. Otherwise, we will not be able to grade it!)


print("\n*** *** PROJECT 2 *** ***\n")

## Useful additional references for this part of the homework from outside class material:
## - the iTunes Search API documentation:
## - the following chapters from the textbook (also referred to in SI 506): https://www.programsinformationpeople.org/runestone/static/publicpy3/Classes/ThinkingAboutClasses.html, https://www.programsinformationpeople.org/runestone/static/publicpy3/Classes/ClassesHoldingData.html, https://www.programsinformationpeople.org/runestone/static/publicpy3/UsingRESTAPIs/cachingResponses.html
## - and possibly other chapters, as a reference!

## The first problem to complete for this project can be found below.


#########


## You can search for a variety of different types of media with the iTunes Search API: songs, movies, ebooks and audiobooks... (and more) You'll definitely need to check out the documentation to understand/recall how the parameters of this API work: https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/

## Here, we've provided functions to get and cache data from the iTunes Search API, but looking at the information in that documentation will help you understand what is happening when the second function below gets invoked.
## Make sure you understand what the function does, how it works, and how you could invoke it to get data from iTunes Search about e.g. just songs corresponding to a certain search term, just movies, or just books.
## Refer to the textbook sections about caching, linked above, to help understand these functions!

## You may want to try them out and see what data gets returned, in order to complete the problems in this project.

def params_unique_combination(baseurl, params_d, private_keys=["api_key"]):
    alphabetized_keys = sorted(params_d.keys())
    res = []
    for k in alphabetized_keys:
        if k not in private_keys:
            res.append("{}-{}".format(k, params_d[k]))
    return baseurl + "_".join(res)

def sample_get_cache_itunes_data(search_term,media_term="all"):
	CACHE_FNAME = 'cache_file_name.json'
	try:
	    cache_file = open(CACHE_FNAME, 'r')
	    cache_contents = cache_file.read()
	    CACHE_DICTION = json.loads(cache_contents)
	    cache_file.close()
	except:
	    CACHE_DICTION = {}
	baseurl = "https://itunes.apple.com/search"
	params = {}
	params["media"] = media_term
	params["term"] = search_term
	unique_ident = params_unique_combination(baseurl, params)
	if unique_ident in CACHE_DICTION:
		return CACHE_DICTION[unique_ident]
	else:
		CACHE_DICTION[unique_ident] = json.loads(requests.get(baseurl, params=params).text)
		full_text = json.dumps(CACHE_DICTION)
		cache_file_ref = open(CACHE_FNAME,"w")
		cache_file_ref.write(full_text)
		cache_file_ref.close()
		return CACHE_DICTION[unique_ident]


## [PROBLEM 1] [250 POINTS]
print("\n***** PROBLEM 1 *****\n")


## For problem 1, you should define a class Media, representing ANY piece of media you can find on iTunes search.


## The Media class should accept one dictionary data structure representing a piece of media from iTunes as input to the constructor.
## Its constructor should invoke a method to get and cache data, and instatiate at least the following instance variables:
## - title
## - author
## - itunes_URL
## - itunes_id (e.g. the value of the track ID, whatever the track is in the data... a movie, a song, etc)

## The Media class should also have the following methods:
## - a special string method, that returns a string of the form 'TITLE by AUTHOR'
## - a special representation method, which returns "ITUNES MEDIA: <itunes id>" with the iTunes id number for the piece of media (e.g. the track) only in place of "<itunes id>"
## - a special len method, which, for the Media class, returns 0 no matter what. (The length of an audiobook might mean something different from the length of a song, depending on how you want to define them!)
## - a special contains method (for the in operator) which takes one additional input, as all contains methods must, which should always be a string, and checks to see if the string input to this contains method is INSIDE the string representing the title of this piece of media (the title instance variable)

class Media:
    def __init__(self, diction_file):
        self.title = diction_file['trackName']
        self.author = diction_file['artistName']
        self.itunes_URL = diction_file['trackViewUrl']
        self.itunes_id = diction_file['trackId']

    def __str__(self):
        return '{} by {}'.format(self.title, self.author)

    def __repr__(self):
        return 'ITUNES MEDIA: {}'.format(self.itunes_id)

    def __len__(self):
        return 0

    def __contains__(self, s):
        return x in self.title



## [PROBLEM 2] [400 POINTS]
print("\n***** PROBLEM 2 *****\n")
## In 2 parts.

## Now, you'll define 2 more different classes, each of which *inherit from* class Media:
## class Song
## class Movie

## In the class definitions, you can assume a programmer would pass to each class's constructor only a dictionary that represented the correct media type (song, movie, audiobook/ebook).

## Below follows a description of how each of these should be different from the Media parent class.

### class Song:

class Song(Media):
    def __init__(self, diction_file):
        Media.__init__(self, diction_file)
        self.album = diction_file['collectionName']
        self.track_number = diction_file['trackNumber']
        self.genre = diction_file['primaryGenreName']
        try:
			self.track_time = diction_file['trackTimeMillis']
		except:
			self.track_time = 0

    def __len__(self):
        return int(self.track_time / 1000)

## Should have the following additional instance variables:
## - album (the album title)
## - track_number (the number representing its track number on the album)
## - genre (the primary genre name from the data iTunes gives you)

## Should have the len method overridden to return the number of seconds in the song. (HINT: The data supplies number of milliseconds in the song... How can you access that data and convert it to seconds?)



### class Movie:

class Movie(Media):
    def __init__(self, diction_file):
        Media.__init__(self, diction)
        self.rating = diction_file['contentAdvisoryRating']
        self.genre = diction_file['primaryGenreName']
        try:
			self.track_time = diction_file['trackTimeMillis']
		except:
			self.track_time = 0

		try:
			self.description = diction_file['longDescription']
		except:
			self.description = None

	def __len__(self):
		return self.track_time/1000

	def title_words_num(self):
		if self.description != None:
			return len(self.description.split())
		else:
			return 0


## Should have the following additional instance variables:
## - rating (the content advisory rating, from the data)
## - genre
## - description (if none, the value of this instance variable should be None) -- NOTE that this might cause some string encoding problems for you to debug!
## HINT: Check out the Unicode sub-section of the textbook! This is a common type of Python debugging you'll encounter with real data... but using the right small amount of code to fix it will solve all your problems.

## Should have the len method overridden to return the number of minutes in the movie (HINT: The data returns the number of milliseconds in the movie... how can you convert that to minutes?)

## Should have an additional method called title_words_num that returns an integer representing the number of words in the movie description. If there is no movie description, this method should return 0.



## [PROBLEM 3] [150 POINTS]
print("\n***** PROBLEM 3 *****\n")

## In this problem, you'll write some code to use the definitions you've just written.

## First, here we have provided some variables which hold data about media overall, songs, movies, and books.

## NOTE: (The first time you run this file, data will be cached, so the data saved in each variable will be the same each time you run the file, as long as you do not delete your cached data.)

media_samples = sample_get_cache_itunes_data("love")["results"]

song_samples = sample_get_cache_itunes_data("love","music")["results"]

movie_samples = sample_get_cache_itunes_data("love","movie")["results"]


## You may want to do some investigation on these variables to make sure you understand correctly what type of value they hold, what's in each one!

## Use the values in these variables above, and the class definitions you've written, in order to create a list of each media type, including "media" generally.

## You should end up with: a list of Media objects saved in a variable media_list,
## a list of Song objects saved in a variable song_list,
## a list of Movie objects saved in a variable movie_list,
## and a list of Book objects saved in a variable book_list.

## You may use any method of accumulation to make that happen.

media_list = [Media(v) for v in media_samples]
song_list = [Song(v) for v in song_samples]
movie_list = [Movie(v) for v in movie_samples]




## [PROBLEM 4] [200 POINTS]
print("\n***** PROBLEM 4 *****\n")

## Finally, write 3 CSV files:
# - movies.csv
# - songs.csv
# - media.csv

## Each of those CSV files should have 5 columns each:
# - title
# - artist
# - id
# - url (for the itunes url of that thing -- the url to view that track of media on iTunes)
# - length

## There are no provided tests for this problem -- you should check your CSV files to see that they fit this description to see if this problem worked correctly for you. IT IS VERY IMPORTANT THAT YOUR CSV FILES HAVE EXACTLY THOSE NAMES!

## You should use the variables you defined in problem 3, iteration, and thought-out use of accessing elements of a class instance, to complete this!

## HINT: You may want to think about what code could be generalized here, and what couldn't, and write a function or two -- that might make your programming life a little bit easier in the end, even though it will require more thinking at the beginning! But you do not have to do this.

## HINT #2: *** You MAY add other, non-required, methods to the class definitions in order to make this easier, if you prefer to!

## It is perfectly fine to write this code in any way, as long as you rely on instances of the classes you've defined, and the code you write results in 3 correctly formatted CSV files!

## HINT #3: Check out the sections in the textbook on opening and writing files, and the section(s) on CSV files!

## HINT #4: Write or draw out your plan for this before you actually start writing the code! That will make it much easier.

def writeCSV(name, media_list=[]):
    with open('{}.csv'.format(name), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['title', 'artist', 'id', 'url', 'length'])
        for item in media_list:
            writer.writerow([item.title,
                             item.author,
                             item.itunes_id,
                             item.itunes_URL,
                             len(item)])

writeCSV('media', media_list)
writeCSV('song', song_list)
writeCSV('movie', movie_list)
