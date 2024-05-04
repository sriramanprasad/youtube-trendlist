import streamlit as st
from googleapiclient.discovery import build

# YouTube API
youtube_api_key = st.secrets["api"]
youtube = build('youtube', 'v3', developerKey=youtube_api_key)

# Country codes for the four countries
country_codes = {
    'India': 'IN',
    'Australia': 'AU',
    'USA': 'US',
    'UK': 'GB'
}

# Mapping of category names to category IDs
categories = {
    'Film & Animation': 1,
    'Music': 10,
    'Sports': 17,
    'Comedy': 23,
    'Entertainment': 24,
    'News & Politics': 25,
    'Howto & Style': 26,
    'Education': 27,
    'Science & Technology': 28
}

# Function to fetch top trending videos and hashtags for a given country and category
def fetch_trending_videos(country_code, category_id, max_results):
    youtube_response = youtube.videos().list(
        part='snippet',
        chart='mostPopular',
        regionCode=country_code,
        videoCategoryId=category_id,
        maxResults=max_results
    ).execute()

    trending_videos = []
    for video in youtube_response['items']:
        video_id = video['id']
        title = video['snippet']['title']
        hashtags = video['snippet'].get('tags', [])
        trending_videos.append((title, video_id, hashtags))

    return trending_videos

# Streamlit app
st.title('Top Trending YouTube Videos with Hashtags')
selected_country = st.selectbox('Select a country:', list(country_codes.keys()))
selected_category = st.selectbox('Select a category:', list(categories.keys()))

country_code = country_codes[selected_country]
category_id = categories[selected_category]

# Slider for selecting number of videos
num_videos = st.slider('Select number of videos to display:', min_value=1, max_value=50, value=10)

# Button to fetch trending videos
if st.button('Fetch Trending Videos'):
    trending_videos = fetch_trending_videos(country_code, category_id, num_videos)

    for title, video_id, hashtags in trending_videos:
        st.video(f'https://www.youtube.com/watch?v={video_id}')
        st.write('Title:', title)
        st.write('Hashtags:', ', '.join(hashtags) if hashtags else 'None')
