import streamlit as st
import pandas as pd
import numpy as np
import music_rec as mr

st.set_page_config(layout="wide")

# Define the navigation bar function
def navigation_bar():
    st.sidebar.markdown("# Navigation")
    if st.sidebar.button("Home"):
        st.session_state.page = "Home"
        st.experimental_rerun()

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
    navigation_bar() # Include the navigation bar on the playlist page
    st.title("Playlist")
    # Input field for entering playlist ID
    playlist_id = st.text_input("Enter your playlist ID", value="", key="playlist_input")

    # Save the playlist ID when the user clicks the submit button
    if st.button("Choose my tunes!"):
        st.session_state.playlist_id = playlist_id

        # Add your playlist logic here
        st.write(f"Current Playlist ID: {st.session_state.playlist_id}")

        df = mr.get(playlist_id)
        print(df)
    # st.dataframe(df[0])
        st.dataframe(df[1])
        
        for i in range(df[0].shape[0]):
            track = dict(df[0].iloc[i])
            st.write(track["song_name"])
            st.write(track["artist"])
            st.image(track["track_img"], width=300)
            st.audio(track["track_preview"])
    #print(playlist_id)



    # Define the main function
def main():
    # Initialize session state
    if "page" not in st.session_state:
        st.session_state.page = "Home"

    # Display the current page based on the session state
    if st.session_state.page == "Home":
        home_page()
    elif st.session_state.page == "Explore":
        explore_page()
    elif st.session_state.page == "Playlist":
        playlist_page()
#ncg
# Run the app
if __name__ == "__main__":
    main()

