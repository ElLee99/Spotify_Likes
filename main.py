import spotipy
import numpy as np
import random
from spotipy.oauth2 import SpotifyOAuth
from secrets import client_id, client_secret, redirect_uri, scope, spotify_username 


#Allows to establish a coonection with the spotify api
class connect_Spotify:
    def __init__(self):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri                  
        self.scope = scope                                              #The scope are the permissions that we ask to the user
        self.username = spotify_username                                #The username from spotify from the user

    #Generates a token with the data from the user and the client(dashboard) 
    #Also creates and returns an object which is the way we request and give data from the api 
    def create_Object(self):
        self.token = SpotifyOAuth(client_id = self.client_id, client_secret =self.client_secret, redirect_uri = self.redirect_uri, scope=self.scope, username=self.username)
        self.spotifyObject  = spotipy.Spotify(auth_manager = self.token)
        return self.spotifyObject

    #Returns the username
    def get_username(self):
        return self.username


#Save all the liked tracks from the user and stores it in a list
class all_Saved_Tracks():
    def __init__ (self, spotify_object):
        print("Guardando tus me gusta...")
        self.tracks=""
        results = spotify_object.current_user_saved_tracks(limit=50, offset=0, market=None)
        temp_tracks = results ['items']
        while (results['next']):
            results = spotify_object.next(results)
            temp_tracks.extend(results['items'])
        for i in temp_tracks :
            self.tracks += (i["track"] ["uri"] + "," )
        self.tracks = self.tracks[:-1]
        self.tracks = list((self.tracks).split(","))

    #Returns all the tracks as a list
    def get_tracks(self):
        return self.tracks


#Creates an empty playlist 
class create_Playlist:
    def __init__(self, spotify_object, name, description, username):
        print("Creando la playlist...")
        self.name = name
        self.description = description
        self.username = username
        self.playlist = spotify_object.user_playlist_create(user = self.username, name = self.name, public = True, description = self.description)
        self.id = self.playlist["id"]

    #Returns an id from the playlist created 
    def get_id(self):
        return self.id


#Add songs to a playlist
class add_Tracks_To_Playlist:
    def __init__(self, spotify_object, id_playlist, tracks, **kwargs):
        print("Añadiendo tus canciones...")      
        length_list = len(tracks)

        if 'random_list' in kwargs.keys():
            random_list = kwargs['random_list']
            if random_list == True:
                random.shuffle(tracks)
            else:
                pass
            
        if  'no_tracks' in kwargs.keys():
            no_tracks = kwargs['no_tracks']

            if length_list > no_tracks:
                tracks = tracks [:no_tracks]
                length_list = no_tracks
            else:
                pass

        if length_list > 100:
            n = 0
            while (length_list - (n * 100) > 100):
                temp_tracks = tracks [n*100:((n+1)*100)]
                spotify_object.playlist_add_items(id_playlist, temp_tracks, position=None)
                n += 1
            if (length_list - (n * 100) > 0):
                temp_tracks = tracks [n*100 : length_list]
                spotify_object.playlist_add_items(id_playlist, temp_tracks, position=None)
        else:
            spotify_object.playlist_add_items(id_playlist, tracks, position=None)



spoti_connection = connect_Spotify()                    #Connect with the spotify API 
spoti_object = spoti_connection.create_Object()         #Create the spotify object
my_username = spoti_connection.get_username()           #Get the username
tracks = all_Saved_Tracks(spoti_object)                 #Save all liked tracks 
my_tracks = all_Saved_Tracks.get_tracks(tracks)         #Get the list with the likes

#Create a playlist for all the likes and get the id 
my_likes = create_Playlist(spoti_object, "Mis likes", "Playlist con mis likes", my_username)
my_likes_playlist = my_likes.get_id()

#Create a playlist for the last 50 likes and get the id 
my_last_50 = create_Playlist(spoti_object, "Mis últimos 50 likes", "Playlist con mis últimos 50 likes", my_username)
my_last_50_playlist = my_last_50.get_id()

#Create a playlist for the last 100 likes and get the id 
my_last_100 = create_Playlist(spoti_object, "Mis últimos 100 likes", "Playlist con mis últimos 100 likes", my_username)
my_last_100_playlist = my_last_100.get_id()

#Add the whole list to the playlist to the first playlist
add_Tracks_To_Playlist (spotify_object = spoti_object, id_playlist= my_likes_playlist, tracks = my_tracks, random_list = False)

#Add the whole last 50 songs to the second playlist
add_Tracks_To_Playlist (spotify_object = spoti_object, id_playlist= my_last_50_playlist, tracks = my_tracks, random_list = False, no_tracks = 50)

#Add the whole last 100 songs to the third playlist
add_Tracks_To_Playlist (spotify_object = spoti_object, id_playlist= my_last_100_playlist, tracks = my_tracks, random_list = False, no_tracks = 100)