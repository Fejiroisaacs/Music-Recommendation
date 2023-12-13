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

    df = mr.get(playlist_id)[2]
    print(df)
    st.dataframe(df)
    #print(playlist_id)
    # Include the rest of your playlist logic based on the playlist_id variable


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

# Run the app
if __name__ == "__main__":
    main()



# all_data = pd.read_csv("data/song_info_final.csv")

# dataFrame = all_data[["artist_name", "song_name"]]

# print(dataFrame.shape[0])

# new_l = []
# for _ in range(5):
#   new_l.append({"audio": st.audio('https://p.scdn.co/mp3-preview/0062178836f645d0c1ab0a84447cddd1022aec15?cid=09f53c0a70fc4818ab7438fb2dff64dd')})


# print(type(dataFrame))
# dataFrame = pd.concat([dataFrame, pd.DataFrame(new_l)], axis=1)

# #print(new_l)
# dq = dataFrame.iloc[:20, :]
# print(dq, "vsjbkjdnvkljnsdak")
# st.dataframe(dataFrame.iloc[:20, ::])

# st.image("https://i.scdn.co/image/ab67616d0000b2731a0affe36002256fac950cdb", width=300)
# st.audio('https://p.scdn.co/mp3-preview/0062178836f645d0c1ab0a84447cddd1022aec15?cid=09f53c0a70fc4818ab7438fb2dff64dd')
# st.data_editor(np.array([
# ["st.text_area", "widget", 4.92],
# ["st.markdown", "element", 47.22]
# ]))



# song_dict = pd.DataFrame(columns=["song_id", "liked"])

# # button clicked
# song_dict = song_dict.concat({"song_id": id, "liked": True})