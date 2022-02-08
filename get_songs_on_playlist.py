import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint
import json
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="10d3ea965cf04b8484b4f49d8ce8fb16",
                                               client_secret="483d7bdc5b3e4dc28bd67370b7bc4de9",
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="user-library-read playlist-modify-private playlist-modify-public",
                                               show_dialog=True,
                                               cache_path="token.txt"))


results = sp.user_playlists("stuart5971")
playlist_id = ''
for playlist in results['items']:
    if(playlist['name'] == 'Youtube Liked Vids'):
        print(playlist['name'])
        print(playlist['id'])
        playlist_id = playlist['id']

print('')
songs = sp.playlist_items(playlist_id)
for song in songs['items']:
    print(song['track']['id'])



