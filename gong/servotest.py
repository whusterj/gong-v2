#!/usr/bin python
"""

A SG90 mini servo can be controlled by timed HIGH pulses.

      0 degrees   0.5ms pulse
     90 degrees   1.5ms pulse
    180 degrees   2.5ms pulse

"""
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)

try:
    while True:
        # Send a HIGH signal for
        GPIO.output(7, 1)
        time.sleep(0.0015)
        GPIO.output(7, 0)
        time.sleep(2)
except KeyboardInterrupt:
    GPIO.cleanup()
