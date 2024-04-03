import googleapiclient.discovery
import pandas as pd
import logging
# from video import video_details
# from playlist import playlist_details

# # Define the API_KEY and the CHANNEL_ID
# API_KEY = "AIzaSyDHCf3HwoldxHIYSHCB9JAeBYzx1hvg1WA"
# CHANNEL_ID="UCduIoIMfD8tT3KoU0-zBRgQ" #Channel_id #Guvi Channel id
# # Define the video ID
# # VIDEO_ID ="hfDNdc9m11I"
# PLAYLIST_LST=playlist_details(API_KEY,CHANNEL_ID)
# VIDEO_LST= ['_kNrrFITwac','_Q0q2KbP4xE','_vmUgsrzXK4','-aNgkaxzZxY','-PGLrwPLFYI','-zWujhGwW0g','0-NCXuRCb5w']

# print('The video list is :', VIDEO_LST)
# print('The Length of Video list is :', len(VIDEO_LST))

def comment_details(API_KEY, VIDEO_LST):
    # Define the maximum number of comments to retrieve (optional)
    MAX_RESULTS = 100  # Adjust this value as needed

    # Define the YouTube service object
    youtube = googleapiclient.discovery.build(
    "youtube", "v3", developerKey=API_KEY  
    )
    # Create a dictionary to fit comments 
    comments_dict=dict()
    # Creating the structure for dictionary
    comments_dict['comment_id']=list()
    comments_dict['video_id']=list()
    comments_dict['comment_text']=list()
    comments_dict['comment_author']=list()
    comments_dict['comment_published_date']=list()
    # NEW_VIDEO_LST=VIDEO_LST[0:6]
    # print(f'The Video List being Processed is : {NEW_VIDEO_LST}')
    for VIDEO_ID in VIDEO_LST:
        # print(f"Processing Video ID ------>>>> {VIDEO_ID}")
        try:
            # Define the request parameters
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=VIDEO_ID,
                maxResults=MAX_RESULTS
            )

            # Execute the request and get the response
            response = request.execute()

            # Extract and print comments information
            if len(response["items"]) > 0:
                for item in response["items"]:
                    comments_dict['video_id'].append(item["snippet"]["videoId"])
                    comments_dict['comment_id'].append(item["id"])
                    comments_dict['comment_text'].append(item["snippet"]["topLevelComment"]['snippet']["textDisplay"])  # Access comment text
                    comments_dict['comment_author'].append(item["snippet"]["topLevelComment"]['snippet']["authorDisplayName"])  # Access author name
                    comments_dict['comment_published_date'].append(item["snippet"]["topLevelComment"]['snippet']["publishedAt"])  # Access published date

            else:
                print(f"No comments found for the video. {VIDEO_ID}")
                logging.info(f"No comments found for the video. {VIDEO_ID}")
        except googleapiclient.errors.HttpError as error:
            print(f"Error retrieving comments for video ID: {VIDEO_ID} and the error is {error}")
            logging.error(f"Error retrieving comments for video ID: {VIDEO_ID} and the error is {error}")
            # Skip to the next video ID
            continue
        except Exception as e:
            print(f"Unexpected Error occured")
            logging.error(f"Unexpected Error occured")
    # print(comments_dict)
    comments_df=pd.DataFrame(comments_dict)
    comments_df['comment_published_date'] = pd.to_datetime(comments_df['comment_published_date'])
    comments_df['comment_published_date'] = comments_df['comment_published_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # print(comments_df)
    return comments_df

# if __name__ == "__main__":
#     comment_details(API_KEY, VIDEO_LST)
