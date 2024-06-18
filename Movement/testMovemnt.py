import RPi.GPIO as GPIO
import time

# Setting Mode of board
GPIO.setmode(GPIO.BOARD)

# defining Motor pins
MOTOR_PINS = {
    'forward_left': 11,
    'forward_right': 15,
    'backward_left': 37,
    'backward_right': 13    
}

# Setup
for pin in MOTOR_PINS.values():
    GPIO.setup(pin, GPIO.OUT)


def cleargpios():
    print("clearing GPIO")
    for pin in MOTOR_PINS.values():
        GPIO.output(pin, False)
    #for sensor in SENSOR_PINS.values():
    #    GPIO.output(sensor['trigger'], False)
    print("All GPIOs CLEARED")
cleargpios()


