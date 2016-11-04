from flask import Flask, request, jsonify
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

@app.route('/api/v1/search/<keyword>', methods=['GET'])
def keyword_search(keyword):
    """
    Searches the <keyword> at the spotify endpoint.

    Gets the artists' top 10 tracks for the playlist.

    Gets an artist and queries  the wikipedia and twitter endpoints to get a
    summary and tweets.  

    Returns all the info in a json dictionary.
    """
    try:
        #Search artists, if nothing is found, then search for the song
        artist = spotify_search_artist(keyword)
    except (IndexError):
        artist = spotify_search_song(keyword)

    artist_id = artist['id']
    artist_name = artist['name']
    playlist = spotify_search_playlist(artist_id)
    summary = wikipedia_search(artist_name)
    tweets = tweet_search(artist_name)

    data = {'artist_name':artist_name,'summary':summary,
    'tweets':tweets, 'playlist':playlist}

    return jsonify(results=data)

@app.route('/api/v1/twitter/<keyword>', methods=['GET'])
def tweet_search(keyword):
    """
    Searches twitter for tweets with the keyword.

    Returns a list of strings, each string being the text of one of the
    tweets.  Returns a maximum of 5 tweets.
    """
    MAX_TWEETS = 5
    searched_tweets = [status for status in tweepy.Cursor(api.search, q=keyword).items(MAX_TWEETS)]
    tweet_texts = [status.text for status in searched_tweets]
    return tweet_texts


@app.route('/api/v1/wikipedia/<keyword>', methods=['GET'])
def wikipedia_search(keyword):
    """
    Returns the summary of the first result from wikipedia from the query <keyword>/
    """
    summary = wikipedia.summary(wikipedia.search(keyword)[0])
    return summary

@app.route('/api/v1/spotify/artist/<keyword>', methods=['GET'])
def spotify_search_artist(keyword):
    """
    Queries spotify for an artist.

    Returns a dictionary containing the name and spotify id of the artist.
    """
    results = spotify.search(q='artist:'+keyword, type = 'artist')
    artist_id = results['artists']['items'][0]['id']
    artist_name = results['artists']['items'][0]['name']
    artist = {'name':artist_name, 'id':artist_id}
    return artist

@app.route('/api/v1/spotify/song/<keyword>', methods=['GET'])
def spotify_search_song(keyword):
    """
    Queries spotify for a song, and gets the artist of that song.

    Returns a dictionary containing the name and spotify id of the artist.
    """
    results = spotify.search(q='track:'+keyword, type = 'track')
    artist_id = results['tracks']['items'][0]['artists'][0]['id']
    artist_name = results['tracks']['items'][0]['artists'][0]['name']
    artist = {'name':artist_name, 'id':artist_id}
    return artist

@app.route('/api/v1/spotify/playlist/<artist_id>', methods = ['GET'])
def spotify_search_playlist(artist_id):
    """
    Searches spotify for the provided artist_id.

    Returns the title of the top 10 tracks of the artist in a list. 
    """
    results = spotify.artist_top_tracks('spotify:artist:' + artist_id)
    songs = [results['tracks'][i]['name'] for i in xrange(min(10,len(results['tracks'])))]
    return songs


if __name__ == '__main__':
    app.run(debug=True)