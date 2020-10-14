# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 22:37:27 2020

@author: Jane

'Create a playlist with the "Best Melodic Rap Performances" Grammy award-winning songs on Spotify using Spotipy'
"""

import requests
import json
import spotipy
import spotipy.util as util
from bs4 import BeautifulSoup
from user_info import user_id, client_id, client_secret # PERSONAL ACCOUNT INFO

#GET AUTHENTICATION TOKEN
def get_token():
    scope = 'playlist-modify-public'
    token = util.prompt_for_user_token(user_id,scope,client_id=client_id,client_secret=client_secret,redirect_uri='http://localhost:8080/') 
    return spotipy.Spotify(auth=token)
spotify = get_token() 

# CREATE A PLAYLIST
def create_playlist(name, description):
    create = spotify.user_playlist_create(user_id, name, public=True, description= description)
    playlist_id = create['external_urls']['spotify']
    return playlist_id
# USER INPUTS PLAYLIST NAME AND DESCRIPTION
playlist_id = create_playlist("Best Melodic Rap Performances", "My first Spotify Python Project yay!")

# GET PAGE DATA
def get_data ():
    url = 'https://totalmusicawards.com/grammy-awards/best-rap-sung-collaboration-winners-nominees/'
    response = requests.get(url)
    page = response.content
    
    soup = BeautifulSoup(page, 'lxml')
    contents = soup.find('div',attrs={"class":"entry-content"})

    #FIND THE BOLD TEXT AFTER THE STRING, WHICH CORRESPONDS TO THE WINNING TITLES AND RESPECTIVE ARTISTS    
    title = soup.find(string = "Grammy Awards: Best Melodic Rap Performance Winners and Nominees By Year")
    a = []
    for i in range(19):
        title = title.find_next('strong')
        a.append(title.string)

    x = []
    y = []
    for i in range(19):
        x.append(a[i].split(":"))
        y.append(x[i][1].split(","))
    return y               
list = get_data()


# ADD SONGS TO THE PLAYLIST
def add_songs():
    track_uris = []
    for i in range(len(list)):
        # CREATE TWO LISTS: ONE FOR THE ARTIST'S NAMES AND THE OTHER FOR THE SONG TITLES
        artist = list[i][1]
        artist = artist.replace("featuring","")
        artist = artist.replace("&","") 
        track = list[i][0]
        #SEARCH FOR THE TRACKS ON SPOTIFY AND APPEND THEIR URI'S TO A LIST
        track_info = spotify.search(q = 'artist:' + artist + ' track:' + track , type = 'track', limit=1)
        if track_info['tracks']['items']!=[]:
            track_uri = track_info['tracks']['items'][0]["uri"]
            track_uris.append(track_uri)
    #ADD TRACKS TO THE PLAYLIST
    spotify.user_playlist_add_tracks(user_id, playlist_id, tracks = track_uris)
add_songs()




    