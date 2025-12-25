# Jedi Mirror



Jedi Mirror is a smart mirror with a screen behind it that is controlled with a RaspberryPi. The camera connected to the RaspberryPi will run a hand-tracking software which is controlled by OpenCV. With the hand-tracking software the person will be able to control the contents of the mirror without touching it.





#### Bill Of Materials



1. Samsung Essential S4 24"" FHD IPS Monitor (Any screen with HDMI and at least 300 nits should be fine this is my choice)
2. 1 mm Silver Acrylic One-Way Mirror,
3. Raspberry Pi 4 4gb (or better)
4. 1 mm Silver Acrylic One-Way Mirror
5. Wooden Frame



### Setup



1. sudo apt update
2. sudo apt install -y python3-pip python3-opencv python3-picamera2
3. python3 -m pip install --user mediapipe pynput numpy
4. nano hand\_mouse\_picam2.py
5. Paste the code from hand\_mouse\_picam2.py to here
6. python3 hand\_mouse\_picam2.py

And you are good to go 😀
