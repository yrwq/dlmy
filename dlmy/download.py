#!/usr/bin/env python3
import youtube_dl
import os
import re
import music_tag
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

    whole = search.spotify_track(url)
    artist = whole[0]
    track = whole[1]

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

    f = music_tag.load_file(name)
    f["title"] = track
    f["artist"] = artist
    f.save()

    return 0
