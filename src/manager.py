import requests
import json


# Manage retreiving artists names, executing the request to the api
# and then populating the playlist just created
class Manager:
    def __init__(self):
        with open("config.json", "r") as f:
            self.json = json.load(f)
        self.client_id = self.json["config"]["client_id"]
        self.client_secret = self.json["config"]["client_secret"]
        self.spotify_token = self.json["config"]["access_token"]
        self.scope = 'playlist-modify-public'
        self.artists = []
        self.songs = []

    def create_playlist(self):
        r = json.dumps({
            "name": "rappa trappa 2021 🔥",
            "description": "tracks released on 2021",
            "public": True
        })
        endpoint = "https://api.spotify.com/v1/users/{}/playlists".format(
            self.client_id)
        response = requests.post(endpoint,
                                 data=r,
                                 headers={
                                     "Content-Type":
                                     "application/json",
                                     "Authorization":
                                     "Bearer {}".format(self.spotify_token)
                                 })
        self.playlist_id = response.json()["id"]

    def get_artist_name(self):
        names = []
        for artist in self.json["artists"]:
            query = "https://api.spotify.com/v1/search?query=%3A{}&type=artist&limit=1".format(
                artist)
            response = requests.get(query,
                                    headers={
                                        "Content-Type":
                                        "application/json",
                                        "Authorization":
                                        "Bearer {}".format(self.spotify_token)
                                    })
            if len(response.json()['artists']['items']) != 0:
                names.append(response.json()['artists']['items'][0]['name'])
        self.artists = names

    def get_songs(self):
        songs = []
        for name in self.artists:
            endpoint = "https://api.spotify.com/v1/search?q=artist:%22{}%22%20year:2021&type=track&limit=20".format(
                name)
            response = requests.get(endpoint,
                                    headers={
                                        "Content-Type":
                                        "application/json",
                                        "Authorization":
                                        "Bearer {}".format(self.spotify_token)
                                    })
            for song in response.json()['tracks']['items']:
                if song['name'] not in list(map(lambda x: x['name'], songs)):
                    songs.append(song)
        return list(map(lambda x: x['uri'], songs))

    def populate(self):
        j = 0
        div = len(self.songs) // 100
        for i in range(div, len(self.songs) + 1, div):
            request_data = json.dumps(self.songs[j:i])
            endpoint = "https://api.spotify.com/v1/playlists/{}/tracks".format(
                self.playlist_id)
            response = requests.post(endpoint,
                                     data=request_data,
                                     headers={
                                         "Content-Type":
                                         "application/json",
                                         "Authorization":
                                         "Bearer {}".format(self.spotify_token)
                                     })
            j = i
        print(f"Response obtained {response.json()}")


if __name__ == "__main__":
    print("Starting playlist and populating... 🧞🎹")
    try:
        manager = Manager()
        manager.create_playlist()
        manager.get_artist_name()
        manager.get_songs()
        manager.populate()

    except Exception as e:
        print(f"Error ⁉️ {e}")
