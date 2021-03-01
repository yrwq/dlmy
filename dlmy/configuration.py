#!/usr/bin/env python3
"""
Parse configuration file
"""
import configparser
import os
import shutil

config = configparser.ConfigParser()

def get_config():
    """
    Get the configuration path and file.
    """

    user = os.getlogin()

    # Linux
    if os.name == "posix":
        # First try to locate XDG_CONFIG_HOME
        if os.environ["XDG_CONFIG_HOME"]:
            config_path = os.environ["XDG_CONFIG_HOME"] + "/dlmy/"
        # Fallback to home env var
        else:
            config_path = os.environ["HOME"] + "/.config/dlmy/"

    # Windows
    elif os.name == "nt":
        # First try to locate appdata
        if os.environ["APPDATA"]:
            config_path = os.environ["APPDATA"] + "/dlmy/"
        # If fails, fallback to manually locating appdata
        else:
            config_path = "C:/Users/" + user + "/AppData/Roaming/dlmy/"

    # Create directories
    if not os.path.exists(config_path):
        os.makedirs(config_path)

    config_file = config_path + "config.ini"

    if not os.path.isfile(config_file):
        f = open(config_file, "w")
        f.write("""
[DEFAULT]
music_dir = ~/Music
ffmpeg = True
                """)
        f.close()

    return config_file


config_file = get_config()
config.read(config_file)
