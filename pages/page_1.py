#page_1
import streamlit as st
st.subheader(":red[CHANNEL INFORMATION AVAILABLE IN THE DATABASE]")
conn = st.connection('mysql', type='sql')
df = conn.query('SELECT * from channel;')
df.index += 1
df
st.subheader(":red[VIDEO INFORMATION AVAILABLE IN THE DATABASE]")
conn = st.connection('mysql', type='sql')
dfv = conn.query('SELECT * from video;')
dfv.index += 1
dfv
st.subheader(":red[COMMENT INFORMATION AVAILABLE IN THE DATABASE]")
conn = st.connection('mysql', type='sql')
dfc = conn.query('SELECT * from comment;')
dfc.index += 1
dfc