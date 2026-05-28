"""
Module 1 - Take a Selfie
Captures a photo using the Raspberry Pi Camera and saves it to the images folder.
"""

import os
import time
from picamera2 import Picamera2


IMAGES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images")


def ensure_images_dir():
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)


def take_selfie():
    ensure_images_dir()

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

    print("Photo saved to: " + filepath)
    return filepath


if __name__ == "__main__":
    path = take_selfie()
    print("Done. File: " + path)
