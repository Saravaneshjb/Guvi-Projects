import os
import streamlit as st
import pandas as pd
import logging
from datetime import datetime
from utils.channel import channel_details
from utils.playlist import playlist_details
from utils.video import video_details
from utils.comment import comment_details
from mysql.connector import IntegrityError
from database.data_load_sql_connector import Dataload
from database.data_extract import execute_query


## Setting up the logging 
# Create a log folder if it doesn't exist
if not os.path.exists("logs"):
    os.makedirs("logs")

# Get current date and time
current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Configure logging with the dynamic log file name
log_file_name = f"logs/log_file_{current_datetime}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename=log_file_name
)


def extract_data():
    st.title("YouTube Data Harvesting Project")
    
    # Input field to get the YouTube channel ID, API_KEY from the user
    channel_id = st.text_input("Enter YouTube Channel ID:")
    
    if st.button("Extract Channel Details"):
        # Call your channel_details function with API Key and user-provided channel ID
        API_KEY = ""  # Replace "YOUR_API_KEY" with your actual YouTube API key
        directory="process_dataframe"
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        #creating a dictionary to store the dataframe details 
        data_df=dict()
        # file_path=os.path.join()
        logging.info('Started Channel data extraction')
        channel_df = channel_details(API_KEY, channel_id)
        data_df['channel'] = channel_df
        channel_df.to_csv(os.path.join(directory,'channel.csv'),index=False)
        logging.info('Completed Channel data extraction')
        logging.info('Started Playlist data extraction')
        playlist_df, playlist_lst=playlist_details(API_KEY,channel_id)
        data_df['playlist'] = playlist_df
        playlist_df.to_csv(os.path.join(directory,'playlist.csv'),index=False)
        logging.info('Completed Playlist data extraction')
        logging.info('Started video data extraction')
        #sample playlist 
        # playlist_lst=["PL8Q-CmKVRc9r8qQEBhDrxAWxVn0A5YuX3"]
        video_df, video_lst=video_details(API_KEY,playlist_lst)
        #Preprocess Video_df
        video_df = video_df.where(pd.notnull(video_df), None)
        data_df['video'] = video_df
        video_df.to_csv(os.path.join(directory,'video.csv'),index=False)
        logging.info('Completed video data extraction')
        logging.info('Started comments data extraction')
        comment_df=comment_details(API_KEY,video_lst)
        data_df['comment']=comment_df
        comment_df.to_csv(os.path.join(directory,'comment.csv'),index=False)
        logging.info('Completed comments data extraction')
        for dataframe in data_df: 
            if dataframe is not None:
                # Display the DataFrame returned by the function
                # st.write(dataframe)
                try:
                    dl_ob=Dataload()
                    dl_ob.load_df(data_df[dataframe],dataframe)
                    st.success(f"{dataframe} Data Extracted, processed & loaded successfully")
                    logging.info(f"{dataframe} Data Extracted, processed & loaded successfully")
                except IntegrityError as e:
                    st.error(f'Unique Key Violation while inserting the to the {dataframe} table. Provide another id')
                    logging.error(f'Unique Key Violation while inserting the to the {dataframe} table. Provide another id')
                except Exception as e:
                    st.error(f"Error loading {dataframe} data to database {e}")
                    logging.error(f"Error loading {dataframe} data to database {e}")
            else:
                st.error('Failed to retrieve channel details. Please check the Channel ID')
                logging.error('Failed to retrieve channel details. Please check the Channel ID')


# Queries to be executed
queries={
        "What are the names of all the videos and their corresponding channels?": """
            SELECT vd.video_name, ch.channel_name
            FROM video vd
            JOIN playlist pl ON vd.playlist_id = pl.playlist_id
            JOIN channel ch ON pl.channel_id = ch.channel_id
        """,
        "which channels have the most number of videos and how many videos do they have":"""
            select video_count,channel
            from 
            (select count(vd.video_name) as "video_count", ch.channel_name as "channel"
            from channel ch 
            join playlist pl
            on   ch.channel_id=pl.channel_id
            join video vd
            on pl.playlist_id=vd.playlist_id
            group by ch.channel_name
            order by video_count DESC
            LIMIT 1) as my_tab;
        """,
        "What are the top 10 most viewed videos and their respective channels":"""
            select vd.video_name,vd.view_count,ch.channel_name
            from channel ch 
            join playlist pl
            on   ch.channel_id=pl.channel_id
            join video vd
            on pl.playlist_id=vd.playlist_id
            order by vd.view_count DESC
            LIMIT 10
         """,
         "How many comments were made of each video and what are their corresponding video names":"""
            select vd.video_name,vd.comment_count
            from channel ch 
            join playlist pl
            on   ch.channel_id=pl.channel_id
            join video vd
            on pl.playlist_id=vd.playlist_id
          """,
          "Which videos have the highest number of likes and what are their corresponding channel names":"""
            select vd.video_name, vd.like_count, ch.channel_name
            from channel ch 
            join playlist pl
            on   ch.channel_id=pl.channel_id
            join video vd
            on pl.playlist_id=vd.playlist_id
            order by vd.like_count DESC
            LIMIT 1;
           """,
           "What are the total number of likes, dislikes for each video and what are their corresponding video name":"""
            select sum(like_count) + sum(dislike_count) as "sum of like/dislike per video",
            vd.video_name 
            from video vd
            group by vd.video_name;
            """,
            "what is the total number of views for each channel, and what are their corresponding channel names":"""
              select channel_name, channel_views as "Views"
              from youtube_data_harvesting.channel ch
              order by channel_views DESC;
             """,
             "What are the names of all the channels that have published videos in the year 2022?":"""
                select distinct ch.channel_name
                from channel ch 
                join playlist pl
                on   ch.channel_id=pl.channel_id
                join video vd
                on pl.playlist_id=vd.playlist_id
                where YEAR(vd.published_date)=2022;
             """,
             "What is the average duration of all videos in each channel, and what are their corresponding channel names?":"""
                select ch.channel_name,round(avg(vd.duration),1)
                from channel ch 
                join playlist pl
                on   ch.channel_id=pl.channel_id
                join video vd
                on pl.playlist_id=vd.playlist_id
                group by ch.channel_name;
              """,
              "Which videos have the highest number of comments, and what are their corresponding channel names?":"""
                select vd.video_name as 'video_name', 
                ch.channel_name as 'channel_name',
                vd.comment_count as 'comment_count'
                from youtube_data_harvesting.channel ch 
                join youtube_data_harvesting.playlist pl on   ch.channel_id=pl.channel_id
                join youtube_data_harvesting.video vd on pl.playlist_id=vd.playlist_id
                join (
                    select max(comment_count) as "max_comment_count"
                    from youtube_data_harvesting.video
                    ) AS max_comments 
                ON vd.comment_count=max_comments.max_comment_count
                order by vd.comment_count desc
              """,
              "Which videos have the highest number of comments, and what are their corresponding channel names?":"""
                SELECT video_name, channel_name, comment_count
                FROM (
                    SELECT vd.video_name,
                        ch.channel_name,
                        vd.comment_count,
                        ROW_NUMBER() OVER(PARTITION BY ch.channel_id ORDER BY vd.comment_count DESC) AS rn
                    FROM youtube_data_harvesting.channel ch
                    JOIN youtube_data_harvesting.playlist pl ON ch.channel_id = pl.channel_id
                    JOIN youtube_data_harvesting.video vd ON pl.playlist_id = vd.playlist_id
                ) AS ranked
                WHERE rn = 1
               """
       }



# Function to visualize data
def visualize_data():
    st.title("Visualize Data")
    question = st.selectbox("Select a question:", list(queries.keys()))
    if st.button("Get Answer"):
        if question in queries:
            query_result = execute_query(queries[question])
            if query_result is not None:
                st.write("Query Result:")
                st.write(query_result)
            else:
                st.error("Failed to fetch data from the database.")
                logging.error("Failed to fetch data from the database.")
        else:
            st.error("Invalid question selected.")
            logging.error("Invalid question selected.")

# Set background color
st.markdown(
    """
    <style>
    .reportview-container {
        background: linear-gradient(120deg, #fdfbfb 0%, #ebedee 100%);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Add sidebar options
option = st.sidebar.selectbox(
    'Choose an option:',
    ('Extract data', 'Visualize data')
)

# Based on the selected option, call the corresponding function
if option == 'Extract data':
    extract_data()
elif option == 'Visualize data':
    visualize_data()
