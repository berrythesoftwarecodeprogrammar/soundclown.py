# soundclown.py
python soundcloud downloader

# requirements
python
python requests (pip install requests)

# about
i had a python soundcloud downloader which i found online a while ago and modified a bunch to suit my needs but recently it started failing on some songs so ive decided to rewrite it and put it on github while i work on it.

# problems/todo
- its UNFINISHED. havent added in most of the error handling and stuff yet, i just finished writing it. it works on songs without any issues
- the reason my old script started failing is because now some songs have 'streamable=False' in the api response for some reason. i found that another request is required for these songs to retrieve the stream mp3. but im using keys which i found my browser using on soundcloud.com. i dont know yet how permanent these keys are and if they work with every song. this needs to be investigated
- id3v2 tag support to automatically do the stuff i currently do in mp3tag

# how it works / what it does
1. supply a sound url (no playlist support yet). "python soundclown.py https://soundcloud.com/artist/sound"
2. it checks for stream and download urls
3. saves album art, stream mp3, and original audio file if available

# tested on
Python 2.7.10
Windows 7 x64

#changeblog
##v20151114-2155##
- forgot to remove an unnecessary print
##v20151114-2146##
- only download original artwork if its available (it was downloading an empty file when 404)
##v20151114-1853##
- first release
