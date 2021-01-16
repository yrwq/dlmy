#!/usr/bin/env python3
from __future__ import unicode_literals
from bs4 import BeautifulSoup
import requests


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
