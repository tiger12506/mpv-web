import os
import sys
from flask import Flask
from flask import request
from jinja2 import Environment, PackageLoader, select_autoescape


directory = '/home/jacob/tv'
fifo_name = '/tmp/mpv'


env = Environment(
        loader=PackageLoader('mpv', 'templates'),
        autoescape=select_autoescape(['html', 'xml']),
        line_statement_prefix='#'

)
template = env.get_template('index.html')

app = Flask(__name__)

@app.route('/version')
def version():
    return sys.version

@app.route('/')
def index():
    lis = []
    for p in os.listdir(directory):
        full = os.path.join(directory, p)
        if os.path.isdir(full):
            continue
        if os.path.isfile(full):
            lis.append((p, full))

    return template.render(dirlist=lis)

@app.route('/add', methods=['GET'])
def add():
    p = request.args.get('path')
    full = os.path.join(directory, p)
    result = send('loadfile {} append-play'.format(full))
    return result + index()

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
            'show'      : 'show_text ${playlist}', \
            'clear'     : 'playlist-clear' \
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

