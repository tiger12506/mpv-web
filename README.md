1. Install Python3 pip

    sudo apt install python3-pip

2. Install Flask

    sudo pip3 install Flask

3. Install python-mpv

    sudo pip3 install python-mpv

4. Create fifo /tmp/mpv and /tmp/mpv-playlist.m3u

    mkfifo /tmp/mpv
    mkfifo /tmp/mpv-playlist.m3u

5. Run mpv in slave mode

    mpv --input-file=/tmp/mpv --idle /tmp/mpv-playlist.m3u

6. Run debug-mpv, which sets up flask to run app to run on port 5000 in debug mode

GOAL is to provide a web interface to an mpv instance under slave mode, to allow controlling RPi3 with web browser on any device
