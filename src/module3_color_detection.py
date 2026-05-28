"""
Module 3 - Color Detection with LED and Buzzer Response
Detects red, green, and blue colors using the Raspberry Pi Camera.
Works in two modes:
  1 - Single capture: takes one photo and responds for a few seconds
  2 - Real-time: continuously reads the camera until Ctrl+C

LED and buzzer behavior:
  - Blue detected  -> blue LED on  (GPIO 17)
  - Green detected -> green LED on (GPIO 27)
  - Red detected   -> red LED on   (GPIO 22)
  - Higher color % -> buzzer beeps faster

Requires: picamera2, numpy
  sudo apt install python3-picamera2 python3-numpy
"""

import os
import time
import numpy
import RPi.GPIO as GPIO
from PIL import Image
from picamera2 import Picamera2


PIN_LED_BLUE  = 17
PIN_LED_GREEN = 27
PIN_LED_RED   = 22
PIN_BUZZER    = 18

# Minimum color percentage to trigger an LED
DETECTION_THRESHOLD = 5.0

# How much a channel must exceed the other two to count as that color
COLOR_MARGIN = 30


def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    for pin in [PIN_LED_BLUE, PIN_LED_GREEN, PIN_LED_RED, PIN_BUZZER]:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)


def cleanup_gpio():
    for pin in [PIN_LED_BLUE, PIN_LED_GREEN, PIN_LED_RED, PIN_BUZZER]:
        GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup()


def beep(duration=0.05):
    pwm = GPIO.PWM(PIN_BUZZER, 1000)
    pwm.start(50)
    time.sleep(duration)
    pwm.stop()
    GPIO.output(PIN_BUZZER, GPIO.LOW)


def beep_interval(percentage):
    """Returns how many frames to wait between beeps. 0 means no beep."""
    if percentage < DETECTION_THRESHOLD:
        return 0
    if percentage < 20:
        return 6
    if percentage < 40:
        return 4
    if percentage < 60:
        return 2
    return 1


def analyze_colors(frame_array):
    """
    Fast numpy-based RGB color detection.
    Returns (red_pct, green_pct, blue_pct) as float percentages.
    picamera2 capture_array() returns BGR, so channels are index 2=R, 1=G, 0=B.
    """
    img = Image.fromarray(frame_array).resize((160, 120))
    arr = numpy.array(img, dtype=numpy.int16)

    r = arr[:, :, 2]
    g = arr[:, :, 1]
    b = arr[:, :, 0]
    total = float(r.size)

    red_mask   = (r.astype(numpy.int16) - g > COLOR_MARGIN) & (r.astype(numpy.int16) - b > COLOR_MARGIN)
    green_mask = (g.astype(numpy.int16) - r > COLOR_MARGIN) & (g.astype(numpy.int16) - b > COLOR_MARGIN)
    blue_mask  = (b.astype(numpy.int16) - r > COLOR_MARGIN) & (b.astype(numpy.int16) - g > COLOR_MARGIN)

    red_pct   = float(numpy.sum(red_mask))   / total * 100.0
    green_pct = float(numpy.sum(green_mask)) / total * 100.0
    blue_pct  = float(numpy.sum(blue_mask))  / total * 100.0

    return red_pct, green_pct, blue_pct


def update_leds(red_pct, green_pct, blue_pct):
    GPIO.output(PIN_LED_RED,   GPIO.HIGH if red_pct   >= DETECTION_THRESHOLD else GPIO.LOW)
    GPIO.output(PIN_LED_GREEN, GPIO.HIGH if green_pct >= DETECTION_THRESHOLD else GPIO.LOW)
    GPIO.output(PIN_LED_BLUE,  GPIO.HIGH if blue_pct  >= DETECTION_THRESHOLD else GPIO.LOW)


def print_status(red_pct, green_pct, blue_pct):
    detected = []
    if red_pct   >= DETECTION_THRESHOLD: detected.append("RED")
    if green_pct >= DETECTION_THRESHOLD: detected.append("GREEN")
    if blue_pct  >= DETECTION_THRESHOLD: detected.append("BLUE")
    label = ", ".join(detected) if detected else "none"
    print("R:{:5.1f}%  G:{:5.1f}%  B:{:5.1f}%  |  Detected: {}".format(
        red_pct, green_pct, blue_pct, label))


def realtime_mode():
    print("Starting real-time color detection. Press Ctrl+C to stop.")
    print("")

    camera = Picamera2()
    config = camera.create_video_configuration(
        main={"size": (640, 480), "format": "RGB888"}
    )
    camera.configure(config)
    camera.start()
    time.sleep(1)

    frame_count = 0
    try:
        while True:
            frame = camera.capture_array()
            red_pct, green_pct, blue_pct = analyze_colors(frame)

            update_leds(red_pct, green_pct, blue_pct)
            print_status(red_pct, green_pct, blue_pct)

            dominant_pct = max(red_pct, green_pct, blue_pct)
            interval = beep_interval(dominant_pct)
            if interval > 0 and frame_count % interval == 0:
                beep(0.05)

            frame_count += 1
            time.sleep(0.2)

    except KeyboardInterrupt:
        print("")
        print("Stopped.")
    finally:
        camera.stop()
        camera.close()


def single_capture_mode():
    print("Taking photo for color detection...")

    camera = Picamera2()
    config = camera.create_still_configuration(main={"size": (1920, 1080)})
    camera.configure(config)
    camera.start()
    time.sleep(2)
    frame = camera.capture_array()
    camera.stop()
    camera.close()

    red_pct, green_pct, blue_pct = analyze_colors(frame)
    print_status(red_pct, green_pct, blue_pct)

    update_leds(red_pct, green_pct, blue_pct)

    # Hold LEDs and buzz for 5 seconds then turn off
    dominant_pct = max(red_pct, green_pct, blue_pct)
    interval = beep_interval(dominant_pct)
    end_time = time.time() + 5.0
    frame_count = 0
    while time.time() < end_time:
        if interval > 0 and frame_count % interval == 0:
            beep(0.05)
        frame_count += 1
        time.sleep(0.2)

    cleanup_gpio()


if __name__ == "__main__":
    setup_gpio()

    print("Module 3 - Color Detection")
    print("1 - Single capture")
    print("2 - Real-time")
    choice = input("Select mode (1 or 2): ").strip()

    if choice == "1":
        single_capture_mode()
    elif choice == "2":
        realtime_mode()
        cleanup_gpio()
    else:
        print("Invalid choice.")
        cleanup_gpio()
