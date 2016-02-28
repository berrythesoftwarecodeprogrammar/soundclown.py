# soundclown.py
python soundcloud downloader

# usage
`python soundclown.py <soundcloud-url>`

# requirements
python  
python requests (`pip install requests`)

# about
i had a python soundcloud downloader which i found online a while ago and modified a bunch to suit my needs but recently it started failing on some songs so ive decided to rewrite it and put it on github while i work on it.

# todo
- id3v2 tag support to automatically do the stuff i currently do in mp3tag

# how it works / what it does
1. supply a sound url (no playlist support yet). "python soundclown.py https://soundcloud.com/artist/sound"
2. it checks for stream and download urls
3. saves album art, stream mp3, and original audio file if available

# tested on
Python 2.7.10
Windows 7 x64

#changeblog
v20151212-2014
- fixed crashing when no artwork available

v20151127-0221
- fixed not downloading original file
- print original filename

v20151114-2226
- dont print titles and artists in unicode because it breaks (fuck python utf8). still saves as utf8

v20151114-2155
- forgot to remove an unnecessary print

v20151114-2146
- only download original artwork if its available (it was downloading an empty file when 404)

v20151114-1853
- first release
