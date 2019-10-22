import os
import sys
from flask import Flask
from flask import request
app = Flask(__name__)

directory = '/home/jacob/tv'
fifo_name = '/tmp/mpv'

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
            comb += "<li><a href=\"/add?path="+p+"\">" + p + "</a></li>\n"

    return html.format(comb)

@app.route('/add', methods=['GET'])
def add():
    p = request.args.get('path')
    return 'commanded to play with path: {}'.format(p)

cmd_map = { 'pause'     : 'cycle pause', \
            'mute'      : 'mute', \
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
            'frameprev' : 'frame-back-step'
}

@app.route('/cmd/<command>')
def cmd(command):
    if (command in cmd_map):
        return send(cmd_map[command])
    return 'FAIL: command={}'.format(command)

def send(command):
    try:
        f.write(command+'\n')
        f.flush()
        return 'OK'
    except:
        return 'FAIL'

f = open(fifo_name, "w+")
