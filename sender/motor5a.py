#!/usr/bin/python3

# motor5a.py
# Calibrated by tanh function
# 2021 4/17
# Yasushi Honda

import pigpio
import time
import numpy as np

MIN_WIDTH=1000
MID_WIDTH=1500
MAX_WIDTH=2000

class Motor:

   def __init__(self,gpio):
      self.gpio=gpio
      self.pi = pigpio.pi()
      if not self.pi.connected:
         exit()
      self.pi.set_servo_pulsewidth(gpio, MID_WIDTH)

   def move(self,power):
      self.pi.set_servo_pulsewidth(self.gpio, MID_WIDTH+power)

   def stop(self):
      self.move(0)
      self.pi.stop()

class Lmotor(Motor):
   def run(self,power):
      output=62*np.arctanh(-power/101)+6*np.sign(-power)
      self.move(output)

class Rmotor(Motor):
   def run(self,power):
      output=62*np.arctanh(power/101)+6*np.sign(power)
      self.move(output)
