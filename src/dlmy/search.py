#!/usr/bin/env python3
from __future__ import unicode_literals
from bs4 import BeautifulSoup
import requests
import urllib.request
import json


class yt_search:
    """
    Search on youtube with a song's title.
    Returns: youtube url, youtube title in a dict
    """
    def __init__(self, search_terms: str):
        self.search_terms = search_terms
        self.videos = self.search()

    def search(self):
        encoded_search = urllib.parse.quote(self.search_terms)
        BASE_URL = "https://youtube.com"
        url = f"{BASE_URL}/results?search_query={encoded_search}"
        response = requests.get(url).text
        while "ytInitialData" not in response:
            response = requests.get(url).text
        results = self.parse_html(response)
        return results

    def parse_html(self, response):
        results = []
        start = (
            response.index("ytInitialData") + len("ytInitialData") + 3
        )
        end = response.index("};", start) + 1
        json_str = response[start:end]
        data = json.loads(json_str)

        videos = data["contents"]
        ["twoColumnSearchResultsRenderer"]
        ["primaryContents"]["sectionListRenderer"]
        ["contents"][0]["itemSectionRenderer"]["contents"]

        for video in videos:
            res = {}
            if "videoRenderer" in video.keys():
                video_data = video.get("videoRenderer", {})

                res["title"] = video_data.get
                ("title", {}).get("runs", [[{}]])[0].get
                ("text", None)

                res["url_suffix"] = video_data.get
                ("navigationEndpoint",
                 {}).get("commandMetadata",
                         {}).get("webCommandMetadata",
                                 {}).get("url", None)

                results.append(res)
        return results

    def to_dict(self):
        return self.videos


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
