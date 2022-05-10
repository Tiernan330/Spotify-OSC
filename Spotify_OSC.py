import requests
from pythonosc import udp_client



class SpotifyOSC:
    def __init__(self):
        self.osc_ip = "127.0.0.1"
        self.osc_port = 9000
        self.osc_client = udp_client.SimpleUDPClient(self.osc_ip, self.osc_port)
        self.Music = "/avatar/parameters/Music"

    def sendData(self, data):
        self.osc_client.send_message(self.Music, data)


class TrackInfo:
    def __init__(self):
        self.token = None
        self.Spotify_Get_Playback_State = 'https://api.spotify.com/v1/me/player'

    def setToken(self, x):
        self.token = x

    def getToken(self):
        return self.token

    def getPS(self):
        return self.Spotify_Get_Playback_State


    def getInfo(self):
        Spotify_Get_Playback_State = self.getPS()

        Spotify_Access_Token = self.getToken()

        response = requests.get(Spotify_Get_Playback_State,
                            headers={"Content-Type": "application/json",
                                     "Authorization": "Bearer {}".format(Spotify_Access_Token)})
        json_resp = response.json()

        track_id = json_resp['item']['id']
        track_name = json_resp['item']['name']
        artists = [artist for artist in json_resp['item']['artists']]
        get_art = [image for image in json_resp['item']['album']['images'][0]['url']]
        link = json_resp['item']['external_urls']['spotify']
        artists_names = ', '.join([artist['name'] for artist in artists])
        art = ''.join([str(item) for item in get_art])
        shuffle = json_resp['shuffle_state']
        repeat = json_resp['repeat_state']
        length = json_resp["item"]["duration_ms"]

        current_track_info = \
            {
                "id": track_id,
                "name": track_name,
                "artists": artists_names,
                "album art": art,
                "link": link,
                "shuffle": shuffle,
                "repeat": repeat,
                "length": length
            }
        return current_track_info



