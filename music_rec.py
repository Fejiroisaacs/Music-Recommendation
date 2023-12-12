import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.neighbors import NearestNeighbors
import functions as fn


def main():
    
    sp = get_SP("09f53c0a70fc4818ab7438fb2dff64dd", "fcfcaea7cc9a42f697da7ce6d4680d3d", "Fejiro Anigboro")
    sp1 = get_SP("922db1c93c90406fb8608e2729577cf4", "8561aa0a985f470f91193d912a494287", "my_spotify_name")
    sp2 = get_SP("79724bfb388b451e9d80af9972ed118f", "4c1784725f7a468aa97127ee54d63209", "rami")
    sp3 = get_SP("d7e20fdf6b044b8c83c6ef74045bd89d", "bb863640b3844f3a84289182ce5a7c01", "Idan")
    sp4 = get_SP("6ca97a1822a849458f3c105d5f83e3c2", "bb57f33f51da4321b14e0f5309abf7ca", "my_spotify_F2")
    all_sps = [sp1, sp2, sp3, sp4]
    
    
    user = fn.userInput("7mVCbkMcSXApmQ08F9uUi5", sp, all_sps)
    
    print(user[0])
    print(user[1])
    print(user[2])
    
    
    # test_pl = filter_info(sp4, "7mVCbkMcSXApmQ08F9uUi5")
    # gatt = get_artist_top_tracks("4ETSs924pXMzjIeD6E9b4u", sp)
    
    # df = pd.read_csv("data/song_info_final.csv")

    # filtered_df = df[selected_columns]
    
    
    # gat = get_album_tracks(sp, "6P1sBa0T1fRooA0UTAQfOu")

    # print(gat)
    # print(sp.recommendations(seed_tracks = ['0ofbQMrRDsUaVKq2mGLEAb'], limit=5, country="US")['tracks'][0])

    # spr = sp.recommendations(seed_tracks = list(df['id'])[:5], limit=5, country="US")['tracks'][0]
    # print(spr.keys())
    # print(spr['name'])
    # print(spr['id'])
    # print(spr['external_urls']['spotify'])
    # print(spr['album']['images'][0]['url'])

    # filtered_df_matrix = filtered_df[matrix_cols].to_numpy()


    # neigh = NearestNeighbors(n_neighbors=3)
    # neigh.fit(filtered_df_matrix)
    # neigh.kneighbors([[ 6.150e-01,  7.790e-01,  2.000e+00, -6.454e+00,  1.000e+00,
    #         1.350e-01,  6.650e-02,  0.000e+00,  1.550e-01,  4.530e-01,
    #         1.600e+02], [ 6.8700e-01,  8.4500e-01,  7.0000e+00, -4.3700e+00,  1.0000e+00,
    #         5.7600e-02,  1.0000e-01,  0.0000e+00,  4.5200e-02,  8.0900e-01,
    #         8.7972e+01] , [ 6.8700e-01,  8.4500e-01,  7.0000e+00, -4.3700e+00,  1.0000e+00,
    #         5.7600e-02,  1.0000e-01,  0.0000e+00,  4.5200e-02,  8.0900e-01,
    #         8.7972e+01]], return_distance=False)
    


def get_SP(ID, Secret, Name):
    CLIENT_ID = ID
    CLIENT_SECRET = Secret
    my_username = Name

    # instantiating the client.  This 'sp' version of the client is used repeatedly below
    # source: Max Hilsdorf (https://towardsdatascience.com/how-to-create-large-music-datasets-using-spotipy-40e7242cc6a6)
    client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, status_retries=3, backoff_factor=0.3)
    
    return sp


if __name__ == "__main__":
    main()