import googleapiclient.discovery
import pandas as pd
import logging

# Replace with your YouTube Data API v3 API key
API_KEY = "AIzaSyBgFY8OEiMSK-sq8Odr1yu2_T7v06du2fM"

# Define the channel ID
CHANNEL_ID = "UCduIoIMfD8tT3KoU0-zBRgQ" #Guvi
# CHANNEL_ID ="UCJcCB-QYPIBcbKcBQOTwhiA" #Vjsiddhu vlogs


def channel_details(API_KEY, CHANNEL_ID):
    # Define the YouTube service object
    youtube = googleapiclient.discovery.build(
        "youtube", "v3", developerKey=API_KEY
    )

    # Define the request parameters
    request = youtube.channels().list(
        part="snippet,status,statistics",
        id=CHANNEL_ID,
        maxResults=150
    )

    # Execute the request and get the response
    response = request.execute()

    #creating a sample dictionary
    my_dict=dict()
    
    # Print the response
    for item in response['items']:
        my_dict['channel_id']=CHANNEL_ID
        my_dict['channel_name']=item['snippet']['title']
        my_dict['channel_description']=item['snippet']['description']
        my_dict['channel_views']=item['statistics']['viewCount']
        my_dict['channel_status']=item['status']['privacyStatus']
    
    # Retrieve channel sections
    channel_sections_response = youtube.channelSections().list(
        part='snippet',
        channelId=CHANNEL_ID
    ).execute()

    # Find the main channel section
    for section in channel_sections_response['items']:
        if section['snippet']['type'] == 'single_channel':
            main_section_title = section['snippet']['title']
            break
    else:
      main_section_title='unavailable'
    
    # Append channel type to dictionary
    my_dict['channel_type'] = main_section_title
    
    data=pd.Series(my_dict)
    channel_df=pd.DataFrame(data).T
    return channel_df

if __name__ == "__main__":
    channel_details(API_KEY, CHANNEL_ID)
