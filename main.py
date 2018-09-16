#!/usr/bin/python

import sys
import RPi.GPIO as GPIO
import time
import simpleaudio as sa
import pdb

def start_audio(wave_object):
    play_obj = wave_object.play()
    return play_obj
    
def stop_audio(play_object):
    play_object.stop()

def calculate_distance():
    time.sleep(.025)
    GPIO.output(PIN_TRIGGER, GPIO.HIGH)
    time.sleep(0.00001) # 1.0 nanosecond pulse required to trigger sensor
    GPIO.output(PIN_TRIGGER, GPIO.LOW)

    while GPIO.input(PIN_ECHO)==0:
        pulse_start_time = time.time()
    while GPIO.input(PIN_ECHO)==1:
        pulse_end_time = time.time()
    time.sleep(.0001)
    pulse_duration = pulse_end_time - pulse_start_time
    distance = round(pulse_duration * 1750, 2) # calculate distance in cm

#    print('DISTANCE: ', distance)
    return distance

try:
    print('Initializing...')
    wave_obj = sa.WaveObject.from_wave_file('/lego-dev/Aquaspin/media/humble.wav')

    GPIO.setmode(GPIO.BOARD)
    PIN_TRIGGER = 7
    PIN_ECHO = 11

    GPIO.setup(PIN_TRIGGER, GPIO.OUT)
    GPIO.setup(PIN_ECHO, GPIO.IN)

    GPIO.output(PIN_TRIGGER, GPIO.LOW)

    print('Ready...')

    play_obj = None
    
    while True:
        time.sleep(.025)
        distance = calculate_distance()

        if distance > .8:
            play_obj = start_audio(wave_obj)
            time.sleep(.025)
            
            Condition = play_obj.is_playing
            while Condition:
                if (calculate_distance() < .8):
                    stop_audio(play_obj)
                    Condition = False

    print('done!')
except KeyboardInterrupt:
    print('Application stopped by keyboard input')
    
finally:
    print('finally...')
    GPIO.cleanup()
