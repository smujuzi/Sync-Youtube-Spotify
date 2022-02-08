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


result = sp.user_playlist_create("stuart5971","justCreated3")
print(result["id"])


