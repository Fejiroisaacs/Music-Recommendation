import streamlit as st
import pandas as pd
import numpy as np
import music_rec as mr
import random

st.set_page_config(layout="wide")

# Define the navigation bar function
def navigation_bar():
    st.sidebar.markdown("# Navigation")
    if st.sidebar.button("Home"):
        st.session_state.page = "Home"
        #st.experimental_rerun()

# Define functions for each page
def home_page():
    navigation_bar() # Include the navigation bar on the home page
    st.title("Music Recommendation Website")
    st.write("Welcome to the home page!")

# Add buttons for navigation
if st.button("Explore Page"):
    st.session_state.page = "Explore"
    st.experimental_rerun()

if st.button("Playlist Page"):
    st.session_state.page = "Playlist"
    st.experimental_rerun()



def explore_page():
    navigation_bar() # Include the navigation bar on the explore page
    st.title("Explore Page")
    st.write("This is the explore page.")
# Add your explore logic here

# Define the playlist page function
def playlist_page():
    navigation_bar()  # Include the navigation bar on the playlist page
    st.title("Playlist")

    # Input field for entering playlist ID
    playlist_id = st.text_input("Enter your playlist ID", value="", key="playlist_input")

    # Save the playlist ID when the user clicks the submit button
    if st.button("Choose my tunes!"):
        st.session_state.playlist_id = playlist_id
    
        # Add your playlist logic here
        st.write(f"Current Playlist ID: {st.session_state.playlist_id}")

        # Get the playlist ID from the session state
        df = mr.get(playlist_id)
        df[0].to_csv("data/recommended.csv", index=False)
        df[1].to_csv("data/recommended_no_preview.csv", index=False)
        
        st.session_state.page = "Recommendation"
        st.experimental_rerun()
                    

def recommendation_page(currently_playing_index):
    # navigation_bar()  # Include the navigation bar on the recommendation page
    # st.session_state.page = "Recommendation"
    
    st.cache()
    df = pd.read_csv("data/recommended.csv")
    st.session_state.currently_playing_track = st.empty()
    st.session_state.currently_playing_track = dict(df.iloc[currently_playing_index])

    # Create a placeholder for "Currently Playing" content
    
    # st.session_state.currently_playing_song = st.empty()
    # st.session_state.currently_playing_artist = st.empty()
    # st.session_state.currently_playing_image = st.empty()
    # st.session_state.currently_playing_audio = st.empty()

    # Display currently playing song details to the right of the image
    # st.session_state.col1, st.session_state.col2 = st.empty(), st.empty()
    # st.session_state.col1, st.session_state.col2 = st.columns([1, 2])

    # # Display the image in the first column
    # st.session_state.col1.image(st.session_state.currently_playing_track["track_img"], width=300)

    # # Display the song name and artist name in the second column
    # st.session_state.col2.markdown(f"<h1 style='font-weight: bold;'>{st.session_state.currently_playing_track['song_name']}</h1>", unsafe_allow_html=True)
    # st.session_state.col2.markdown(f"<h2 style='font-size: larger;'>{st.session_state.currently_playing_track['artist']}</h2>", unsafe_allow_html=True)

    # # Add a spacer for better separation
    # st.session_state.col2.write("")  # You can adjust the number of empty lines for better spacing

    # # Display the audio player
    # st.session_state.col2.audio(st.session_state.currently_playing_track["track_preview"], format="audio/mp3")




    # Create a section for "Up Next"
    st.title("Chosen Tunes")
    # Display the list of songs in "Up Next"
    for i in range(df.shape[0]):
        if i != currently_playing_index:  # Exclude the currently playing song
            track = dict(df.iloc[i])

            # Button to move the song to "Currently Playing" when clicked
           
            if st.button(f"{track['song_name']} - {track['artist']}\n\n", key=i):
                
                st.session_state.current_song = i
                
                currently_playing_index = i
                
                st.session_state.currently_playing_track = dict(df.iloc[currently_playing_index])
                st.session_state.col1, st.session_state.col2 = st.columns([1, 2])

                # Display the image in the first column
                st.session_state.col1.image(st.session_state.currently_playing_track["track_img"], width=300)

                # Display the song name and artist name in the second column
                st.session_state.col2.markdown(f"<h1 style='font-weight: bold;'>{st.session_state.currently_playing_track['song_name']}</h1>", unsafe_allow_html=True)
                st.session_state.col2.markdown(f"<h2 style='font-size: larger;'>{st.session_state.currently_playing_track['artist']}</h2>", unsafe_allow_html=True)

                # Add a spacer for better separation
                st.session_state.col2.write("")  # You can adjust the number of empty lines for better spacing

                # Display the audio player
                st.session_state.col2.audio(st.session_state.currently_playing_track["track_preview"], format="audio/mp3")

                    
                
                
   
# Define the main function
def main():
    # Initialize session state
    st.session_state.current_song = 0
    if "page" not in st.session_state:
        st.session_state.page = "Home"

    # Display the current page based on the session state
    if st.session_state.page == "Home":
        home_page()
    elif st.session_state.page == "Explore":
        explore_page()
    elif st.session_state.page == "Playlist":
        playlist_page()
    elif st.session_state.page == "Recommendation":
        recommendation_page(st.session_state.current_song)

# Run the app
if __name__ == "__main__":
    main()

