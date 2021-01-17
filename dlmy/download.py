#!/usr/bin/env python3
import youtube_dl
import os
import re
from mutagen.mp3 import MP3
from dlmy import search
from dlmy import configuration


def download(url, title):
    """
    Download the music from YouTube,
    and move it to the download direcotry
    """

    # Remove extra characters which can fuck up the final path
    title = re.sub("   ", "", title)
    title = re.sub("  ", "", title)
    title = re.sub(" ", "_", title)
    title = re.sub("/", "", title)

    if not title.endswith("mp3"):
        title += '.' + "mp3"

    dw_dir = configuration.config["DEFAULT"]["download_dir"]

    name = os.path.join(dw_dir, title)

    if configuration.config["DEFAULT"]["ffmpeg"] == "True":
        ydl_opts = {
            'format': 'bestaudio/best',
            'writethumbnail': True,
            'noplaylist': True,
            'restrictfilenames': True,
            'outtmpl': name,
            'continue_dl': True,
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
    else:
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'restrictfilenames': True,
            'outtmpl': name,
            'continue_dl': True,
            'quiet': True,
            'no_warnings': True,
        }

    ydl = youtube_dl.YoutubeDL(ydl_opts)

    ydl.download([url])

    whole_title = search.spotify_track(url)
    artist = whole_title[0]
    title = whole_title[1]

    tag(name, artist, title)

    return 0


def tag(file, artist, title):
    """
    Tag an MP3 file with the corresponding metadata
    """

    audio = MP3(file)
    audio["artist"] = artist
    audio["title"] = title
    audio.save()
