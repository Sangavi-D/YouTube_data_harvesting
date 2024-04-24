import streamlit as st
import pandas as pd
import numpy as np


conn = st.connection('mysql', type='sql')


st.button("QUERIES", type="primary")
if st.button('Q1 - What are the names of all the videos and their corresponding channels?'):
    df1 = conn.query('''SELECT video_name,channel_name
    FROM channel
    LEFT JOIN video
    ON channel.channel_id = video.channel_id''')
    df1.index += 1
    df1    
        

elif st.button('Q2 - Which channels have most number of videos and how many videos do they have?'):
    df2 = conn.query('''SELECT channel_id,channel_name,channel_video_count
FROM channel
ORDER BY channel_video_count DESC
LIMIT 1''')
    df2.index += 1
    df2   

elif st.button('Q3 - What are the top 10 most viewed videos and their respective channels?'):
    df3 = conn.query('''SELECT video_id,video_name,channel_name
FROM channel
RIGHT JOIN video
ON channel.channel_id = video.channel_id                                  
ORDER BY video_view_count DESC
LIMIT 10 ''')
    df3.index += 1
    df3  

elif st.button('Q4 - How many comments were made on each video and what are their corresponding video names?'):
    df4 = conn.query('''SELECT video_id,video_name,video_comment_count
FROM video ''')
    df4.index += 1
    df4  

elif st.button('Q5 - Which videos have the highest number of likes and what are their corresponding channel names?'):
    df5 = conn.query('''SELECT video_id,video_name,channel_name,video_like_count
FROM video
LEFT JOIN channel
ON video.channel_id = channel.channel_id 
ORDER BY video_like_count DESC
LIMIT 1  ''')
    df5.index += 1
    df5  

elif st.button('Q6 - What are the total number of likes  for each videos and corresponding video names ?'):
    df6 = conn.query('''SELECT video_id,video_name,video_like_count
FROM video  ''')
    df6.index += 1
    df6  

elif st.button('Q7 - What is the total number of views for each channel and what are their corresponding channel names?'):
    df7 = conn.query('''SELECT channel_id,channel_name,channel_view_count
FROM channel ''')
    df7.index += 1
    df7  

elif st.button('Q8 - What are the names of all the channels that have published videos in the year 2022?'):
    df8 = conn.query('''SELECT channel.channel_id,channel_name,video_published_at
FROM channel
LEFT JOIN video
ON channel.channel_id = video.channel_id 
WHERE YEAR(video_published_at) = 2022
GROUP BY channel_name   ''')
    df8.index += 1
    df8  

elif st.button('Q9 - What is the average duration od all the videos in each channel and what are their corresponding channel names?'):
    df9 = conn.query('''SELECT channel.channel_id,channel_name,AVG(video_duration) AS "AVG video duration in sec"
FROM channel
LEFT JOIN video
ON channel.channel_id = video.channel_id 
GROUP BY channel_name   ''')
    df9.index += 1
    df9  

elif st.button('Q10 - Which videos have the highest number of comments and what are their corresponding channel names?'):
    df10 = conn.query('''SELECT channel.channel_id,channel_name,video_name,video_comment_count
FROM channel
LEFT JOIN video
ON channel.channel_id = video.channel_id 
ORDER BY video_comment_count DESC 
LIMIT 1  ''')
    df10.index += 1
    df10     
