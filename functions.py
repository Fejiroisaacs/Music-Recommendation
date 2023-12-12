import pandas as pd
import numpy as np
import random
import altair as alt
import plotly.graph_objects as go
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import networkx as nx
import networkx.algorithms.community as nx_comm
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import plotly.express as px
import pyvis
from pyvis import network as net
from copy import deepcopy
import time
import csv
from sklearn.neighbors import NearestNeighbors



def filter_info(sp, playlist_id, username="Any user"):
    r = sp.user_playlist_tracks(username, playlist_id)
    t = r['items']
    
    info_list = []
      
    while r['next']:
        r = sp.next(r)
        t.extend(r['items'])
    for s in t: 
        album_type = s['track']['album']['album_type'] 
        song_id = s["track"]["id"]
        song_name = s["track"]["name"]
        #print(song_name)
        
        artist_name = s["track"]["artists"][0]["name"]
        #print(artist_name)
        
        # this gives the id of an artist
        artist_id = s["track"]["artists"][0]["id"] # use href if I need to get the full api call for this -- split by "/" thne get [-1] element
        #print(artist_id) 
        
        popularity = s["track"]["popularity"]
        
        #print(s)
        
        try:
            # getting the url of the album
            album_id = s['track']['album']['id']
            #print(album_id) # split by same condiiton above
        except:
            album_id = None
           
        
        info_list.append({"song_name" : song_name, "song_id": song_id, "artist" : artist_name, "artist_id": artist_id, "album_type": album_type, "album_id": album_id, "popularity": popularity})
        
    
    return pd.DataFrame(info_list)


def get_artist_top_tracks(artist_id, sp):
    top_hits = sp.artist_top_tracks(artist_id, country='US')
    info_list = []
    
    for track in top_hits['tracks']:
        song_id = track["id"]
        song_name = track["name"]
        artist_name = track["artists"][0]["name"]
        popularity = track["popularity"]
        cover_img = track['album']['images'][1]['url']
        track_preview = track["preview_url"]
        
        info_list.append({"song_name" : song_name, "song_id" : song_id, "artist" : artist_name, "popularity": popularity, "track_preview": track_preview, "track_img": cover_img})
    
    return pd.DataFrame(info_list)


def csv_writer(info):
    with open('Song_data.csv', 'a', newline='') as file:
        # Step 4: Using csv.writer to write the list to the CSV file
        writer = csv.writer(file)
        writer.writerow(info) # Use writerow for single list


def get_audio_features_slowly(track_info, all_sps): #replace this(sp) -- since using jhub, can leave this for now.
    track_dict_list = []
    tracker = 0
    for track in track_info:
        tracker += 1
        try:
            audio_features_temp = all_sps[tracker%len(all_sps)].audio_features(track)
            track_dict_list.append(audio_features_temp)
        except Exception as e:
            print(e, track)

        print(tracker)
    
    track_info_df = pd.DataFrame()
    
    for track in track_dict_list:
        track_dict_df = pd.DataFrame(track[0], [0])
        track_info_df = pd.concat([track_info_df, track_dict_df], ignore_index=True)
        
    return get_our_recommended_songs(track_info_df)


def get_our_recommended_songs(track_df):
    matrix_cols = [  'danceability',
                     'energy',
                     'key',
                     'loudness',
                     'mode',
                     'speechiness',
                     'acousticness',
                     'instrumentalness',
                     'liveness',
                     'valence',
                     'tempo'
                                         ]
    our_cols = [    'id',
                    'danceability',
                    'energy',
                    'key',
                    'loudness',
                    'mode',
                    'speechiness',
                    'acousticness',
                    'instrumentalness',
                    'liveness',
                    'valence',
                    'tempo'
                                        ]
    
    user_track_df = track_df[our_cols]
    user_track_matrix = user_track_df[matrix_cols].to_numpy()
    user_playlist_avg = np.mean(user_track_matrix, axis=0)
    
    database_tracks = pd.read_csv("data/song_info_final.csv")
    database_matrix = database_tracks[matrix_cols].to_numpy()

    return track_df


def userInput(playlist_id, sp, all_sps):
    playlist_songs = filter_info(sp, playlist_id)
    playlist_songs = playlist_songs.drop_duplicates(subset=['artist_id'])

    top_tracks_artists = []
    
    artist_ids = set(list(playlist_songs["artist_id"]))
    album_ids = set(list(playlist_songs["album_id"]))
    track_ids = set(list(playlist_songs['song_id']))
    
 
    top_hits = pd.DataFrame(columns=["song_name", "song_id", "artist", "popularity"])
    all_album_tracks = pd.DataFrame() 
    
    for artist_id in artist_ids:
        top_tracks_artists.append(pd.DataFrame(get_artist_top_tracks(artist_id, sp)))
    
    for df in top_tracks_artists:
        df.dropna(inplace=True)
        df.sort_values(by='popularity', inplace=True)
        top_hits = pd.concat([top_hits, df.head(2)], ignore_index=True)
        
    top_hits = top_hits.drop_duplicates().sort_values(by='popularity', ignore_index=True)
    
    for album_id in album_ids:
        all_album_tracks = pd.concat([all_album_tracks, get_album_tracks(sp, album_id)], ignore_index=True)
    
    
    all_album_tracks.dropna(inplace=True)
    all_album_tracks = all_album_tracks.drop_duplicates(ignore_index=True)
    
    track_data = get_audio_features_slowly(track_ids, all_sps)
    
    return top_hits, all_album_tracks, track_data


def get_album_tracks(sp, album_id):
    album_info = sp.album(album_id=album_id)
    album_track_info = album_info['tracks']['items']
    track_img = album_info['images'][1]['url']
    album_df = pd.DataFrame(columns=["song_name", "song_id", "track_preview", "track_img"])
    index = 0
    
    for track in album_track_info:
        df = pd.DataFrame({"song_name": track["name"] , "song_id": track["id"], "track_preview": track['preview_url'], "track_img": track_img}, [index])
        album_df = pd.concat([album_df, df], ignore_index=True)
        index += 1
        
    return album_df


