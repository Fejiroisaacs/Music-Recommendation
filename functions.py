import pandas as pd
import numpy as np
import csv
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
import random


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
        artist_id = s["track"]["artists"][0]["id"] 
        #print(artist_id) 
        
        popularity = s["track"]["popularity"]
        
        #print(s)
        
        try:
            # getting the url of the album
            album_id = s['track']['album']['id']
            #print(album_id) # split by same condiiton above
        except:
            album_id = None
           
        
        info_list.append({"song_name" : song_name, "song_id": song_id, "artist" : artist_name, "artist_id": artist_id,\
            "album_type": album_type, "album_id": album_id, "popularity": popularity})
        
    
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


def get_audio_features_slowly(track_info, all_sps): 
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
        
    return get_our_recommended_songs(track_info_df, all_sps[2])



def get_our_recommended_songs(track_df, sp):
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
    
    database_tracks = pd.read_csv("data/song_info_final.csv")
    database_matrix = database_tracks[matrix_cols].to_numpy()
    
    neigh = NearestNeighbors(n_neighbors=2)
    neigh.fit(database_matrix)
    
    song_indexes = []

    for row in user_track_matrix:
        
        neighbors = neigh.kneighbors([row], return_distance=False)[0]
        for i in neighbors:
            song_indexes.append(int(i))

        similarities = cosine_similarity([row], database_matrix)
        song_indexes.append(np.argmax(similarities))
        
    song_indexes = list(set(song_indexes))
    similiar_songs = database_tracks.iloc[song_indexes]
    
    return get_database_track_preview(similiar_songs[['song_name', 'artist_name', 'id', 'popularity']], sp)


def get_database_track_preview(songs_df, sp):
    track_ids = list(songs_df["id"])
    other_dataFrame = pd.DataFrame(columns=["song_name", "song_id", "artist", "track_preview", "track_img", "popularity"])
    index = 0
    
    for track_id in track_ids:
        track_info = sp.track(track_id)
        preview = track_info['preview_url']
        image = track_info['album']['images'][1]['url']
        track_name = track_info['name']
        song_id = track_info['id']
        artist_name = track_info['album']['artists'][0]['name']
        popularity = track_info['popularity']
        df = pd.DataFrame({"song_name": track_name , "song_id": song_id, "artist": artist_name, "track_preview": preview, \
            "track_img": image,  "popularity": popularity}, [index])
        other_dataFrame = pd.concat([other_dataFrame, df],  ignore_index=True)
        index+=1
    
    other_dataFrame.sort_values(by='popularity', inplace=True, ignore_index=True)
    other_dataFrame.drop('popularity', axis=1, inplace=True)
    
    return other_dataFrame

def userInput(playlist_id, sp, all_sps):
    playlist_songs = filter_info(sp, playlist_id)
    playlist_songs = playlist_songs.drop_duplicates(subset=['artist_id'])

    top_tracks_artists = []
    
    artist_ids = list(playlist_songs["artist_id"])
    album_ids = set(list(playlist_songs["album_id"]))
    track_ids = set(list(playlist_songs['song_id']))
    
 
    top_hits = pd.DataFrame(columns=["song_name", "song_id", "artist", "popularity"])
    all_album_tracks = pd.DataFrame() 
    
    for i in range(len(artist_ids)):
        similar_art = sp.artist_related_artists(artist_ids[i])
        all_artists = []    
        for artist in similar_art['artists']:
            all_artists.append(artist['id'])
        random.shuffle(all_artists)
        artist_ids.extend(all_artists[1:3])
    
    artist_ids = set(artist_ids)
    
    for artist_id in artist_ids:
        top_tracks_artists.append(pd.DataFrame(get_artist_top_tracks(artist_id, sp)))
    
    for df in top_tracks_artists:
        df.dropna(inplace=True)
        df.sort_values(by='popularity', inplace=True)
        top_hits = pd.concat([top_hits, df.head(2)], ignore_index=True)
        
    top_hits = top_hits.drop_duplicates().sort_values(by='popularity', ignore_index=True)
    top_hits = top_hits.drop('popularity', axis=1)
    top_hits = top_hits.sample(frac=0.5).reset_index(drop=True)
    
    for album_id in album_ids:
        album_tracks = get_album_tracks(sp, album_id)
        all_album_tracks = pd.concat([all_album_tracks, \
            album_tracks.sample(n=2) if album_tracks.shape[0] > 2 else album_tracks], ignore_index=True)
    

    all_album_tracks = all_album_tracks.drop_duplicates(ignore_index=True)
    all_album_tracks = all_album_tracks.sample(frac=1).reset_index(drop=True)
    
    track_data = get_audio_features_slowly(track_ids, all_sps)
    
    recommended_songs = pd.concat([track_data, top_hits, all_album_tracks], ignore_index=True)
    r_s_no_preview = recommended_songs.loc[recommended_songs['track_preview'].isnull()]
    recommended_songs.dropna(inplace=True)

    for track in track_ids:
        recommended_songs = recommended_songs.loc[recommended_songs['song_id'] != track]
        r_s_no_preview = r_s_no_preview.loc[r_s_no_preview['song_id'] != track]

    r_s_no_preview.reset_index(inplace=True, drop=True)
    recommended_songs.reset_index(inplace=True, drop=True)
    
    r_s_no_preview.drop_duplicates(subset=['song_name', 'artist'], inplace=True)
    recommended_songs.drop_duplicates(subset=['song_name', 'artist'], inplace=True)
     
    return recommended_songs, r_s_no_preview


def get_album_tracks(sp, album_id):
    album_info = sp.album(album_id=album_id)
    album_track_info = album_info['tracks']['items']
    track_img = album_info['images'][1]['url']
    artist_name = album_info['artists'][0]['name']
    
    album_df = pd.DataFrame(columns=["song_name", "song_id", "artist", "track_preview", "track_img"])
    
    index = 0
    
    for track in album_track_info:
        df = pd.DataFrame({"song_name": track["name"] , "song_id": track["id"], 'artist': artist_name, \
            "track_preview": track['preview_url'], "track_img": track_img}, [index])
        album_df = pd.concat([album_df, df], ignore_index=True)
        index += 1
        
    return album_df


def get_contextual_songs(place, mood):
    
    all_songs = pd.read_csv("data/song_info_final.csv")
    
    if place == None and mood == None:
        print("place and mood is none")
        return all_songs.sample(n=10)
    
    danceability = dict(all_songs["danceability"].describe())
    energy = dict(all_songs["energy"].describe())
    loudness = dict(all_songs["loudness"].describe())
    tempo = dict(all_songs["tempo"].describe())
    liveness = dict(all_songs["liveness"].describe())
    
    all_places = {
        "Library" : {"danceability": [danceability["min"], danceability["max"]],
                     "energy": [energy["min"], energy["50%"]],
                     "loudness": [loudness["25%"], loudness["75%"]],
                     "tempo": [tempo["min"], tempo["max"]],
                     "liveness": [liveness["min"], liveness["max"]]},
        
        "Dorm" : {"danceability": [danceability["min"], danceability["max"]],
                     "energy": [energy["min"], energy["50%"]],
                     "loudness": [loudness["50%"], loudness["max"]],
                     "tempo": [tempo["min"], tempo["max"]],
                     "liveness": [liveness["min"], liveness["max"]]},
        
        "Party" : {"danceability": [danceability["50%"], danceability["max"]],
                     "energy": [energy["50%"], energy["max"]],
                     "loudness": [loudness["50%"], loudness["max"]],
                     "tempo": [tempo["min"], tempo["max"]],
                     "liveness": [liveness["50%"], liveness["max"]]}   
    }
    
    
    if place != None:
        current_place = all_places[place]
        all_songs = all_songs.loc[(all_songs["danceability"] >= current_place["danceability"][0]) & \
            (all_songs["danceability"] <= current_place["danceability"][1])]
        all_songs = all_songs.loc[(all_songs["energy"] >= current_place["energy"][0]) & \
            (all_songs["energy"] <= current_place["energy"][1])]
        all_songs = all_songs.loc[(all_songs["loudness"] >= current_place["loudness"][0]) & \
            (all_songs["loudness"] <= current_place["loudness"][1])]
        all_songs = all_songs.loc[(all_songs["tempo"] >= current_place["tempo"][0]) & \
            (all_songs["tempo"] <= current_place["tempo"][1])]
        all_songs = all_songs.loc[(all_songs["liveness"] >= current_place["liveness"][0]) & \
            (all_songs["liveness"] <= current_place["liveness"][1])]
        
        
    danceability = dict(all_songs["danceability"].describe())
    energy = dict(all_songs["energy"].describe())
    loudness = dict(all_songs["loudness"].describe())
    tempo = dict(all_songs["tempo"].describe())
    liveness = dict(all_songs["liveness"].describe())
    
    all_moods = {
        "Happy" : {"danceability": [danceability["75%"], danceability["max"]],
                     "energy": [energy["50%"], energy["max"]],
                     "loudness": [loudness["50%"], loudness["max"]],
                     "tempo": [tempo["50%"], tempo["max"]]},
        
        "Sad" : {"danceability": [danceability["min"], danceability["max"]],
                     "energy": [energy["min"], energy["25%"]],
                     "loudness": [loudness["min"], loudness["25%"]],
                     "tempo": [tempo["min"], tempo["25%"]],
                     "mode": 0}
    }
        
    if mood != None:
        current_mood = all_moods[mood]
        
        all_songs = all_songs.loc[(all_songs["danceability"] >= current_mood["danceability"][0]) & \
            (all_songs["danceability"] <= current_mood["danceability"][1])]
        all_songs = all_songs.loc[(all_songs["energy"] >= current_mood["energy"][0]) & \
            (all_songs["energy"] <= current_mood["energy"][1])]
        all_songs = all_songs.loc[(all_songs["loudness"] >= current_mood["loudness"][0]) & \
            (all_songs["loudness"] <= current_mood["loudness"][1])]
        all_songs = all_songs.loc[(all_songs["tempo"] >= current_mood["tempo"][0]) & \
            (all_songs["tempo"] <= current_mood["tempo"][1])]
        
        if mood == "Sad":
            all_songs = all_songs.loc[(all_songs["mode"] == current_mood["mode"])]
        
    
    return all_songs.sample(n=10) if all_songs.shape[0] > 10 else all_songs
    
