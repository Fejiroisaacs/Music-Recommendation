import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

all_data = pd.read_csv("data/song_info_final.csv")

dataFrame = all_data[["artist_name", "song_name"]]

print(dataFrame.shape[0])

new_l = []
for _ in range(5):
    new_l.append({"audio": st.audio('https://p.scdn.co/mp3-preview/0062178836f645d0c1ab0a84447cddd1022aec15?cid=09f53c0a70fc4818ab7438fb2dff64dd')})


print(type(dataFrame))
dataFrame = pd.concat([dataFrame, pd.DataFrame(new_l)], axis=1)

#print(new_l)
dq = dataFrame.iloc[:20, :]
print(dq, "vsjbkjdnvkljnsdak")
st.dataframe(dataFrame.iloc[:20, ::])

st.image("https://i.scdn.co/image/ab67616d0000b2731a0affe36002256fac950cdb", width=300)
st.audio('https://p.scdn.co/mp3-preview/0062178836f645d0c1ab0a84447cddd1022aec15?cid=09f53c0a70fc4818ab7438fb2dff64dd')
st.data_editor(np.array([
    ["st.text_area", "widget", 4.92],
    ["st.markdown", "element", 47.22]
]))

