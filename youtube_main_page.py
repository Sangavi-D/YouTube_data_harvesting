#Importing necessary libraries
import googleapiclient.discovery
import pandas as pd
import re
import mysql.connector
from mysql.connector import Error 
from sqlalchemy import create_engine
import streamlit as st

# MySQL Connection
user = "user_name"
password = "your_password"
host = "host_name"  # Or the actual IP address of your MySQL server
database = "your_database_name"

connection_url = f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"
engine = create_engine(connection_url)

# YouTube API Connection
api_service_name = "youtube"
api_version = "v3"
api_key = "your api key" #Insert your own api key
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)

# Streamlit UI
st.title("YOUTUBE DATA HARVESTING AND WAREHOUSING USING SQL AND STREAMLIT")
st.page_link("youtube_main_page.py", label="Home", icon="🏠")
st.page_link("pages/page_1.py", label="Channel Info available ", icon="1️⃣")
st.page_link("pages/page_2.py", label="Queries", icon="2️⃣", disabled=True)
channel_id = st.text_input("Enter Channel ID:")


if st.button("Submit"):
    if channel_id:
        st.success("Channel ID stored!")
        st.experimental_rerun() 
    else:
        st.warning("Please enter a channel ID.")

# Function to get channel data
def get_channel_data(channel_id, youtube):
    try:
        request = youtube.channels().list(id=channel_id, part="snippet,contentDetails,statistics")
        response = request.execute()
        
        if 'items' in response and response['items']:
            channel_data = {
                "channel_id": channel_id,
                "channel_name": response['items'][0]['snippet']['title'],
                "channel_description": response['items'][0]['snippet']['description'],
                "channel_published_at": response['items'][0]['snippet']['publishedAt'],
                "channel_playlist_id": response['items'][0]['contentDetails'].get('relatedPlaylists', {}).get('uploads'),
                "channel_view_count": response['items'][0]['statistics']['viewCount'],
                "channel_subscriber_count": response['items'][0]['statistics']['subscriberCount'],
                "channel_video_count": response['items'][0]['statistics']['videoCount']
            }
            return channel_data
        else:
            # print(f"Skipping channel ID {channel_id} due to missing data.")
            return None
    except Exception as e:
        # print(f"Error retrieving data for channel ID {channel_id}: {e}")
        return None

# Function to insert channel data
def insert_channel_data(channel_data, engine):
    try:
        if channel_data:
            channel_df = pd.DataFrame([channel_data])
            channel_df.to_sql(name='channel', con=engine, if_exists='append', index=False)
            print(f"Channel data for ID {channel_data['channel_id']} inserted successfully!")
        else:
            print(f"Skipping channel data insertion due to missing data.")
    except Exception as e:
        print(f"Error inserting channel data for ID {channel_data['channel_id']}: {e}")

#Getting playlist videos
playlist_videos = []
def video_ids(channel_id, youtube):
    try:
        request = youtube.channels().list(id=channel_id, part="snippet,contentDetails,Statistics")
        response = request.execute() 
        if 'items' in response and response['items']:
            playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            
            next_page_token = None
            # playlist_videos = []

            while True:
                request = youtube.playlistItems().list(part="snippet", playlistId=playlist_id, pageToken=next_page_token)
                response = request.execute()
                for item in response['items']:
                    playlist_videos.append(item['snippet']['resourceId']['videoId'])
                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break
                    
            return playlist_videos
        else:
            print(f"No data found for channel ID {channel_id}.")
            return []
    except Exception as e:
        print(f"Error fetching video IDs: {e}")
        return []

              

# Function to get video data
def get_video_data(video_id, channel_id, youtube):
    try:
        request = youtube.videos().list(id=video_id, part="snippet,contentDetails,statistics")
        response = request.execute()

        video_data = {
            "channel_id": channel_id,
            "video_id": video_id,
            "video_name": response['items'][0]['snippet']['title'],
            "video_description": response['items'][0]['snippet']['description'],
            "video_published_at": response['items'][0]['snippet']['publishedAt'],
            "video_thumbnail": response['items'][0]['snippet']['thumbnails']['default']['url'],
            "video_duration": parse_duration(response['items'][0]['contentDetails'].get('duration')),
            "video_caption": response['items'][0]['contentDetails'].get('caption'),
            "video_view_count": response['items'][0]['statistics']['viewCount'],
            "video_like_count": response['items'][0]['statistics']['likeCount'],
            "video_comment_count": response['items'][0]['statistics']['commentCount']
        }
        return video_data
    except Exception as e:
        print(f"Error retrieving data for video ID {video_id}: {e}")
        return None

# Function to insert video data
def insert_video_data(video_data, engine):
    try:
        if video_data:
            video_df = pd.DataFrame([video_data])
            video_df.to_sql(name='video', con=engine, if_exists='append', index=False)
            print(f"Video data for ID {video_data['video_id']} inserted successfully!")
        else:
            print(f"Skipping video data insertion due to missing data.")
    except Exception as e:
        print(f"Error inserting video data for ID {video_data['video_id']}: {e}")

comment_ids = []
def comments(playlist_videos):
    try:
        for video_id in playlist_videos:
            request = youtube.commentThreads().list(part="snippet", videoId=video_id, maxResults=100)
            response = request.execute()
            if "items" in response:
                for item in response["items"]:
                    comment_ids.append(item["id"])
    except Exception as e:
        print(f"Error fetching comments: {e}")
    return comment_ids    

comments(playlist_videos=playlist_videos) 


     

# Function to get comment data
def get_comment_data(comment_id, video_id, youtube):
    try:
        request = youtube.comments().list(part="snippet", id=comment_id)
        response = request.execute()

        comment_data = {
            "video_id": video_id,
            "comment_id": comment_id,
            "comment_text": response['items'][0]['snippet']['textOriginal'],
            "comment_author": response['items'][0]['snippet']['authorDisplayName'],
            "comment_published_at": response['items'][0]['snippet']['publishedAt']
        }
        return comment_data
    except Exception as e:
        print(f"Error retrieving data for comment ID {comment_id}: {e}")
        return None

# Function to insert comment data
def insert_comment_data(comment_data, engine):
    try:
        if comment_data:
            comment_df = pd.DataFrame([comment_data])
            comment_df.to_sql(name='comment', con=engine, if_exists='append', index=False)
            print(f"Comment data for ID {comment_data['comment_id']} inserted successfully!")
        else:
            print(f"Skipping comment data insertion due to missing data.")
    except Exception as e:
        print(f"Error inserting comment data for ID {comment_data['comment_id']}: {e}")

# Function to parse duration - Converting duration present as string to integer in seconds
def parse_duration(duration_str):
    try:
        match = re.search(r"^PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?$", duration_str)
        if match:
            hours, minutes, seconds = match.groups()
            hours = int(hours or 0)
            minutes = int(minutes or 0)
            seconds = int(seconds or 0)
            return hours * 3600 + minutes * 60 + seconds
        else:
            print(f"Warning: Invalid duration format: {duration_str}")
            return 0
    except Exception as e:
        print(f"Error parsing duration: {e}")
        return 0

# Main execution
try:
    # Get channel data
    channel_data = get_channel_data(channel_id, youtube)
    # Insert channel data
    insert_channel_data(channel_data, engine)

    # Get video data
    playlist_videos = video_ids(channel_id, youtube)
    for video_id in playlist_videos:
        video_data = get_video_data(video_id, channel_id, youtube)
        insert_video_data(video_data, engine)

    # Get comment data
    comment_ids = comments(playlist_videos)
    for comment_id in comment_ids:
        comment_data = get_comment_data(comment_id, video_id, youtube)
        insert_comment_data(comment_data, engine)

    print("Data harvesting and insertion completed successfully!")

except Exception as e:
    print("Error occurred:", e)
