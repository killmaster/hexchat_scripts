# -*- coding: utf-8 -*-
__module_name__ = "media spammer"
__module_version__ = "9006 py3"
__module_description__ = "media spammer"
import urllib
from urllib import request
import socket
import os.path
import math
import json
import xchat
import platform
from html.parser import HTMLParser

#change
mpc_host = 'localhost'
mpc_port = '13579'

foo_host = '127.0.0.1'
foo_port = '3333'

MPVSOCK = "/tmp/mpvsocket"

#Must have web interface enabled and have a mpc-hc revision greater then 3110
#and you must update the host and port name if you change them from the default values
args = dict()

class MyHTMLParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.curtag = ("", None)
	def handle_starttag(self, tag, attrs):
		self.curtag = (tag, attrs)
	def handle_endtag(self, tag):
		self.curtag = ("", None)
	def handle_data(self, data):
		if self.curtag[0] == "p":
			if self.curtag[1][0][0] == "id":
				args[self.curtag[1][0][1]] = data

def mpcSpam(word, word_eol, userdata):
	req = urllib.request.Request('http://'+mpc_host+':'+mpc_port+'/variables.html')

	try: response = urllib.request.urlopen(req,timeout=2)
	except urllib.error.URLError as e:
		xchat.prnt('Server did not respond, maybe mpc-hc isn\'t running: '+str(e.reason))
		return xchat.EAT_ALL

	parser = MyHTMLParser()
	parser.feed(response.read().decode('utf-8'))

	filename = args["filepath"]
	size = os.path.getsize(filename)
	size = int(math.floor(size/1048576))
	filename = os.path.basename(filename)
	state = args["statestring"]
	current_time = args["positionstring"]
	total_time = args["durationstring"]
	position = float(args["position"])
	duration = float(args["duration"])
	loops = math.floor(((position/duration)*20))
	progress = "6"
	for i in range(20):
		if loops < i:
			progress = progress + "12"
			loops = 21
		progress = progress + '|'
	#variables: size, filename, state, current_time, total_time
	#xchat.command("ME 13»»6 MPC-HC 13«»6 ["+progress+"6] " + filename + " 13«»6 " + current_time + "/" + total_time + " 13«»6 "+str(size)+"MB 13«»6 [" + state + "]")
	xchat.command("ME 01 MPC-HC 04 " + filename + " 04 " + current_time + "01/04" + total_time + " 04 "+str(size)+"MB")
	return xchat.EAT_ALL

#Must have foo_controlserver and foo_controlserver output options set to
#'%codec%|||%playback_time%|||%length%|||%bitrate%|||$if(%album artist%,%album artist%,%artist%)|||%album%|||%date%|||%genre%|||%tracknumber%|||%title%|||%playback_time_seconds%|||%length_seconds%'
#also change the "Base Delimiter from "|" to "|||"
#or this will not work!
#also, as pointed out by weeaboo faggot herkz, if you wanna spam jap shit you gotta enable utf8 output
#foo_controlserver can be downloaded from this url: http://www.hydrogenaudio.org/forums/index.php?s=425185f6437f61b939f004da0c9eee91&act=attach&type=post&id=2744
#and be sure and update the ports/hostnames if you change them from the defaults
def fooSpam(word, word_eol, userdata):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try: sock.connect((foo_host,int(foo_port)))
	except socket.error as e:
		xchat.prnt('An error occured, foobar probably isn\'t running or you didn\'t install foo_controlserver: '+str(e))
		return xchat.EAT_ALL

	data = sock.recv(1024)
	buf = data.decode('utf-8')
	pos = buf.find('Connected to foobar2000 Control Server')
	if pos < 0:
		xchat.prnt('An error occured idk why m8')
		sock.close()
		return xchat.EAT_ALL
	else:
		data = sock.recv(1024)
		buf = data.decode('utf-8')
		sock.close()

	buf = buf.split('|||')
	state = {
		'111': lambda : 'Playing',
		'112': lambda : 'Stopped',
		'113': lambda : 'Paused'
	}[buf[0]]()
	codec = buf[4]
	current_time = buf[5]
	total_time = buf[6]
	bitrate = buf[7]
	artist = buf[8]
	album = buf[9]
	year = buf[10]
	genre = buf[11]
	track = buf[12]
	title = buf[13]
	position = float(buf[14])
	try:
		duration = float(buf[15])
		loops = math.floor(((position/duration)*20))
		derps = 0
		progress = ''
		while derps < 20:
			if loops < derps:
				progress = progress+'04'
				loops = 21
			progress = progress+'|'
			derps = derps+1
	except:
		duration = "∞"
		progress = "04||||||||||||||||||||"
	#variables: codec, current_time, total_time, birate, artist, album, year, genre, track, title
	#xchat.command(u"ME 13»»6 fb2k 13«»6 ["+progress+"6] " + artist + " [ "+album+" ] "+track+". "+title+" 13«»6 " + current_time + "/" + total_time + " 13«»6 "+bitrate+"kbps "+codec+" 13«»6 [" + state + "]")
	#xchat.command("ME 13»»6 fb2k 13«»6 " + artist + " [ "+album+" ] "+track+". "+title+" 13«»6 " + current_time + "/" + total_time + " 13«»6 "+bitrate+"kbps "+codec+" ")
	xchat.command("ME 01 fb2k 01 ["+progress+"01] 04" + artist + " [ 04"+album+" ] 04"+track+". "+title+"  " + current_time + "/" + total_time + "  "+bitrate+"kbps "+codec+"  [" + state + "]")
	return xchat.EAT_ALL

#run mpv with the --input-unix-socket=/tmp/mpvsocket flag, obviously you can change the socket location just be sure to update MPVSOCK
def mpvSpam(word, word_eol, userdata):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        sock.connect(MPVSOCK)
    except:
        xchat.prnt("Could not connect to "+MPVSOCK+"!")
        return xchat.EAT_ALL
    sock.sendall('{"command":["get_property","filename"]}\n')
    data = json.loads(sock.recv(1024))
    filename = data["data"].encode('utf-8')
    sock.sendall('{"command":["get_property","file-size"]}\n')
    data = json.loads(sock.recv(1024))
    size = int(data["data"]/1000000)
    sock.sendall('{"command":["get_property","pause"]}\n')
    data = json.loads(sock.recv(1024))
    state = data["data"]
    if state:
        state = "Paused"
    else:
        state = "Playing"
    sock.sendall('{"command":["get_property","time-pos"]}\n')
    data = json.loads(sock.recv(1024))
    try:
        position = float(data["data"])
    except:
        position = 0.0
    sock.sendall('{"command":["get_property","length"]}\n')
    data = json.loads(sock.recv(1024))
    sock.close()
    try:
        duration = float(data["data"])
    except:
        duration = 0.0
    c_hour = int(position/3600)
    c_min = int(position/60)-c_hour*60
    c_sec = int(position)-c_hour*3600-c_min*60
    current_time = str(c_min).zfill(2)+":"+str(c_sec).zfill(2)

    t_hour = int(duration/3600)
    t_min = int(duration/60)-t_hour*60
    t_sec = int(duration)-t_hour*3600-t_min*60
    if t_hour > 0:
        current_time = str(c_hour).zfill(1)+":"+str(c_min).zfill(2)+":"+str(c_sec).zfill(2)
        total_time = str(t_hour).zfill(1)+":"+str(t_min).zfill(2)+":"+str(t_sec).zfill(2)
    else:
        total_time = str(t_min).zfill(2)+":"+str(t_sec).zfill(2)
    loops = math.floor(((position/duration)*20))
    progress = "6"
    for i in range(20):
        if loops < i:
            progress = progress + "12"
            loops = 21
        progress = progress + '|'
    xchat.command("ME 13»»6 mpv 13«»6 ["+progress+"6] " + filename + " 13«»6 " + current_time + "/" + total_time + " 13«»6 "+str(size)+"MB 13«»6 [" + state + "]")
    return xchat.EAT_ALL

def rhySpam(word, word_eol, userdata):
    proc = subprocess.Popen(shlex.split("/usr/bin/rhythmbox-client --no-start --print-playing-format %aa§%at§%ay§%tN§%tt§%te§%td"),stdout=subprocess.PIPE)
    line, err = proc.communicate()
    line = line.rstrip('\n').split("§")
    xchat.command("ME 14»»7 rhythmbox 14«»7 " + line[0] + " [ "+line[1]+" ] "+line[3]+". "+line[4]+" 14«»7 " + line[5] + "/" + line[6])
    return xchat.EAT_ALL

if platform.system() == "Windows":
    xchat.hook_command('vid', mpcSpam)
else:
    xchat.hook_command('vid', mpvSpam)

if platform.system() == "Windows":
    xchat.hook_command('aud', fooSpam)
else:
    xchat.hook_command('aud', rhySpam)
