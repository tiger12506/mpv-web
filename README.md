GOAL is to provide a web interface to an mpv instance under slave mode, to allow controlling RPi3 with web browser on any device

1. Install Python3 pip

    sudo apt install python3-pip

2. Install Flask

    sudo pip3 install Flask

3. Install python-mpv

    sudo pip3 install python-mpv

4. Run debug-mpv, which sets up flask to run app to run on port 5000 in debug mode

    ./debug-mpv

    a. Create fifo /tmp/mpv

        mkfifo /tmp/mpv

    b. Run mpv in slave mode

        mpv --input-file=/tmp/mpv --idle


5. While debug-mpv holds open instance of mpv, make changes and save mpv.py as needed and work with browser granpi:5000/

