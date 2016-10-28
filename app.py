from flask import Flask, request
import app
import tweepy
import json
import urllib2
import wikipedia
import spotipy


app = Flask(__name__)

#Setting up tweepy authorization
auth = tweepy.OAuthHandler('2V53Lal2KelyzphD4wEXU3oht', 'feisD0DTMeG3HZ277R89OI6cmG05CZ158cODqNjYIEV3Vf9m19')
auth.set_access_token('778344887867416576-MDQM4AuLBaHTyAyKqedL9IboTXDopO8', 'zDHetn79XdWdJJMD2Hzg00Rsz9TBbS1q9M2SxsjZHHb7t')

#Instantiate tweepy api
api = tweepy.API(auth)

#Instantiate spotify
spotify = spotipy.Spotify()


# static url
@app.route('/')
def index():
    returnThis = "MusicSearch v 0.0.0.01"
    return returnThis

@app.route('/search/<keyword>', methods=['GET'])
def keyword_search(keyword):
    try:
        artist = spotify_search_artist(keyword)
    except (IndexError):
        artist = spotify_search_song(keyword)

    artist_id = artist['id']
    playlist = spotify_search_playlist(artist_id)

    artist_name = artist['name']
    summary = wikipedia_search(artist_name)
    tweets = tweet_search(artist_name)

    data = {'artist_name':artist_name,'summary':summary,
    'tweets':tweets, 'playlist':playlist}

    return str(data)

@app.route('/twitter/<keyword>', methods=['GET']) #, methods = ['GET']
def tweet_search(keyword):
    MAX_TWEETS = 3
    searched_tweets = [status for status in tweepy.Cursor(api.search, q=keyword).items(MAX_TWEETS)]
    tweet_texts = [status.text for status in searched_tweets]
    return tweet_texts


@app.route('/wikipedia/<keyword>', methods=['GET'])
def wikipedia_search(keyword):
    summary = wikipedia.summary(wikipedia.search(keyword)[0])
    return summary

@app.route('/spotify/artist/<keyword>', methods=['GET'])
def spotify_search_artist(keyword):
    results = spotify.search(q='artist:'+keyword, type = 'artist')
    artist_id = results['artists']['items'][0]['id']
    artist_name = results['artists']['items'][0]['name']
    artist = {'name':artist_name, 'id':artist_id}
    return artist

@app.route('/spotify/song/<keyword>', methods=['GET'])
def spotify_search_song(keyword):
    results = spotify.search(q='track:'+keyword, type = 'track')
    artist_id = results['tracks']['items'][0]['artists'][0]['id']
    artist_name = results['tracks']['items'][0]['artists'][0]['name']
    artist = {'name':artist_name, 'id':artist_id}
    return artist

@app.route('/spotify/playlist/<artist_id>', methods = ['GET'])
def spotify_search_playlist(artist_id):
    results = spotify.artist_top_tracks('spotify:artist:' + artist_id)
    songs = [results['tracks'][i]['name'] for i in xrange(min(10,len(results['tracks'])))]

    return songs


if __name__ == '__main__':
    app.run(debug=True)