import requests
import json
from secrets import secrets

class CreateAndPopulate:
    
    def __init__(self):
        self.client_id = secrets["client_id"] 
        self.client_secret = secrets["client_secret"]
        self.spotify_token = secrets["access_token"]
        self.scope = 'playlist-modify-public'
        

    def create_playlist(self):
        r = json.dumps({
            "name":"NANAANANAN",
            "description": "Top 5 tracks of each of my top and most streamed artists",
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
    
    def get_artist_id(self, artists):
        ids = []
        for artist in artists:
            query= "https://api.spotify.com/v1/search?query=%3A{}&type=artist&limit=1".format(artist)
            response = requests.get(
                query,
                headers={
                    "Content-Type":"application/json",
                    "Authorization": "Bearer {}".format(self.spotify_token)
                }
            )
            ids.append(response.json()['artists']['items'][0]['id'])   
        return ids

    def get_top5_songs(self, ids):
        tops = []
        for id in ids:
            endpoint = "https://api.spotify.com/v1/artists/{}/top-tracks?country=US".format(id)
            response = requests.get(
                endpoint,
                headers={
                    "Content-Type":"application/json",
                    "Authorization": "Bearer {}".format(self.spotify_token)
                }
            )
            tops.extend(list(map(lambda x: x['uri'],response.json()['tracks'])))
        return tops

    def populate(self, top5):
        j = 0
        div = len(top5)//100
        for i in range(div, len(top5)+1, div):
            request_data = json.dumps(top5[j:i])
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
    with open("artists.json", "r") as f:
        artists = json.load(f)['artists']
        main.populate(main.get_top5_songs(main.get_artist_id(artists)))