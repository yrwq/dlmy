#!/usr/bin/env python3
from __future__ import unicode_literals
import requests
import sys
import getopt
import youtube_dl
from search import yt_search
from bs4 import BeautifulSoup


def spotify_track(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")
    title = soup.find("meta", property="og:title")
    title = title["content"]
    artist = soup.find("meta", property="twitter:audio:artist_name")
    artist = artist["content"]
    song_name = str(artist + " - " + title)

    return song_name


def spotify_playlist(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    songs = soup.find_all('meta', property="music:song")

    return songs


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


try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)

    # checking each argument
    for currentArgument, currentValue in arguments:

        if currentArgument in ("-h", "--help"):
            help()

        elif currentArgument in ("-t", "--track"):

            # Get title if spotify link given
            if "https://spotify.com/track" in currentValue:
                title = spotify_track(currentValue)
            else:
                title = currentValue

            try:
                results = yt_search(title).to_dict()
                print(results[0]["title"])
                url_suffix = results[0]["url_suffix"]

                prompt = str(input("Is this correct? (Y/n)"))
                if prompt == "n" or prompt == "N":
                    exit(1)
                else:
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download(["http://www.youtube.com" + url_suffix])

            except:
                print("Unable to find " + title)
                print("Please try a longer title!")

        elif currentArgument in ("-l", "--playlist"):

            valid_url = "https://open.spotify.com/playlist"
            if valid_url in currentValue:

                songs = spotify_playlist(currentValue)
                print("")
                for tag in songs:
                    print(spotify_track(tag["content"]))

                print("")

                prompt = str(input("Is this correct? (Y/n)"))
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
