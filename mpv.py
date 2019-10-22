#!/usr/bin/env python
from flask import Flask, escape, request
import os

fifo_name = '/tmp/mpv'

map = ["pause", "next", "prev", "volup", "voldn", "mute", "seekup", "seekdn", "subtitles", "quit", "framenext", "frameprev", "audio", "loop"]

app = Flask(__name__)

@app.route('/')
def help():
    return "<ul>" + "\n".join("<li><a href=\"/"+x+"\">" + x + "</a></li>" for x in map) + "</ul>"

@app.route('/pause')
def pause():
    return send("cycle pause")

@app.route('/next')
def next():
    return send("playlist-next")

@app.route('/prev')
def prev():
    return send("playlist-prev")

@app.route('/volup')
def volume_up():
    return send("add volume 2")

@app.route('/voldn')
def volume_down():
    return send("add volume -2")

@app.route('/mute')
def mute():
    return send("mute")

@app.route('/seekup')
def seek_up():
    return send("seek 5")

@app.route('/seekdn')
def seek_down():
    return send("seek -5")

@app.route('/subtitles')
def subtitles():
    return send("cycle sub-visibility")

@app.route('/quit')
def quit():
    return send("quit")

@app.route('/framenext')
def frame_next():
    return send("frame-step")

@app.route('/frameprev')
def frame_prev():
    return send("frame-back-step")

@app.route('/audio')
def audio_next():
    return send("cycle audio")

@app.route('/loop')
def loop():
    return send("cycle-values loop-file \"inf\" \"no\"")

def send(command):
    try:
        f.write(command+"\n")
        f.flush()
        return "OK<hr>" + help() + '<hr><input type="text" name="url"><input type="submit" value="Submit">'
    except:
        return "FAIL<hr>" + help()


f = open(fifo_name, "w+")

app.run(host='0.0.0.0', port=1250, debug=True)
