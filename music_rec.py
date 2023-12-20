import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
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
    
    
def get(playlist_id):
    
    sp = get_SP("09f53c0a70fc4818ab7438fb2dff64dd", "fcfcaea7cc9a42f697da7ce6d4680d3d", "Fejiro Anigboro")
    sp1 = get_SP("922db1c93c90406fb8608e2729577cf4", "8561aa0a985f470f91193d912a494287", "my_spotify_name")
    sp2 = get_SP("79724bfb388b451e9d80af9972ed118f", "4c1784725f7a468aa97127ee54d63209", "rami")
    sp3 = get_SP("d7e20fdf6b044b8c83c6ef74045bd89d", "bb863640b3844f3a84289182ce5a7c01", "Idan")
    sp4 = get_SP("6ca97a1822a849458f3c105d5f83e3c2", "bb57f33f51da4321b14e0f5309abf7ca", "my_spotify_F2")
    all_sps = [sp1, sp2, sp3, sp4]
    
    
    return fn.userInput(playlist_id, sp, all_sps)
    


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