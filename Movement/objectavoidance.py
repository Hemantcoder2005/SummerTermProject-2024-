import RPi.GPIO as GPIO
import time

# Define GPIO for Driver motors
MOTOR_PINS = {
    'forward_left': 11,
    'forward_right': 15,
    'backward_left': 37,
    'backward_right': 13
}

GPIO.setmode(GPIO.BOARD)
for pin in MOTOR_PINS.values():
    GPIO.setup(pin, GPIO.OUT)

# Define GPIO for ultrasonic sensors
SENSOR_PINS = {
    'central': {'trigger': 16, 'echo': 18},
    'right': {'trigger': 33, 'echo': 35},
    'left': {'trigger': 38, 'echo': 40}
}

for sensor in SENSOR_PINS.values():
    GPIO.setup(sensor['trigger'], GPIO.OUT)
    GPIO.setup(sensor['echo'], GPIO.IN)

# Functions for driving
def set_motor_state(forward_left, forward_right, backward_left, backward_right):
    GPIO.output(MOTOR_PINS['forward_left'], forward_left)
    GPIO.output(MOTOR_PINS['forward_right'], forward_right)
    GPIO.output(MOTOR_PINS['backward_left'], backward_left)
    GPIO.output(MOTOR_PINS['backward_right'], backward_right)

def goforward():
    print("Forward")
    set_motor_state(True, True, False, False)

def gobackward():
    print("back")
    set_motor_state(False, False, True, True)

def turnleft():
    print("left")
    set_motor_state(True, False, False, False)
    time.sleep(0.8)
    set_motor_state(False, False, False, False)

def turnright():
    print("right")
    set_motor_state(False, True, False, False)
    time.sleep(0.8)
    set_motor_state(False, False, False, False)

def stopmotors():
    print("stop")
    set_motor_state(False, False, False, False)

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

def frontobstacle():
    print("Front Sensor")
    return measure_distance(SENSOR_PINS['central']['trigger'], SENSOR_PINS['central']['echo'])

def rightobstacle():
    print("right Sensor")
    return measure_distance(SENSOR_PINS['right']['trigger'], SENSOR_PINS['right']['echo'])

def leftobstacle():
    print("left Sensor")
    return measure_distance(SENSOR_PINS['left']['trigger'], SENSOR_PINS['left']['echo'])

def avoid_obstacle():
    stopmotors()
    left_dist = leftobstacle()
    right_dist = rightobstacle()
    if left_dist > right_dist:
        turnleft()
    else:
        turnright()
    goforward()

def prefer_left_lane():
    if frontobstacle() > 30 and leftobstacle() < rightobstacle():
        turnleft()
        goforward()

def obstacleavoiddrive():
    goforward()
    start_time = time.time()
    while time.time() - start_time < 300:  # 300 seconds = 5 minutes
        if frontobstacle() < 30:
            avoid_obstacle()
        else:
            prefer_left_lane()
    cleargpios()

def cleargpios():
    print("clearing GPIO")
    for pin in MOTOR_PINS.values():
        GPIO.output(pin, False)
    for sensor in SENSOR_PINS.values():
        GPIO.output(sensor['trigger'], False)
    print("All GPIOs CLEARED")

def main():
    cleargpios()
    print("start driving: ")
    obstacleavoiddrive()

if __name__ == "__main__":
    main()
