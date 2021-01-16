#!/usr/bin/env python3
from __future__ import unicode_literals
import sys
import getopt
from dlmy import search
from dlmy import download
from youtube_search import YoutubeSearch as yt_search


class col:
    """
    Colors used to colorize text
    """
    blue = '\033[94m'
    ok = '\033[92m'
    warn = '\033[93m'
    fail = '\033[91m'
    end = '\033[0m'


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


def help_message():
    """
    Shows usage of the application
    """
    print("""

{}Usage:

    {}-h                      show help
    -t <spotify url>        download the url as mp3
    -t "track title"        download the title as mp3
    -l <spotify playlist>   download the url as mp3

{}Examples:

    {}dlmy -t "Travis Scott - Stargazing"
    dlmy -t https://open.spotify.com/track/7wBJfHzpfI3032CSD7CE2m
    dlmy -l https://open.spotify.com/playlist/37i9dQZF1DWUgX5cUT0GbU
{}
""".format(col.warn, col.ok, col.warn, col.ok, col.end))


def main():
    """
    Program starts here
    """
    try:
        options, remainder = getopt.getopt(
            sys.argv[1:], 'ht:l:', ['playlist', 'track', 'help'])

        for opt, arg in options:

            if opt in ("-h", "--help"):
                help_message()

            elif opt in ("-t", "--track"):

                if "https://spotify.com/track" in arg:
                    title = search.spotify_track(arg)
                elif "http" not in arg:
                    title = arg
                else:
                    print(f"{col.fail}Please provide a valid url!{col.end}")

                try:
                    results = yt_search(title).to_dict()
                    title = results[0]["title"]
                    url_suffix = results[0]["url_suffix"]

                    print(f'\n{col.blue}{title}' + col.end + "\n")

                    prompt = str(input(f"{col.ok}Is this correct? {col.warn}(Y/n){col.end}"))

                    if prompt in ("n", "N"):
                        sys.exit()
                    else:
                        download.download("https://youtube.com" + url_suffix, title)

                except IndexError:
                    print(f"{col.fail}Unable to find {col.blue}{title}{col.end}")

            elif opt in ("-l", "--playlist"):

                valid_url = "https://open.spotify.com/playlist"
                if valid_url in arg:

                    songs = search.spotify_playlist(arg)

                    print("")

                    for tag in songs:
                        title = search.spotify_track(tag["content"])
                        print(f"{col.blue}{title}{col.end}")

                    print("")

                    prompt = str(input(f"{col.ok}Is this correct? {col.warn}(Y/n){col.end}"))

                    if prompt in ("n", "N"):
                        sys.exit()

                    else:
                        print("")
                        for tag in songs:
                            title = search.spotify_track(tag["content"])
                            results = yt_search(title).to_dict()
                            url_suffix = results[0]["url_suffix"]

                            print(
                                f"{col.warn}Downloading: {col.blue}{results[0]['title']}{col.end}")

                            download.download("https://youtube.com" + url_suffix, title)

            else:
                help_message()

    except getopt.error:
        help_message()

    except KeyboardInterrupt:
        sys.exit()


if __name__ == "__main__":
    main()
