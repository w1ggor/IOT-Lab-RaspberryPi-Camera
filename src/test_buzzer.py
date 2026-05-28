"""
Temporary buzzer test script - delete after testing.
Tests both active (DC) and passive (PWM) buzzer modes.
GPIO 18
"""

import time
import RPi.GPIO as GPIO

PIN_BUZZER = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_BUZZER, GPIO.OUT)
GPIO.output(PIN_BUZZER, GPIO.HIGH)

print("Test 1 - DC signal (active buzzer style)...")
for i in range(3):
    print("Beep " + str(i + 1))
    GPIO.output(PIN_BUZZER, GPIO.LOW)
    time.sleep(0.3)
    GPIO.output(PIN_BUZZER, GPIO.HIGH)
    time.sleep(0.3)

time.sleep(1)

print("Test 2 - PWM 1000Hz (passive buzzer style)...")
pwm = GPIO.PWM(PIN_BUZZER, 1000)
for i in range(3):
    print("Beep " + str(i + 1))
    pwm.start(50)
    time.sleep(0.3)
    pwm.stop()
    time.sleep(0.3)

GPIO.cleanup()
print("Done. Which test made a proper sound?")
