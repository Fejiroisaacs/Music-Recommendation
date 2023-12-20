import streamlit as st
import pandas as pd
import music_rec as mr

st.set_page_config(layout="wide")


def navigation_bar():
    st.sidebar.markdown("# Navigation")
    if st.sidebar.button("Home"):
        st.session_state.page = "Home"
        st.experimental_rerun()
    # Add buttons for navigation
    if st.sidebar.button("Explore"):
        st.session_state.page = "Explore"
        st.experimental_rerun()

    if st.sidebar.button("Playlist"):
        st.session_state.page = "Playlist"
        st.experimental_rerun()
    
    if st.sidebar.button("Chosen Tunes"):
        st.session_state.page = "Recommendation"
        st.experimental_rerun()


def home_page():
    navigation_bar() # Include the navigation bar on the home page
    
    
    st.markdown(f"<h1 style='font-weight: bold; color: darkorange; text-align: center'>Welcome to Choosey Tunes!</h1>", unsafe_allow_html=True)
    st.divider()
    col1, col2 = st.columns([1, 1], gap="large")
    col1.write("")
    col1.write("")
    col1.write("")
    col1.write("")
    col1.write("")
    col1.write("")
    
    col1.markdown(f"<h2 style='font-size: larger;'>Choosey Tunes recommends music for you based on your Spotify playlists.</h2>", unsafe_allow_html=True)
    col1.markdown(f"<h2 style='font-size: larger;'>Discover new songs on the <b>Explore page!</b></h2>", unsafe_allow_html=True)
    col1.markdown(f"<h2 style='font-size: larger;'>Import your Spotify playlist and discover new songs.</h2>", unsafe_allow_html=True)
    
    
    col1.write("")
    col1.write("")
    col1.write("")
    
    col1.markdown(f"<p style='font-size: larger;'>To import your playlist, paste in the playlist ID from the URL:</p>", unsafe_allow_html=True)
    col1.image("images/how_to.png", width=500)
    col2.image("images/choosey_tunes.png", width=500, caption='The New Way to Discover Music')   
    
    st.divider() 
    st.write("")


def explore_page():
    navigation_bar() # Include the navigation bar on the explore page
    st.title("Explore Page")
    st.write("This is the explore page.")


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
        

def recommendation_page():
    navigation_bar()  # Include the navigation bar on the recommendation page

    df = pd.read_csv("data/recommended.csv")
    st.session_state.currently_playing_track = st.empty()
    st.session_state.currently_playing_track = dict(df.iloc[st.session_state.current_song])


    # section for "Up Next"
    st.title("Chosen Tunes")
    
    # Display the list of songs in "Up Next"
    for i in range(df.shape[0]):
        
        track = dict(df.iloc[i])
        
        if st.button(f"{track['song_name']} - {track['artist']}\n\n", key=i):
            
            st.session_state.current_song = i
            
            st.session_state.currently_playing_track = dict(df.iloc[st.session_state.current_song])
            st.session_state.col1, st.session_state.col2 = st.columns([1, 2])

            # Display the image in the first column
            st.session_state.col1.image(st.session_state.currently_playing_track["track_img"], width=300)

            # Display the song name and artist name in the second column
            st.session_state.col2.write("") 
            st.session_state.col2.write("") 
            st.session_state.col2.markdown(f"<h1 style='font-weight: bold;'>{st.session_state.currently_playing_track['song_name']}</h1>", unsafe_allow_html=True)
            st.session_state.col2.markdown(f"<h2 style='font-size: larger;'>{st.session_state.currently_playing_track['artist']}</h2>", unsafe_allow_html=True)

            st.session_state.col2.write("") 

            # Display the audio 
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
        recommendation_page()

# Run the app
if __name__ == "__main__":
    main()

