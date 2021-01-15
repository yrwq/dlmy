## Dlmy

### Introduction

Yet another Spotify Downloader omg. 🤐

Dlmy uses the given Spotify Track's metadata tags, to extract information about the music.

After extracting information, the music is downloaded from YouTube using [youtube_dl](https://github.com/ytdl-org/youtube-dl).

Any contributions are welcomed!

### Features

- [x] Download single tracks using a Spotify url
- [x] Download single tracks using a search query
- [x] Download whole Spotify playlists

### Installation

#### Packages

##### Pip

```bash
pip install dlmy
```

##### Aur

In progress ...

### Usage

```bash
dlmy -t "title of the track"        download a track using query
dlmy -t <url>                       download the given track
dlmy -l <url>                       download a whole playlist
```

