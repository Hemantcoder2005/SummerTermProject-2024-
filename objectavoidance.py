import time
import RPi.GPIO as GPIO

# GPIO Mode (BOARD)
GPIO.setmode(GPIO.BOARD)

# Set GPIO Pins for Ultrasonic Sensors
SENSOR_PINS = {
    'central': {'trigger': 16, 'echo': 18},
    'right': {'trigger': 33, 'echo': 35},
    'left': {'trigger': 38, 'echo': 40}
}

# Define GPIO for Driver motors
MOTOR_PINS = {
    'motora_in1': 11,
    'motora_in2': 13,
    'motorb_in3': 15,
    'motorb_in4': 37  
}

# Set GPIO direction (IN / OUT)
for sensor in SENSOR_PINS.values():
    GPIO.setup(sensor['trigger'], GPIO.OUT)
    GPIO.setup(sensor['echo'], GPIO.IN)

for pin in MOTOR_PINS.values():
    GPIO.setup(pin, GPIO.OUT)

# Function to measure distance
def distance(trigger, echo):
    # Ensure trigger is low
    GPIO.output(trigger, False)
    time.sleep(0.05)

    # Send a short 10us pulse to trigger
    GPIO.output(trigger, True)
    time.sleep(0.00001)
    GPIO.output(trigger, False)

    start_time = time.time()
    stop_time = time.time()

    # Save start_time
    while GPIO.input(echo) == 0:
        start_time = time.time()

    # Save stop_time
    while GPIO.input(echo) == 1:
        stop_time = time.time()

    # Time difference between start and arrival
    elapsed_time = stop_time - start_time

    # Calculate distance
    dist = (elapsed_time * 34300) / 2
    return dist


# Functions for driving
def set_motor_state(forward_left, backward_left, forward_right, backward_right):
    GPIO.output(MOTOR_PINS['motora_in1'], forward_left)
    GPIO.output(MOTOR_PINS['motora_in2'], backward_left)
    GPIO.output(MOTOR_PINS['motorb_in3'], forward_right)
    GPIO.output(MOTOR_PINS['motorb_in4'], backward_right)


# Motor control functions
def stop():
    set_motor_state(False, False, False, False)

def forward():
    set_motor_state(True, False, True, False)

def backward():
    set_motor_state(False, True, False, True)

def left():
    set_motor_state(True, False, False, True)

def right():
    set_motor_state(False, True, True, False)

try:
    while True:
        dist_central = distance(SENSOR_PINS['central']['trigger'], SENSOR_PINS['central']['echo'])
        dist_left = distance(SENSOR_PINS['left']['trigger'], SENSOR_PINS['left']['echo'])
        dist_right = distance(SENSOR_PINS['right']['trigger'], SENSOR_PINS['right']['echo'])

        print("Central: {:.2f} cm, Left: {:.2f} cm, Right: {:.2f} cm".format(dist_central, dist_left, dist_right))
        
        if dist_central < 20:
            print("Obstacle detected")
            stop()
            time.sleep(0.1)
            if dist_left < dist_right:
                right()
                print("Turning right")
                time.sleep(0.5)
            else:
                left()
                print("Turning left")
                time.sleep(0.5)
        else:
            if dist_left < 20:
                right()
                print("Adjusting right to maintain distance from left")
                time.sleep(0.1)
            elif dist_left > 30:
                left()
                print("Adjusting left to maintain distance from left")
                time.sleep(0.1)
            else:
                forward()
                print("Moving forward, maintaining left lane distance")

        time.sleep(0.05)

except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()
