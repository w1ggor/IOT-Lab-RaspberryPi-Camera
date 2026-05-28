IOT Lab Assignment - Exploring the Raspberry Pi Camera
=======================================================

Description:
  Lab assignment for exploring the Raspberry Pi Camera module.
  Written in Python 3, designed to run on Raspberry Pi via Thonny.

Project Structure:
  src/        - Python scripts
  images/     - Captured image output
  videos/     - Captured video output
  docs/       - Lab notes and reports

Requirements:
  - Raspberry Pi with camera module attached
  - Camera enabled via: sudo raspi-config
  - Python 3
  - picamera2 (recommended for Raspberry Pi OS Bullseye and newer)
    Install: sudo apt install python3-picamera2
  - Alternatively: picamera (legacy)
    Install: sudo apt install python3-picamera

Usage:
  Run scripts from Thonny or from terminal:
    python3 src/script_name.py
