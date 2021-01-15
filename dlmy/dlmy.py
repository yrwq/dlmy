#!/usr/bin/env python3
from __future__ import unicode_literals
import requests
import sys
import getopt
import youtube_dl
import time
from search import yt_search
from colors import col
from bs4 import BeautifulSoup

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

def prompt(ask):
    return str(input(f"{col.ok}{ask} {col.warn}(Y/n){col.end}"))

# Youtube Download options
ydl_opts = {
    'format': 'bestaudio/best',
    'writethumbnail': True,
    'noplaylist': True,
    'continue_dl': True,
    'restrictfilenames': True,
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

                    prompt = prompt("Is this correct?")

                    if prompt == "n" or prompt == "N":
                        exit(1)
                    else:
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

                    prompt = prompt("Is this correct?")

                    if prompt == "n" or prompt == "N":
                        exit(1)

                    else:
                        for tag in songs:
                            title = spotify_track(tag["content"])
                            results = yt_search(title).to_dict()
                            url_suffix = results[0]["url_suffix"]
                            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                                ydl.download(["http://www.youtube.com" + url_suffix])

            else:
                help()

    except getopt.error:
        help()

    except KeyboardInterrupt:
        exit(1)

