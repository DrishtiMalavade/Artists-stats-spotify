from dotenv import load_dotenv
import os
import requests
import json
import colorama 
from colorama import Fore, Style

load_dotenv()
colorama.init()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "client_credentials"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(url, data=payload, headers=headers, auth=auth)
    return response.json().get("access_token")

def auth_header(token):
    return {
        "Authorization": f"Bearer {token}"
    }   

def get_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    query_url = url + query
    result = requests.get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print(f"No artist found for {artist_name}")
        return None
    return json_result[0]

def get_songs_artists(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = auth_header(token)
    
    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status()
        json_result = result.json()
        songs = json_result.get("tracks", [])
        return songs
    except requests.exceptions.RequestException as e:
        print(f"Error fetching top tracks: {e}")
        print(result.text)  # Print the content of the response
        return []

def get_albums(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums?market=US"
    headers = auth_header(token)
    
    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status()
        json_result = result.json()
        albums = json_result.get("items", [])
        return albums
    except requests.exceptions.RequestException as e:
        print(f"Error fetching albums: {e}")
        print(result.text)  # Print the content of the response
        return []



def get_similar_artists(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/related-artists"
    headers = auth_header(token)

    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status()
        json_result = result.json()
        similar_artists = json_result.get("artists", [])
        return similar_artists
    except requests.exceptions.RequestException as e:
        print(f"Error fetching similar artists: {e}")
        print(result.text)  # Print the content of the response
        return []
    
    
def main():
    print(colorama.ansi.clear_screen())
    token = get_token()

    artist_name = input("Type in the artist name, please: ")
    artist = get_artist(token, artist_name)

    if artist:
        print(Fore.CYAN + f"Top Ten Songs by {artist['name']}:")
        artist_id = artist["id"]
        songs = get_songs_artists(token, artist_id)

        # Display the top ten songs
        for idx, song in enumerate(songs[:10]):
            print( Fore.GREEN + f"{idx + 1}. {song['name']}")

        print(Fore.CYAN + "\nTop Three Albums:")
        albums = get_albums(token, artist_id)

        # Display the top ten albums
        for idx, album in enumerate(albums[:3]):
            print(Fore.YELLOW + f"{idx + 1}. {album['name']}")

        print(Fore.CYAN + "\nSimilar Artists:")
        similar_artists = get_similar_artists(token, artist_id)

        # Display similar artists
        for idx, similar_artist in enumerate(similar_artists[:5]):
            print(Fore.MAGENTA + f"{idx + 1}. {similar_artist['name']}")
    else:
        print(f"No artist found for {artist_name}")

main()
