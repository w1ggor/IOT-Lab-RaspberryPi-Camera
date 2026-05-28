"""
Module 2 - Color Analysis
Takes a photo with the Raspberry Pi Camera, analyzes the ratio of colors
present in the image, and saves the results to a report.txt file.
Requires: picamera2, Pillow, numpy
  sudo apt install python3-picamera2 python3-pil python3-numpy
"""

import os
import time
import colorsys
import numpy
from PIL import Image
import RPi.GPIO as GPIO
from picamera2 import Picamera2


IMAGES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images")
DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")

PIN_LED_BLUE = 17
PIN_BUZZER = 18

# Color hue ranges in degrees (0-360) used for classification
# Saturation and value thresholds separate achromatic colors (black/white/gray)
COLOR_RANGES = [
    ("Red",     0,   15),
    ("Orange",  15,  45),
    ("Yellow",  45,  75),
    ("Green",   75,  150),
    ("Cyan",    150, 195),
    ("Blue",    195, 255),
    ("Purple",  255, 285),
    ("Pink",    285, 345),
    ("Red",     345, 360),
]

SATURATION_MIN = 0.2
VALUE_MIN = 0.15
VALUE_MAX = 0.85


def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_LED_BLUE, GPIO.OUT)
    GPIO.setup(PIN_BUZZER, GPIO.OUT)
    GPIO.output(PIN_LED_BLUE, GPIO.LOW)
    GPIO.output(PIN_BUZZER, GPIO.LOW)


def shutter_feedback():
    pwm = GPIO.PWM(PIN_BUZZER, 1000)
    pwm.start(50)
    for _ in range(4):
        GPIO.output(PIN_LED_BLUE, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(PIN_LED_BLUE, GPIO.HIGH)
        time.sleep(0.1)
    pwm.stop()


def cleanup_gpio():
    GPIO.output(PIN_LED_BLUE, GPIO.LOW)
    GPIO.output(PIN_BUZZER, GPIO.LOW)
    GPIO.cleanup()


def ensure_dirs():
    for d in [IMAGES_DIR, DOCS_DIR]:
        if not os.path.exists(d):
            os.makedirs(d)


def capture_photo():
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = "analysis_" + timestamp + ".jpg"
    filepath = os.path.join(IMAGES_DIR, filename)

    GPIO.output(PIN_LED_BLUE, GPIO.HIGH)
    print("Initializing camera...")
    camera = Picamera2()
    config = camera.create_still_configuration(main={"size": (1920, 1080)})
    camera.configure(config)
    camera.start()
    print("Camera warming up, please wait...")
    time.sleep(2)
    print("Taking photo...")
    camera.capture_file(filepath)
    camera.stop()
    camera.close()

    shutter_feedback()
    return filepath, timestamp


def classify_pixel(r, g, b):
    r_norm = r / 255.0
    g_norm = g / 255.0
    b_norm = b / 255.0
    h, s, v = colorsys.rgb_to_hsv(r_norm, g_norm, b_norm)
    hue = h * 360.0

    if v < VALUE_MIN:
        return "Black"
    if v > VALUE_MAX and s < SATURATION_MIN:
        return "White"
    if s < SATURATION_MIN:
        return "Gray"

    for name, low, high in COLOR_RANGES:
        if low <= hue < high:
            return name

    return "Unknown"


def analyze_colors(filepath):
    print("Analyzing image colors...")
    img = Image.open(filepath).convert("RGB")

    # Resize to speed up analysis without losing color distribution
    img = img.resize((320, 180))

    pixels = numpy.array(img).reshape(-1, 3)
    total = len(pixels)

    counts = {}
    for r, g, b in pixels:
        color = classify_pixel(int(r), int(g), int(b))
        counts[color] = counts.get(color, 0) + 1

    results = {}
    for color, count in counts.items():
        results[color] = (count / total) * 100.0

    return dict(sorted(results.items(), key=lambda x: x[1], reverse=True))


def save_report(filepath, timestamp, results):
    report_filename = "report_" + timestamp + ".txt"
    report_path = os.path.join(DOCS_DIR, report_filename)

    lines = []
    lines.append("Color Analysis Report")
    lines.append("=" * 40)
    lines.append("Date/Time : " + time.strftime("%Y-%m-%d %H:%M:%S"))
    lines.append("Image     : " + os.path.basename(filepath))
    lines.append("")
    lines.append("Color Distribution:")
    lines.append("-" * 40)

    dominant = max(results, key=results.get)
    for color, percentage in results.items():
        bar_len = int(percentage / 2)
        bar = "#" * bar_len
        lines.append("{:<10} {:>6.2f}%  {}".format(color, percentage, bar))

    lines.append("-" * 40)
    lines.append("Dominant color: " + dominant + " ({:.2f}%)".format(results[dominant]))
    lines.append("")

    with open(report_path, "w") as f:
        f.write("\n".join(lines))

    print("Report saved to: " + report_path)
    return report_path


def run():
    ensure_dirs()
    setup_gpio()

    filepath, timestamp = capture_photo()
    results = analyze_colors(filepath)
    report_path = save_report(filepath, timestamp, results)

    cleanup_gpio()

    print("")
    print("--- Results ---")
    for color, pct in results.items():
        print("{:<10} {:.2f}%".format(color, pct))

    return report_path


if __name__ == "__main__":
    run()
