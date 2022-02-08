# Project to create Spotify playlist from liked Youtube videos

# Step 1: Log into Youtube
# Step 2: Grab our Liked Videos 
# Step 3: Create a New Playlist
# Step 4: Search For The Song 
# Step 5: Add this song into the new Spotify playlist


import os
import json
import requests

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import youtube_dl

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
from secrets import spotify_user_id, youtube_api_key, spotify_token
# scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="10d3ea965cf04b8484b4f49d8ce8fb16",
                                               client_secret="483d7bdc5b3e4dc28bd67370b7bc4de9",
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="user-library-read playlist-modify-private playlist-modify-public",
                                               show_dialog=True,
                                               cache_path="token.txt"))


print('new playlist')
class CreatePlaylist:
    def __init__(self) -> None:
        self.user_id = spotify_user_id
        self.spotify_token = spotify_token
        self.credentials = None
        self.youtube_client = self.get_youtube_client()
        self.all_playlists = self.get_user_playlists()
        self.playlist_name = "Youtube Liked Vids"
        self.all_song_info = {}

    # Step 1: Log into Youtube
    def get_youtube_client(self):
        # Sample Python code for youtube.search.list
        #copied from Youtube Data API - > https://developers.google.com/explorer-help/guides/code_samples#python
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret.json"

        # token.pickle stores the user's credentials from previously successful logins
        if os.path.exists("token.pickle"):
            print("Loading Credentials From File...")
            with open("token.pickle", "rb") as token:
                self.credentials = pickle.load(token)
                print('initialisation done')

        # If there are no valid credentials available, then either refresh the token or log in
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                print("Refreshing Access Token...")
                self.credentials.refresh(Request())
            else:
                print("Fetching New Tokens...")
                flow = InstalledAppFlow.from_client_secrets_file("client_secret_one_last_time.json", scopes=["https://www.googleapis.com/auth/youtube.readonly"])
                flow.run_local_server(port=3000, prompt='consent', authorization_prompt_message='')
                self.credentials = flow.credentials
                
                # Save the credentials for the next run
                with open("token.pickle", "wb") as f:
                    print("Saving Credentials for Future Use...")
                    pickle.dump(self.credentials, f)

        #from the Youtube DATA API
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=self.credentials)

        return youtube_client

    # Step 2: Grab our Liked Videos and Creating a Dictionary Of Important Song Information
    def get_liked_videos(self):

        request = self.youtube_client.videos().list(
        part="snippet,contentDetails,statistics",
        maxResults=50,
        myRating="like"
    )
        response = request.execute()

        #collect each video and get important information
        for item in response["items"]:
            
            video_title = item["snippet"]["title"]
            youtube_url = "https://www.youtube.com/watch?v={}".format(item["id"])

            # use youtube_dl to collect the song name & artist name
            video = youtube_dl.YoutubeDL({}).extract_info(youtube_url, download=False)
            if( video["track"] != None and video["artist"] != None):
                song_name=video["track"]
                artist = video["artist"]

                
                if(self.get_spotify_uri(song_name,artist) != ""):
                # save all important info
                    self.all_song_info[video_title]={
                        "youtube_url":youtube_url,
                        "song_name":song_name,
                        "artist":artist,

                        #add the uri, easy to get song to put into playlist
                        "spotify_uri": self.get_spotify_uri(song_name,artist)
                }
                else:
                    continue

    # Step 3: Create a New Playlist
    def create_playlist(self):
        
        result = sp.user_playlist_create(self.user_id,self.playlist_name,public=True,description="All Liked Youtube Videos")

        # playlist id
        return result["id"]

    # Step 4: Search For The Song 
    def get_spotify_uri(self, song_name, artist):
        
        result = sp.search(song_name + " " + artist,limit=1,)
       
        
        if(result["tracks"]["items"] != []  ):
            song = result["tracks"]["items"]
            song_id = song[0]["id"]
            return song_id
        else:
            print("Error in youtube music data")
            return ""
    
    def get_user_playlists(self):

        results = sp.user_playlists("stuart5971")

        return results

        #Get songs on playlist and compare
    def get_songs_on_playlist(self, playlist_id, ids): 

        songs = sp.playlist_items(playlist_id)

        current_playlist_song_IDs = []
        #extract playlist_song_uris
        for song in songs["items"]:
            current_playlist_song_IDs.append(song["track"]["id"])

        
        #compare
        new_ids = []
        for to_be_added_id in ids:
            if to_be_added_id not in current_playlist_song_IDs:
                new_ids.append( to_be_added_id )
        
        
        return new_ids

    # Step 5: Add this song into the new Spotify playlist
    def add_song_to_playlist(self):
        #populate our songs dictionary
        self.get_liked_videos()
        
        ids = []
        
        for info in self.all_song_info.items():
            ids.append(info[1]['spotify_uri'])
        
        playlist_id = ""

        for single_playlist in self.all_playlists["items"]:
            if(single_playlist["name"] == self.playlist_name):
                #update playlist
                playlist_id = single_playlist["id"]
                ids = self.get_songs_on_playlist(playlist_id,ids)
                break
            else:
                # create a new playlist
                playlist_id = self.create_playlist()
                break  

        if( ids == []):
            print('No songs to be added')
            return
        else:
            #add all songs into new playlist
            result = sp.playlist_add_items(playlist_id,ids)
            return result

if __name__ == '__main__':
    cp = CreatePlaylist()
    cp.add_song_to_playlist()
    print('Project Complete!')