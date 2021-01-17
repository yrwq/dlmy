#!/usr/bin/env python3
"""
Download from youtube using youtube_dl
"""
import youtube_dl
import os
import re
from dlmy import configuration


def download(url, title):
    """
    Download the music from YouTube,
    and move it to the download direcotry
    """
    norm_title = title
    # Remove extra characters which can fuck up the final path
    title = re.sub("   ", "", title)
    title = re.sub("  ", "", title)
    title = re.sub(" ", "_", title)
    title = re.sub("/", "", title)

    if not title.endswith("mp3"):
        title += '.' + "mp3"

    dw_dir = configuration.config["DEFAULT"]["download_dir"]

    name = os.path.join(dw_dir, title)
    norm_name = os.path.join(dw_dir, norm_title)

    if configuration.config["DEFAULT"]["ffmpeg"] == "True":
        ydl_opts = {
            'format': 'bestaudio/best',
            'writethumbnail': True,
            'noplaylist': True,
            'restrictfilenames': True,
            'outtmpl': norm_name,
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

    return 0
