#!/usr/bin/env python3
from __future__ import unicode_literals
import requests
import urllib.request
import json
import sys
import getopt
import youtube_dl
import time
import configparser
import os
import shutil
from bs4 import BeautifulSoup
from dlmy import search

# Initialize configparser
config = configparser.ConfigParser()

def get_config():
    """
    Get the configuration path and file.
    """

    user = os.getlogin()

    # Linux
    if os.name == "posix":
        # First try to locate XDG_CONFIG_HOME
        if os.environ["XDG_CONFIG_HOME"]:
            config_path = os.environ["XDG_CONFIG_HOME"] + "/dlmy/"
        # Fallback to home env var
        else:
            config_path = os.environ["HOME"] + "/.config/dlmy/"

    # Windows
    elif os.name == "nt":
        # First try to locate appdata
        if os.environ["APPDATA"]:
            config_path = os.environ["APPDATA"] + "\dlmy\\"
        # If fails, fallback to manually locating appdata
        else:
            config_path = "C:\\Users\\" + user + "\AppData\Roaming\dlmy\\"

    # Create directories
    if not os.path.exists(config_path):
        os.makedirs(config_path)

    config_file = config_path + "config.ini"
    example_config = os.getcwd() + "/config_example.ini"

    if not os.path.isfile(config_file):
        shutil.copy(example_config, config_path)
        os.rename(config_path + "config_example.ini", config_file)

    return config_file

# Read config file
config.read(get_config())

class col:
    blue = '\033[94m'
    ok = '\033[92m'
    warn = '\033[93m'
    fail = '\033[91m'
    end = '\033[0m'

def spotify_track(url):
    """
    Get information about a track from Spotify
    Returns: final song name
    """

    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")
    title = soup.find("meta", property="og:title")
    title = title["content"]
    artist = soup.find("meta", property="twitter:audio:artist_name")
    artist = artist["content"]
    song_name = str(artist + " - " + title)

    return song_name

def spotify_playlist(url):
    """
    Get every song from a spotify playlist
    Returns: list of songs
    """

    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    songs = soup.find_all('meta', property="music:song")

    return songs


# Youtube Download options
ydl_opts = {
    'format': 'bestaudio/best',
    'writethumbnail': True,
    'noplaylist': True,
    'continue_dl': True,
    'restrictfilenames': True,
    'quiet': True,
    'no_warnings': True,
    'postprocessors': [
        {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        },
        {'key': 'EmbedThumbnail'},
        {'key': 'FFmpegMetadata'},
    ],
}

argumentList = sys.argv[1:]
options = "ht:l:"
long_options = ["help", "track", "playlist"]


def help():
    print("""
DLMY
Usage:
    -h                      show help
    -t <spotify url>        download the url as mp3
    -t "track title"        download the title as mp3
    -l <spotify playlist>   download the url as mp3
""")

def main():
    try:
        # Parsing arguments
        arguments, values = getopt.getopt(argumentList, options, long_options)

        for currentArgument, currentValue in arguments:

            if currentArgument in ("-h", "--help"):
                help()

            elif currentArgument in ("-t", "--track"):

                if "https://spotify.com/track" in currentValue:
                    title = spotify_track(currentValue)
                elif "http" not in currentValue:
                    title = currentValue
                else:
                    print(f"{col.fail}Please provide a valid url!{col.end}")

                try:
                    results = yt_search(title).to_dict()
                    print(f'\n{col.blue}{results[0]["title"]}' + col.end + "\n")
                    url_suffix = results[0]["url_suffix"]

                    prompt = str(input(f"{col.ok}Is this correct? {col.warn}(Y/n){col.end}"))

                    if prompt == "n" or prompt == "N":
                        exit(1)
                    else:
                        print("")
                        print(f"{col.warn}Downloading: {col.blue}{results[0]['title']}{col.end}")
                        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                            ydl.download(["http://www.youtube.com" + url_suffix])

                except IndexError:
                    print(f"{col.fail}Unable to find {col.blue}{title}{col.end}")

            elif currentArgument in ("-l", "--playlist"):

                valid_url = "https://open.spotify.com/playlist"
                if valid_url in currentValue:

                    songs = spotify_playlist(currentValue)

                    print("")

                    for tag in songs:
                        title = spotify_track(tag["content"])
                        print(f"{col.blue}{title}{col.end}")

                    print("")

                    prompt = str(input(f"{col.ok}Is this correct? {col.warn}(Y/n){col.end}"))

                    if prompt == "n" or prompt == "N":
                        exit(1)

                    else:
                        print("")
                        for tag in songs:
                            title = spotify_track(tag["content"])
                            results = yt_search(title).to_dict()
                            url_suffix = results[0]["url_suffix"]
                            print(f"{col.warn}Downloading: {col.blue}{results[0]['title']}{col.end}")
                            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                                ydl.download(["http://www.youtube.com" + url_suffix])

            else:
                help()

    except getopt.error:
        help()

    except KeyboardInterrupt:
        exit(1)

if __name__ == "__main__":
    main()
