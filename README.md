# Youtube Data Harvesting Project

## Overview
The YouTube Data Harvesting project aims to extract, process, and visualize data from YouTube channels using the YouTube Data API. The project consists of two main components: Data Extraction and Visualization.

## Project Architecture
The project architecture involves the following components:

1. **Streamlit App**: The user interface for interacting with the project. It allows users to extract data and visualize insights.

2. **Data Extraction, Processing & DB Load Module**:
    - This module collects data from YouTube channels based on user-provided Channel IDs.
    - It retrieves various details such as channel information, playlist details, video details, and comment details using YouTube API keys.
    - The retrieved data is processed into dataframes and loaded into a MySQL Workbench database for further analysis.

3. **Visualization Module**:
    - This module presents a set of predefined questions in a dropdown menu.
    - Upon selecting a question and clicking submit, an SQL query is executed to fetch relevant data from the database.
    - The query results are displayed as dataframes within the Streamlit app for visualization.

## Data Flow / Functionality
### Data Extraction, Processing & DB Load:
1. **Input**: User provides a Channel ID through the Streamlit app.
2. **Data Retrieval**: The system uses YouTube API keys to fetch channel, playlist, video, and comment details from YouTube.
3. **Processing**: The retrieved data is processed and structured into dataframes.
4. **Database Load**: Dataframes are loaded into a MySQL Workbench database.

### Visualization:
1. **Question Selection**: Users select a predefined question from the dropdown menu in the Streamlit app.
2. **Query Execution**: The system executes an SQL query corresponding to the selected question to retrieve data from the database.
3. **Result Presentation**: The query results are displayed as dataframes within the Streamlit app for visualization.

## Error Handling Techniques
1. **Exception Handling**: Comprehensive exception handling is implemented throughout the project to handle errors gracefully.
2. **Logging**: Logging functionality is integrated to capture detailed information, including errors, during the execution of the project. Log files are generated for each run.
3. **Intermediate CSV Files**: Intermediate CSV files are created for channel, playlist, video, and comment data. These files serve as backups and aids in troubleshooting in case of any issues during execution.

## Python Setup 
### create a Python environment
```
conda create -p venv python==3.8
```

### Install all necessary libraries
```
pip install -r requirements.txt
```


## Database Setup
### MySQL Workbench Database
1. **Database Creation**:
   ```sql
   CREATE DATABASE youtube_data_harvesting;
   ```
   
   ```sql 
   create table youtube_data_harvesting.channel(
                channel_id varchar(255) primary key,
                channel_name varchar(255),
                channel_description TEXT,
                channel_views INT,
                channel_status varchar(255),
                channel_type varchar(255));
    ```

    ```sql
    create table youtube_data_harvesting.playlist(
                 playlist_id varchar(255) primary key,
                 channel_id varchar(255),
                 playlist_name varchar(255));
    ```

    ```sql
    create table youtube_data_harvesting.video(
                 video_id varchar(255) primary key,
                 playlist_id varchar(255),
                 video_name varchar(255),
                 video_description TEXT ,
                 published_date DATETIME,
                 view_count INT,
                 like_count INT,
                 dislike_count INT,
                 favorite_count INT,
                 comment_count INT,
                 duration float,
                 thumbnail VARCHAR(255));
    ```

    ```sql
    create table youtube_data_harvesting.comment(
                 comment_id varchar(255) primary key,
                 video_id varchar(255),
                 comment_text TEXT,
                 comment_author varchar(255),
                 comment_published_date DATETIME
                 );
    ```
