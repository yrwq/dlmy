#!/usr/bin/env python3
"""
Search on Spotify and YouTube
"""
from __future__ import unicode_literals
from bs4 import BeautifulSoup
import json
import requests
import urllib.request


def spotify_track(url):
    """
    Get information about a track from Spotify
    Returns: final song name
    """

    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")

    title = soup.find("meta", property="og:title")
    artist = soup.find("meta", property="twitter:audio:artist_name")

    title = title["content"]
    artist = artist["content"]

    song_name = [artist, title]

    return song_name


def spotify_playlist(url):
    """
    Get every song from a spotify playlist
    Returns: list of songs
    """

    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    songs = soup.find_all('meta', property="music:song")
    title = soup.find('meta', property="twitter:title")
    title = title["content"]

    data = [songs, title]

    return data


def parse_html(response):
    """
    """
    results = []
    start = (response.index("ytInitialData") + len("ytInitialData") + 3)
    end = response.index("};", start) + 1
    json_str = response[start:end]
    data = json.loads(json_str)

    videos = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]

    for video in videos:
        res = {}
        if "videoRenderer" in video.keys():
            video_data = video.get("videoRenderer", {})
            res["title"] = video_data.get("title", {}).get("runs", [[{}]])[0].get("text", None)
            res["url_suffix"] = video_data.get("navigationEndpoint", {}).get("commandMetadata", {}).get("webCommandMetadata", {}).get("url", None)
            results.append(res)

    results = json.dumps({"videos": results})
    return results


def yt_search(query):
    """
    Search on youtube using a query
    Returns: video ids
    """

    encoded_search = urllib.parse.quote(query)
    BASE_URL = "https://youtube.com"
    url = f"{BASE_URL}/results?search_query={encoded_search}"
    response = requests.get(url).text
    while "ytInitialData" not in response:
        response = requests.get(url).text
    results = parse_html(response)

    return results
