# Gong v2

The latest and greatest implementation of my Raspberry Pi-controlled remote Gong ringing machine.

2019-12-08, 2019-12-09: I tried multiple times to install Python 3.8 using pyenv, but no luck. It took several hours to build and kept failing because of missing dependencies. I could probably figure this out with more time, but it is really a hassle!

2019-12-10: Really tried to get this to work with Python 3, pyenv, and pipenv... but the C build times were way to slow and taxing on the CPU, so I resorted to Python 2 and installing pigpio via apt-get, which was WAY faster:

```
sudo apt-get install pigpio python-pigpio python3-pigpio
```

pigpio also seems better, because it has hardware-level, rather than software-level timings (which is what I was attempting with RPi.GPIO.

I was able to quickly put together a small proof-of-concept script, ringgong.py that turns the servo and rings the Gong using pigpio. I think this is the way to go!

