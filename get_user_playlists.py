import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="10d3ea965cf04b8484b4f49d8ce8fb16",
                                               client_secret="483d7bdc5b3e4dc28bd67370b7bc4de9",
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="user-library-read playlist-modify-private playlist-modify-public",
                                               show_dialog=True,
                                               cache_path="token.txt"))


results = sp.user_playlists("stuart5971")
response_json = json.dumps(results)
with open('app.json', 'w') as fp:
    json.dump(results, fp)
# for playlist in results['items']:
#     print(playlist['name'])