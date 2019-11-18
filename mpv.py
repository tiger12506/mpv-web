import os
import sys
from flask import Flask
from flask import request, redirect, url_for, jsonify
from jinja2 import Environment, PackageLoader, select_autoescape


directory = '/home/jacob/tv'
fifo_name = '/tmp/mpv'


env = Environment(
        loader=PackageLoader('mpv', 'templates'),
        autoescape=select_autoescape(['html', 'xml']),
        line_statement_prefix='#'

)
template = env.get_template('index.html')
dir_template = env.get_template('dir.html')

app = Flask(__name__)

@app.route('/version')
def version():
    return sys.version

@app.route('/')
def index():
    (dirs, files) = list_dir(directory)
    return template.render(dirs=dirs, files=files)

@app.route('/dir', methods=['GET'])
def get_dir():
    d = request.args.get('path', "")
    result = list_dir(d)
    return dir_template.render(dirs=result[0], files=result[1])

def list_dir(d=""):
    if d == "": d = directory
    lis = []
    licnt = 0
    dirs = []
    dircnt = 0
    for p in sorted(os.listdir(d)):
        full = os.path.join(d, p)
        if os.path.isdir(full):
            dirs.append((dircnt, p, full))
            dircnt += 1
        if os.path.isfile(full):
            lis.append((licnt, p, full))
            licnt += 1
    return (dirs, lis)

@app.route('/add', methods=['GET'])
def add():
    p = request.args.get('path')
    result = send('loadfile {} append-play'.format(p))
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

@app.route('/favicon.ico')
def icon():
    return redirect(url_for('static', filename='open-iconic/svg/audio-spectrum.svg'))

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

