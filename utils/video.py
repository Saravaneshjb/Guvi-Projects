import googleapiclient.discovery
import pandas as pd
import logging
from utils.preprocessing import convert_duration
from googleapiclient.errors import HttpError

MAX_RESULTS=500

def video_details(API_KEY, PLAYLIST_LST):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)
    video_dict = {
        'video_id': [],
        'playlist_id': [],
        'video_name': [],
        'video_description': [],
        'published_date_old': [],
        'view_count': [],
        'like_count': [],
        'dislike_count': [],
        'favorite_count': [],
        'comment_count': [],
        'duration_old': [],
        'thumbnail': []
        # ,
        # 'caption_status': []
    }

    for PLAYLIST_ID in PLAYLIST_LST:
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=PLAYLIST_ID,
            maxResults=MAX_RESULTS
        )
        response = request.execute()
        
        if len(response["items"]) > 0:
            for item in response["items"]:
              try:
                video_id = item["snippet"]["resourceId"]["videoId"]
                video_dict['video_id'].append(video_id)   
                video_dict['playlist_id'].append(item["snippet"]["playlistId"])
                video_dict['video_name'].append(item["snippet"]["title"])
                video_dict['video_description'].append(item["snippet"]["description"])
                video_dict['published_date_old'].append(item["snippet"]["publishedAt"])
                # video_dict['duration'].append(item["contentDetails"].get("duration", "no duration available"))

                # Retrieve statistics for the video
                video_details = youtube.videos().list(
                        part='contentDetails,statistics',
                        id=video_id
                    ).execute().get('items', [])
                    
                if video_details:
                    video_details = video_details[0]
                    content_details = video_details.get('contentDetails', {})
                    statistics = video_details.get('statistics', {})
                    
                    # Retrieve duration
                    duration = content_details.get('duration')
                    video_dict['duration_old'].append(duration)
                    
                    # Retrieve statistics
                    video_dict['view_count'].append(statistics.get('viewCount', 0))
                    video_dict['like_count'].append(statistics.get('likeCount', 0))
                    video_dict['dislike_count'].append(statistics.get('dislikeCount', 0))
                    video_dict['favorite_count'].append(statistics.get('favoriteCount', 0))
                    video_dict['comment_count'].append(statistics.get('commentCount', 0))
                else:
                    # Append default values if video details are not available
                    video_dict['duration_old'].append(0)
                    video_dict['view_count'].append(0)
                    video_dict['like_count'].append(0)
                    video_dict['dislike_count'].append(0)
                    video_dict['favorite_count'].append(0)
                    video_dict['comment_count'].append(0)
                
                 
                # Thumbnail URLs
                thumbnails = item["snippet"]["thumbnails"]
                video_dict['thumbnail'].append(thumbnails.get('default', {}).get('url', ''))

                # Caption status
                # Check if captions are available for the video
                # captions_info = youtube.captions().list(
                #     part='snippet',
                #     videoId=video_id
                # ).execute().get("items", [])

                # # Set caption status based on availability
                # if captions_info:
                #     caption_status = captions_info[0]["snippet"]["status"]
                # else:
                #     caption_status = 'Not available'
              except googleapiclient.errors.HttpError as error:
                print(f"Error retrieving details for video ID: {video_id} in playlist : {PLAYLIST_ID}")
                logging.error(f"Error retrieving details for video ID: {video_id} in playlist : {PLAYLIST_ID}")
                # Skip to the next video ID
                continue
              except Exception as e:
                print(f"Unexpected Error occured processing Playlist - {PLAYLIST_ID} & video - {video_id}")
                logging.error(f"Unexpected Error occured processing Playlist - {PLAYLIST_ID} & video - {video_id}")

        else:
            print(f"No videos found in the playlist --> {PLAYLIST_ID}")
            logging.info(f"No videos found in the playlist --> {PLAYLIST_ID}")

    video_df = pd.DataFrame(video_dict)
    # print(video_df[['video_id','published_date_old']])
    ## Converting the formats of published_date and duration 
    video_df['published_date'] = pd.to_datetime(video_df['published_date_old'])
    # print(video_df[['video_id','published_date_old','published_date']])
    video_df['published_date'] = video_df['published_date'].dt.strftime('%Y-%m-%d %H:%M:%S')

    video_df['duration'] = video_df['duration_old'].apply(convert_duration)
    ## Dropping the unused columns from the dataframe 
    video_df.drop(columns=['published_date_old','duration_old'],inplace=True)

    ## Setting the duration column shich has nan values to 0. 
    nan_duration_rows=video_df['duration'].isna()
    video_df.loc[nan_duration_rows,'duration']=0

    if len(video_df[video_df.duplicated('video_id')]) > 0:
        video_df.drop_duplicates(subset=['video_id'],inplace=True)
    else:
        video_df
    
    video_id_lst=list(video_df['video_id'])
    # print(video_df)

    return video_df, video_id_lst


# if __name__ == "__main__":
#     video_details(API_KEY, PLAYLIST_LST)
