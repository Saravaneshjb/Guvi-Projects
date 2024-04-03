import googleapiclient.discovery
import pandas as pd
import logging


def playlist_details(API_KEY, CHANNEL_ID):
        # Define the YouTube service object
    youtube = googleapiclient.discovery.build(
        "youtube", "v3", developerKey=API_KEY
    )

    # Define the request parameters
    request = youtube.playlists().list(
        part="snippet",
        channelId=CHANNEL_ID,
        maxResults=500  # Adjust this parameter to retrieve a desired number of playlists
    )

    # Execute the request and get the response
    response = request.execute()
    # pprint.pprint(response)
    # Creating a dictionary for storing the playlist details
    playlist_dict=dict()
    #Setting the structure of the dictionary 
    playlist_dict['playlist_id']=list()
    playlist_dict['channel_id']=list()
    playlist_dict['playlist_name']=list()
    # # Extract and print playlist information
    if len(response["items"]) > 0:
        for index,item in enumerate(response["items"]):
            playlist_dict['channel_id'].append(item['snippet']['channelId'])
            playlist_dict['playlist_id'].append(item["id"])
            playlist_dict['playlist_name'].append(item['snippet']["localized"]["title"])
            # print(f"Channel ID:{channel_id}, Playlist ID: {playlist_id}, Title: {title}")
    else:
        print("No playlists found for the channel.")
        logging.info("No playlists found for the channel.")

    #Creating a dataframe for the playlist dictionary
    playlist_df=pd.DataFrame(playlist_dict)
    # print(playlist_df)
    return playlist_df, playlist_dict['playlist_id']

# if __name__ == "__main__":
#     playlist_details(API_KEY, CHANNEL_ID)
