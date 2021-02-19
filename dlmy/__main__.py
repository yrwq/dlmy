#!/usr/bin/env python3
"""
Yet another Spotify downloader
"""
from __future__ import unicode_literals
import sys
import getopt
import json
from colorama import init
from dlmy import search
from dlmy import download


init()  # colorama


class col:
    """
    Colors used to colorize text
    """
    blue = '\033[94m'
    ok = '\033[92m'
    warn = '\033[93m'
    fail = '\033[91m'
    end = '\033[0m'


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
        options, remainder = getopt.getopt(sys.argv[1:], 'ht:l:', ['playlist', 'track', 'help'])

        for opt, arg in options:

            if opt in ("-h", "--help"):
                help_message()

            elif opt in ("-t", "--track"):

                valid_url = "https://open.spotify.com/track"

                if valid_url in arg:
                    whole_title = search.spotify_track(arg)
                    title = f"{whole_title[0]} - {whole_title[1]}"
                elif "http" not in arg:
                    title = arg
                else:
                    print(f"{col.fail}❌ {col.warn}Please provide a valid url!{col.end}")

                try:
                    results = search.yt_search(title)
                    results = json.loads(results)

                    title = results["videos"][0]["title"]
                    url_suffix = results["videos"][0]["url_suffix"]

                    print(f'\n{col.blue} {title}' + col.end + "\n")

                    prompt = str(input(f"{col.ok}✔ Is this correct? {col.warn}(Y/n){col.end}"))

                    if prompt in ("n", "N"):
                        sys.exit()
                    else:
                        print("")
                        download.download("https://youtube.com" + url_suffix, title)

                except IndexError:
                    print(f"{col.fail}Unable to find {col.blue}{title}{col.end}")

            elif opt in ("-l", "--playlist"):

                valid_url = "https://open.spotify.com/playlist"

                if valid_url in arg:

                    songs = search.spotify_playlist(arg)
                    album_title = songs[1]

                    print(f"\n{col.ok} Contents of: {col.warn}{album_title}{col.end}\n")

                    for tag in songs[0]:
                        try:
                            title = search.spotify_track(tag["content"])
                            whole_title = f"{title[0]} - {title[1]}"
                            print(f"{col.blue} {whole_title}{col.end}")
                        except IndexError:
                            print(f"\n{col.fail}❌Can't find all song's!")
                            sys.exit()

                    print("")

                    prompt = str(input(f"{col.ok} Is this correct? {col.warn}(Y/n){col.end}"))

                    if prompt in ("n", "N"):
                        sys.exit()

                    else:
                        print("")
                        for tag in songs[0]:
                            title = search.spotify_track(tag["content"])
                            whole_title = f"{title[0]} - {title[1]}"
                            results = search.yt_search(whole_title)
                            results = json.loads(results)
                            url_suffix = results["videos"][0]["url_suffix"]
                            print(f"{col.ok} Downloading: {col.blue}{whole_title}")
                            download.download("https://youtube.com" + url_suffix, whole_title)

            else:
                help_message()

    except getopt.error:
        help_message()

    except KeyboardInterrupt:
        sys.exit()


if __name__ == "__main__":
    main()
