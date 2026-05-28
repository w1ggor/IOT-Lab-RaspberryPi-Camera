"""
Temporary buzzer test script - delete after testing.
Buzzer is low level trigger: LOW = on, HIGH = off.
GPIO 18
"""

import time
import RPi.GPIO as GPIO

PIN_BUZZER = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_BUZZER, GPIO.OUT)
GPIO.output(PIN_BUZZER, GPIO.HIGH)

print("Buzzer test starting...")

for i in range(3):
    print("Beep " + str(i + 1))
    GPIO.output(PIN_BUZZER, GPIO.LOW)
    time.sleep(0.3)
    GPIO.output(PIN_BUZZER, GPIO.HIGH)
    time.sleep(0.3)

GPIO.cleanup()
print("Done.")
