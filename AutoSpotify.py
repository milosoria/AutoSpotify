import requests
import json

class CreateAndPopulate:
    
    def __init__(self):
        with open("secrets.json","r") as f:
            self.json = json.load(f)
        self.client_id = self.json["config"]["client_id"] 
        self.client_secret = self.json["config"]["client_secret"]
        self.spotify_token = self.json["config"]["access_token"]
        self.scope = 'playlist-modify-public'

    def create_playlist(self):
        r = json.dumps({
            "name":"NANAANANAN",
            "description": "tracks released on 2020-2021",
            "public": True
        })
        endpoint = "https://api.spotify.com/v1/users/{}/playlists".format(self.client_id )
        response = requests.post(
            endpoint,
            data=r,
            headers={
                "Content-Type":"application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        self.playlist_id = response.json()["id"]
    
    def get_artist_name(self):
        names = []
        for artist in self.json["artists"]:
            query= "https://api.spotify.com/v1/search?query=%3A{}&type=artist&limit=1".format(artist)
            response = requests.get(
                query,
                headers={
                    "Content-Type":"application/json",
                    "Authorization": "Bearer {}".format(self.spotify_token)
                }
            )
            names.append(response.json()['artists']['items'][0]['name'])   
        return names

    def get_songs(self, names):
        songs = []
        for name in names:
            endpoint = "https://api.spotify.com/v1/search?q=artist:%22{}%22%20year:2020-2021&type=track&limit=20".format(name)
            response = requests.get(
                endpoint,
                headers={
                    "Content-Type":"application/json",
                    "Authorization": "Bearer {}".format(self.spotify_token)
                }
            )
            songs.extend(list(map(lambda x: x['uri'],response.json()['tracks']['items'])))
        return songs

    def populate(self, songs):
        j = 0
        div = len(songs)//100
        for i in range(div, len(songs)+1, div):
            request_data = json.dumps(songs[j:i])
            endpoint = "https://api.spotify.com/v1/playlists/{}/tracks".format(self.playlist_id)
            response = requests.post(
                    endpoint,
                    data=request_data,
                    headers={
                        "Content-Type":"application/json",
                        "Authorization": "Bearer {}".format(self.spotify_token)
                    }
                )
            j = i
        return response.json()

if __name__ == "__main__":
    main = CreateAndPopulate()
    main.create_playlist()
    main.populate(main.get_songs(main.get_artist_name()))