#!/usr/bin/env python
import sys
import time
import pigpio

pin = 7

right_cycle = 1000
middle_cycle = 1500
left_cycle = 2000

pi = pigpio.pi()

def ring_it():
    pi.set_servo_pulsewidth(pin, left_cycle)
    time.sleep(0.2)

    pi.set_servo_pulsewidth(pin, right_cycle)
    time.sleep(0.13)

    pi.set_servo_pulsewidth(pin, left_cycle)
    time.sleep(0.1)

if len(sys.argv) == 1:
    ring_it()
else:
    num_rings = int(sys.argv[1])
    #print 'num_rings' + str(num_rings)
    for _ in range(0, num_rings):
        ring_it()

pi.stop()

