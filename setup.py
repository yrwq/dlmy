import setuptools
import dlmy

with open("README.md", 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='dlmy',
    version='1.25',
    author='Inhof Dávid',
    author_email='yrwqid@gmail.com',
    description='Yet another Spotify Download.',
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/yrwq/dlmy",
    packages=["dlmy"],
    entry_points={"console_scripts": ["dlmy=dlmy.__main__:main"]},
    install_requires=[
        "beautifulsoup4",
        "lmxl",
        "youtube_dl",
        "requests"
    ],
    python_requires='>=3.6',
)
