"""
Module 1 - Take a Selfie
Captures a photo using the Raspberry Pi Camera and saves it to the images folder.
Gives feedback with a buzzer beep and blue LED flash when the photo is taken.
"""

import os
import time
import RPi.GPIO as GPIO
from picamera2 import Picamera2


IMAGES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images")

PIN_LED_BLUE = 17
PIN_BUZZER = 18

# Buzzer is low level trigger: LOW = on, HIGH = off


def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_LED_BLUE, GPIO.OUT)
    GPIO.setup(PIN_BUZZER, GPIO.OUT)
    GPIO.output(PIN_LED_BLUE, GPIO.LOW)
    GPIO.output(PIN_BUZZER, GPIO.HIGH)


def shutter_feedback():
    GPIO.output(PIN_LED_BLUE, GPIO.HIGH)
    GPIO.output(PIN_BUZZER, GPIO.LOW)
    time.sleep(0.15)
    GPIO.output(PIN_LED_BLUE, GPIO.LOW)
    GPIO.output(PIN_BUZZER, GPIO.HIGH)


def cleanup_gpio():
    GPIO.output(PIN_LED_BLUE, GPIO.LOW)
    GPIO.output(PIN_BUZZER, GPIO.HIGH)
    GPIO.cleanup()


def ensure_images_dir():
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)


def take_selfie():
    ensure_images_dir()
    setup_gpio()

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = "selfie_" + timestamp + ".jpg"
    filepath = os.path.join(IMAGES_DIR, filename)

    print("Initializing camera...")
    camera = Picamera2()

    config = camera.create_still_configuration(
        main={"size": (1920, 1080)}
    )
    camera.configure(config)

    camera.start()
    print("Camera warming up, please wait...")
    time.sleep(2)

    print("Taking photo...")
    camera.capture_file(filepath)

    camera.stop()
    camera.close()

    shutter_feedback()
    cleanup_gpio()

    print("Photo saved to: " + filepath)
    return filepath


if __name__ == "__main__":
    path = take_selfie()
    print("Done. File: " + path)
