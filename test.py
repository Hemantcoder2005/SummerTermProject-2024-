import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

SENSOR_PINS = {
    'central': {'trigger': 16, 'echo': 18}
}

for sensor in SENSOR_PINS.values():
    GPIO.setup(sensor['trigger'], GPIO.OUT)
    GPIO.setup(sensor['echo'], GPIO.IN)


def measure_distance(trigger, echo):
    GPIO.output(trigger, False)
    time.sleep(0.2)
    GPIO.output(trigger, True)
    time.sleep(0.00001)
    GPIO.output(trigger, False)
    start, stop = time.time(), time.time()
    while GPIO.input(echo) == 0:
        start = time.time()
    while GPIO.input(echo) == 1:
        stop = time.time()
    elapsed = stop - start
    distance = elapsed * 34000 / 2
    print(distance)
    return distance

while True:
    measure_distance(16,18)