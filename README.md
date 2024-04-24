
# YouTube Data Harvesting and Warehousing using SQL and Streamlit

A brief description of what this project does and who it's for


## Overview

This project is focused on harvesting channel, video and comment  data from YouTube channels using the YouTube API, processing the data, and warehousing it. The harvested data is stored in MySQL database in seperate tables for channel, video and comment data respectively. The project's core functionality relies on the Extract, Transform, Load (ETL) process.
## Approach

1) Get your youtube api key from Google developers console(https://console.developers.google.com/project) to fetch data using Youtube API. 
2) Create a database in MySQL containing Channel , Video and Comment tables respectively to collect data .
3) Insert the data fetched through YouTube API to the MySQL tables using SQLAlchemy by creating an engine.
4)Create Streamlit app to present data in user-friendly interface.
5)Execute data analysis using SQL queries and Python integration.

## Getting started

1) Install/Import necessary libraries:Googleapiclient,
 Pandas,MySQL,SQLAlchemy,Streamlit


2) Ensure you have access to MySQL server and set up MySQL DBMS on your local environment.


## Steps involved in the execution of the project
Step1: Install/Import required modules.
Step2: Get your Youtube API key from Google developers console(https://console.developers.google.com/project) by creating a project enabling youTube data api v3 and getting the credentials.
Step3: Configure database.Ensure that you are connected to MySQL server.
Step4:Run the project using streamlit.Open the command prompt in the  the youtube_main_page.py and execute the command: streamlit run youtube_main_page.py
This will open a web browser displaying the the project's user interface.
## Methods
1) Fetch YouTube channel data using Channel ID. 
2) Insert channel data to channel table in MySQL using SQLAlchemy engine.
3) Get all video IDs of the channel using playlist ID 
4) Insert video data to the video table in MySQL using SQLAlchemy engine.
5) Get upto maximum of 100 comment IDs of each video using video ID.
6) Insert comment data to the comment table in MySQL using SQLAlchemy engine.

## Tools Expertise
Python scripting, Data Collection, Streamlit, API integration, Data Management using SQL  
## Result
This project aims to develop a user-friendly Streamlit application that utilizes the Google API to extract information on a YouTube channel, stores it in a SQL database, and enables users to search for channel details and join tables to view data in the Streamlit app.