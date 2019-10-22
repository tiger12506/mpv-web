import os
import sys
from flask import Flask
from flask import request
app = Flask(__name__)

directory = '/home/jacob/tv'
fifo_name = '/tmp/mpv'
playlist_fifo_name = '/tmp/mpv-playlist.m3u'

html = '''
<html>
    <head>
        <title>MPV frontend for RPi</title>
    </head>

    <body>
        <h1>This works</h1>
        <ul>
        {0}
        </ul>
    </body>
</html>
'''

@app.route('/version')
def version():
    return sys.version

@app.route('/')
def index():
    comb = ''
    for p in os.listdir(directory):
        full = os.path.join(directory, p)
        if os.path.isdir(full):
            continue
        if os.path.isfile(full):
            comb += "<li><a href=\"/add?path="+full+"\">" + p + "</a></li>\n"

    return html.format(comb)

@app.route('/add', methods=['GET'])
def add():
    p = request.args.get('path')
    try:
        playlist_fifo = open(playlist_fifo_name, "w")
        playlist_fifo.write(p+'\n')
        playlist_fifo.close()
        return 'OK' + index()
    except:
        return 'FAIL' + index()

cmd_map = { 'pause'     : 'cycle pause', \
            'mute'      : 'cycle mute', \
            'next'      : 'playlist-next', \
            'prev'      : 'playlist-prev', \
            'volup'     : 'add volume 2', \
            'voldn'     : 'add volume -2', \
            'seekup'    : 'seek 5', \
            'seekdn'    : 'seek -5', \
            'subtitles' : 'cycle sub-visibility', \
            'quit'      : 'quit', \
            'audio'     : 'cycle audio', \
            'loop'      : 'cycle-values loop-file "inf" "no"', \
            'framenext' : 'frame-step', \
            'frameprev' : 'frame-back-step', \
            'show'      : 'show_text ${playlist}' \
}

@app.route('/cmd/<command>')
def cmd(command):
    if (command in cmd_map):
        return send(cmd_map[command])
    return 'FAIL: command={}'.format(command)

def send(command):
    try:
        cmd_fifo = open(fifo_name, "w")
        cmd_fifo.write(command+'\n')
        cmd_fifo.close()
        return 'OK'
    except:
        return 'FAIL'

