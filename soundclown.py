#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# `soundclown.py' v20151114-2155
# (c) brr [berr.yt]
#
# shoutz 2 whoever's original code helped write this. some of their
# stuff is still in here like the save() and report() functions
#
##

import sys, re, time, requests, urllib, urllib2

try:
	url = sys.argv[1]
except:
	print "[!] No url given."
	sys.exit(1)

dir = "Z:\\_Dlz\\_sc\\"
clientKey = "1c559e20bf7b3d5508181214ed9d6b0e" #1c559e20bf7b3d5508181214ed9d6b0e = soundcloud web
streamKey = "02gUJC0hH2ct1EGOcYXQIzRFU91c72Ea" #02gUJC0hH2ct1EGOcYXQIzRFU91c72Ea = soundcloud web
ver = "bf6f75f" #bf6f75f = soundcloud web (not sure how important this is)

class Error(Exception):
	pass

class sound:
	def __init__(self, url):
		self.download_progress = 0
		self.current_time = time.time()
		self.downloadable = False
		self.streamable = False
		self.ID = ''
		self.streamUrl = ''
		self.downloadUrl = ''
		self.artworkOrig = ''
		self.artwork500 = ''
		self.url = self.parseUrl(url)
		self.title = u''
		self.downloadFilename = ''
		self.streamFilename = ''
		self.userName = ''
		self.userDisplay = ''
		self.getInfo()
	
	def parseUrl(self, url):
		print '[!] Parsing URL...'
		r = re.search("(https?:\/\/soundcloud\.com/[^\/]+/[^\/#&\?]+)",url)
		if r is None:
			raise Error("No valid Soundcloud URL given.")
		else:
			print '    done'
			return r.group(0)
	
	def info(self):
		table = []
		max1 = 0
		max2 = 0
		table.append(('URL',self.url))
		table.append(('ID',str(self.ID)))
		table.append(('Artist (display)',self.userDisplay))
		table.append(('Artist (username)',self.userName))
		table.append(('Title',self.title))
		table.append(('',''))
		table.append(('Artwork (500x500)',self.artwork500))
		if self.artworkOrig != '':
			table.append(('Artwork (Original)',self.artworkOrig))
		if self.streamable:
			table.append(('Stream URL',self.streamUrl))
		else:
			table.append(('Streamable','False'))
		if self.downloadable:
			table.append(('Download URL',self.downloadUrl))
		else:
			table.append(('Downloadable','False'))
		for i in range(len(table)):
			if len(table[i][0]) > max1:
				max1 = len(table[i][0])
			if len(table[i][1]) > max2:
				max2 = len(table[i][1])
		for i in range(len(table)):
			if table[i] != ('',''):
				table[i] = '    '+table[i][0]+((max1-len(table[i][0]))*' ')+' | '+table[i][1]
			else:
				table[i] = ((max1+max1+8)*'-')
		table.insert(0,((max1+max1+8)*'-'))
		table.append(((max1+max1+8)*'-'))
		print '[!] Showing info...'
		for t in table:
			print t
	
	def generateFilename(self): # the filename used for artwork and stream mp3
		f = self.userDisplay+' - '+self.title # characters replaced for windows
		f = re.sub('<', '[', f)
		f = re.sub('>', ']', f)
		f = re.sub('\:', ';', f)
		f = re.sub('"', '\'', f)
		f = re.sub('\\\\', '_', f)
		f = re.sub('\/', '_', f)
		f = re.sub('\|', '_', f)
		f = re.sub('\?', '!', f)
		f = re.sub('[*]', '_', f)
		return f
	
	def getInfo(self):
		print '[!] Retrieving data...'
		r = requests.get("https://api.soundcloud.com/resolve.json?url={0}&client_id={1}".format(self.url, clientKey))
		track = r.json()
		print '    done'
		self.title = track['title']
		self.ID = track['id']
		self.artwork500 = track['artwork_url'].replace('-large','-t500x500')
		self.artworkOrig = track['artwork_url'].replace('-large','-original')
		print '[!] Checking for original artwork...'
		r = urllib2.Request(self.artworkOrig)
		r.get_method = lambda : 'HEAD'
		try:
			r = urllib2.urlopen(r)
			print '    found'
		except urllib2.HTTPError:
			self.artworkOrig = ''
			print '    not found'
		self.userName = track['user']['permalink']
		self.userDisplay = track['user']['username']
		self.url = track['permalink_url']
		self.streamFilename = self.generateFilename()
		if track['streamable']:
			self.streamable = True
			self.streamUrl = "{0}?client_id={1}".format(track['stream_url'], clientKey)
		else:
			print '[!] Sound marked as unstreamable. Finding stream URL...'
			r = requests.get("https://api.soundcloud.com/i1/tracks/{0}/streams?client_id={1}&app_version={2}".format(self.ID, streamKey, ver))
			stream = r.json()
			self.streamable = True
			try:
				self.streamUrl = stream['http_mp3_128_url']
				print '    done'
			except KeyError:
				raise Error("Unable to retrieve stream URL. Most likely invalid key")
		if track['downloadable']:
			self.downloadble = True
			self.downloadUrl = "{0}?client_id={1}".format(track['download_url'], clientKey)
			print '[!] Original file available. Retrieving filename...'
			r = urllib2.Request(self.downloadUrl)
			r.get_method = lambda : 'HEAD'
			r = urllib2.urlopen(r)
			self.downloadFilename = r.info()['Content-Disposition'].split('filename=')[1][1:-1]
		
	def report(self, block_no, block_size, file_size):
		self.download_progress += block_size
		if int(self.download_progress / 1024 * 8) > 1000:
			speed = "{0} Mbps".format(round((self.download_progress / 1024 / 1024 * 8) / (time.time() - self.current_time), 2))
		else:
			speed = "{0} Kbps".format(round((self.download_progress / 1024 * 8) / (time.time() - self.current_time), 2))
		rProgress = round(self.download_progress/1024.00/1024.00, 2)
		rFile = round(file_size/1024.00/1024.00, 2)
		percent = round(100 * float(self.download_progress)/float(file_size))
		sys.stdout.write("\r {3} ({0:.2f}/{1:.2f}MB): {2:.2f}%".format(rProgress, rFile, percent, speed))
		sys.stdout.flush()
	
	def save(self, name, url, filename):
		filename = dir+filename
		sys.stdout.write("\n[!] Downloading "+name+"...\n")
		filename, headers = urllib.urlretrieve(url=url, filename=filename, reporthook=self.report)
		self.download_progress = 0
	
	def download(self):
		print '[!] Starting downloads...'
		if self.artworkOrig != '':
			self.save('Artwork (Original)',self.artworkOrig,self.streamFilename+'-orig.jpg')
		self.save('Artwork (500x500)',self.artwork500,self.streamFilename+'-500.jpg')
		if self.streamable:
			self.save('Stream Audio',self.streamUrl,self.streamFilename+'.mp3')
		if self.downloadable:
			self.save('Original Audio',self.downloadUrl,self.downloadFilename)
		print '    done'

s = sound(url)
s.info()
s.download()
