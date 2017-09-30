# coding=utf-8
# SI 507 F17 Project 2 - Objects
import requests
import json
import csv

print("\n*** *** PROJECT 2 *** ***\n")

def params_unique_combination(baseurl, params_d, private_keys=["api_key"]):
    alphabetized_keys = sorted(params_d.keys())
    res = []
    for k in alphabetized_keys:
        if k not in private_keys:
            res.append("{}-{}".format(k, params_d[k]))
    return baseurl + "_".join(res)


def sample_get_cache_itunes_data(search_term, media_term="all"):
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
        CACHE_DICTION[unique_ident] = json.loads(
            requests.get(baseurl, params=params).text)
        full_text = json.dumps(CACHE_DICTION)
        cache_file_ref = open(CACHE_FNAME, "w")
        cache_file_ref.write(full_text)
        cache_file_ref.close()
        return CACHE_DICTION[unique_ident]


# [PROBLEM 1] [250 POINTS]
print("\n***** PROBLEM 1 *****\n")

class Media(object):
    def __init__(self, diction_file):
        self.title = diction_file['trackName']
        self.author = diction_file['artistName']
        self.author = diction_file['artistName']
        self.itunes_URL = diction_file['trackViewUrl']
        self.itunes_id = diction_file['trackId']
        if 'trackTimeMillis' in diction_file:
            self.length = diction_file['trackTimeMillis']
        else:
            self.length = 0

    def __str__(self):
        return '{} by {}'.format(self.title, self.author)

    def __repr__(self):
        return 'ITUNES MEDIA: {}'.format(self.itunes_id)

    def __len__(self):
        return 0

    def __contains__(self, s):
        return x in self.title



# [PROBLEM 2] [400 POINTS]
print("\n***** PROBLEM 2 *****\n")

class Song(Media):
    def __init__(self, diction_file):
        Media.__init__(self, diction_file)
        self.album = diction_file['collectionName']
        self.track_number = diction_file['trackNumber']
        self.genre = diction_file['primaryGenreName']

    def __len__(self):
        return int(self.time_ms / 1000)

class Movie(Media):
    def __init__(self, diction_file):
        Media.__init__(self, diction_file)
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

print("\n***** PROBLEM 3 *****\n")


media_samples = sample_get_cache_itunes_data("love")["results"]
song_samples = sample_get_cache_itunes_data("love", "music")["results"]
movie_samples = sample_get_cache_itunes_data("love", "movie")["results"]

media_list = [Media(x) for x in media_samples]
song_list = [Song(x) for x in song_samples]
movie_list = [Movie(x) for x in movie_samples]




print("\n***** PROBLEM 4 *****\n")

with open('movies.csv', 'w', newline = '') as movies_csv:
    movie_writter = csv.writer(movies_csv, delimiter=',')
    movie_writter.writerow(["Title", "Artist", "ID", "URL", "Length"])
    for movie in movie_list:
        movie_writter.writerow([movie.title, movie.author, movie.itunes_id, movie.itunes_URL, movie.length])
movies_csv.close()

with open('songs.csv', 'w', newline = '') as songs_csv:
    song_writter = csv.writer(songs_csv, delimiter=',')
    song_writter.writerow(["Title", "Artist", "ID", "URL", "Length"])
    for song in song_list:
        song_writter.writerow([song.title, song.author, song.itunes_id, song.itunes_URL, song.length])
songs_csv.close()

with open('media.csv', 'w', newline = '') as media_csv:
    media_writter = csv.writer(media_csv, delimiter=',')
    media_writter.writerow(["Title", "Artist", "ID", "URL", "Length"])
    for media in media_list:
        media_writter.writerow([media.title, media.author, media.itunes_id, media.itunes_URL, media.length])
media_csv.close()
