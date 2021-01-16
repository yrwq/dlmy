#!/usr/bin/env python3
from sys import stdout
from downloader_cli.download import Download
import youtube_dl
import os
import configuration


def progress_handler(d):
    d_obj = Download('', '')

    if d['status'] == 'downloading':
        length = d_obj._get_terminal_length()
        time_left = d['eta']
        f_size_disp, dw_unit = d_obj._format_size(d['downloaded_bytes'])

        # Total bytes might not be always passed, sometimes
        # total_bytes_estimate is passed
        try:
            total_bytes = d['total_bytes']
        except KeyError:
            total_bytes = d['total_bytes_estimate']

        percent = d['downloaded_bytes'] / total_bytes * 100
        speed, s_unit, time_left, time_unit = d_obj._get_speed_n_time(d['downloaded_bytes'], 0, cur_time=d['elapsed'] - 6)

        status = r"%-7s" % ("%s %s" % (round(f_size_disp), dw_unit))
        if d['speed'] is not None:
            speed, s_unit = d_obj._format_speed(d['speed'] / 1000)
            status += r"| %-3s " % ("%s %s" % (round(speed), s_unit))

        status += r"|| ETA: %-4s " % ("%s %s" % (round(time_left), time_unit))

        status = d_obj._get_bar(status, length, percent)
        status += r" %-4s" % ("{}%".format(round(percent)))

        stdout.write('\r')
        stdout.write(status)
        stdout.flush()


def download_using_yt(link, proxy, song_name, datatype, no_progress=False):

    ydl_opts = {
        'quiet': True,
        'outtmpl': song_name,
        'format': "bestaudio/best",
        'nocheckcertificate': True,
        'source_address': '0.0.0.0'
    }

    if not no_progress:
        ydl_opts['progress_hooks'] = [progress_handler]

    if proxy is not None:
        ydl_opts['proxy'] = proxy

    ydl = youtube_dl.YoutubeDL(ydl_opts)

    ydl.download([link])

    return 0


def download(value, song_name, proxy=None, datatype='mp3', no_progress=False):

    print("Downloading: {}".format(song_name))

    if datatype == "mp3" and not song_name.endswith(datatype):
        song_name += '.' + datatype

    dw_dir = configuration.config["DEFAULT"]["download_dir"]

    name = os.path.join(dw_dir, song_name)

    # Start downloading the song
    status = download_using_yt(value, proxy, name, datatype, no_progress)

    if status == 0:
        return name
    else:
        return status
