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

#Keyword endpoint
@app.route('/twitter/<keyword>', methods=['GET']) #, methods = ['GET']
def tweet_search(keyword):
    #Default max tweets = 10, otherwise it is passed as queryparam 'max'
    MAX_TWEETS = 10 
    searched_tweets = [status for status in tweepy.Cursor(api.search, q=keyword).items(MAX_TWEETS)]
    return ' ***** '.join([status.text for status in searched_tweets])


@app.route('/wikipedia/<keyword>', methods=['GET'])
def wikipedia_search(keyword):
    summary = wikipedia.summary(wikipedia.search(keyword)[0])
    return summary

@app.route('/spotify/artist/<keyword>', methods=['GET'])
def spotify_search_artist(keyword):
    results = spotify.search(q='artist:'+keyword, type = 'artist')
    artist_id = results['artists']['items'][0]['id']
    return artist_id

@app.route('/spotify/song/<keyword>', methods=['GET'])
def spotify_search_song(keyword):
    results = spotify.search(q='track:'+keyword, type = 'track')
    artist_id = results['tracks']['items'][0]['artists'][0]['id']
    return artist_id

@app.route('/spotify/playlist/<artist_id>', methods = ['GET'])
def spotify_search_playlist(artist_id):
    results = spotify.artist_top_tracks('spotify:artist:' + artist_id)
    artist_id = results['tracks']['items'][0]['artists'][0]['id']
    return artist_id


if __name__ == '__main__':
    app.run(debug=True)