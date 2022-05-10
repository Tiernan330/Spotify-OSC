import urllib.request
import requests
from Refresh_Token import Refresh
from Spotify_OSC import SpotifyOSC, TrackInfo
from Texture import CreateTexture
from PIL import Image
from pprint import pprint
import urllib.request
import time


def call_refresh():
    refreshCaller = Refresh()
    spotify_token = refreshCaller.refresh()
    return spotify_token


# creates initial auth token
Spotify_Access_Token = call_refresh()
Spotify_Get_Current_Track_URL = 'https://api.spotify.com/v1/me/player/currently-playing'


def SpotifyInfo():
    global Spotify_Access_Token

    # ------------------------------------------------------------------------------------------------------------------
    def TrackPlaying(access_token):
        response = requests.get(Spotify_Get_Current_Track_URL, headers={"Authorization": f"Bearer {access_token}"})
        json_resp = response.json()
        is_Playing = json_resp['is_playing']
        return is_Playing

    # ------------------------------------------------------------------------------------------------------------------
    get_current_track = TrackInfo()
    OSC = SpotifyOSC()
    current_track_id = None
    while True:
        # Checks to see if the auth token is valid or needs to be refreshed
        try:
            response = requests.get(Spotify_Get_Current_Track_URL,
                                    headers={"Authorization": f"Bearer {Spotify_Access_Token}"})
            if response.status_code == 204:
                print("Must play music before activating for auth token")
                break
            json_resp = response.json()
            is_Playing = json_resp['is_playing']
        except KeyError:
            print("refreshing token...")
            Spotify_Access_Token = call_refresh()

        previousSong = current_track_id
        get_current_track.setToken(Spotify_Access_Token)
        current_track_info = get_current_track.getInfo()

        # creates png of the album art for use in the Texture.py
        urllib.request.urlretrieve(
            current_track_info["album art"],
            "album.png")
        img = Image.open("album.png")
        img.save("album.png")

        # Spotify is paused---------------------------------------------------------------------------------------------
        if current_track_info['id'] == current_track_id and TrackPlaying(Spotify_Access_Token) is False:
            OSC.sendData(0)
            current_track_id = None
            pprint('No song Playing')
            Texture = CreateTexture(current_track_info['name'], current_track_info['artists'],
                                    TrackPlaying(Spotify_Access_Token), current_track_info['shuffle'],
                                    current_track_info['repeat'], current_track_info['length'])
            Texture.createTexture()

        # --------------------------------------------------------------------------------------------------------------

        # Spotify is playing a Song and if its a different song
        if current_track_info['id'] != current_track_id and TrackPlaying(Spotify_Access_Token) is True:
            OSC.sendData(1)
            pprint(current_track_info, indent=4, )
            current_track_id = current_track_info['id']

            # Prints length of Song Name and previous and current song ID----
            if previousSong is None:
                print("No previous Song")
            else:
                print("previous song ID: " + previousSong)
            print("Current Song ID: " + current_track_id)
            # ---------------------------------------------------------------
            Texture = CreateTexture(current_track_info['name'], current_track_info['artists'],
                                    TrackPlaying(Spotify_Access_Token), current_track_info['shuffle'],
                                    current_track_info['repeat'], current_track_info['length'])
            Texture.createTexture()

        else:
            pass


        time.sleep(1)


if __name__ == '__main__':
    SpotifyInfo()
