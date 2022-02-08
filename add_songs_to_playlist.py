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

# sp.playlist_add_items(playlist_id,['3a7ziOOO3Cbuv6BMXrj0wU'])
sp.playlist_add_items(playlist_id, ['0GGfGINoVYiSFXPOjg3RHj', '450u5gGMGwQXmtLSR7AN2s', '6JpN5w95em8SODPiM7W2PH', '4tr4oHjFijp0EgISHYDIXe', '70o3Clq7OXVKYps0jYiTEi', '4Pgh4b9rY9vVuXXl4Y1ob8', '0H1oMxanFzeKs8huBRtOn6', '4czNORk5MjW5WOn98bki32', '7FXj7Qg3YorUxdrzvrcY25', '6O20JhBJPePEkBdrB5sqRx', '7795WJLVKJoAyVoOtCWqXN', '4iN16F8JtVxG2UTzp3avGl', '2bCQHF9gdG5BNDVuEIEnNk', '0gplL1WMoJ6iYaPgMCL0gX', '6LNoArVBBVZzUTUiAX2aKO', '6vt0I1cw1YmAIKDJvHVIM5'])
print('done')



