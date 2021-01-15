from distutils.core import setup
setup(
  name = 'dlmy',
  packages = ['dlmy'],
  version = '0.3',
  license='MIT',
  description = 'Yet another Spotify Downloader',
  author = 'Inhof Dávid',
  author_email = 'yrwqid@gmail.com',
  url = 'https://github.com/yrwq/dlmy',
  download_url = 'https://github.com/yrwq/dlmy/archive/0.3.tar.gz',
  keywords = ['spotify', 'youtube_dl', 'spotipy'],
  install_requires=[
          'requests',
          'youtube_dl',
          'beautifulsoup4',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
