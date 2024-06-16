import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

SENSOR_PINS = {
    'central': {'trigger': 16, 'echo': 18},
    'right': {'trigger': 33, 'echo': 35},
    'left': {'trigger': 38, 'echo': 40}
}
for sensor in SENSOR_PINS.values():
    GPIO.setup(sensor['trigger'], GPIO.OUT)
    GPIO.setup(sensor['echo'], GPIO.IN)

def cleargpios():
    print("clearing GPIO")
    for sensor in SENSOR_PINS.values():
        GPIO.output(sensor['trigger'], False)
    print("All GPIOs CLEARED")
def measure_distance(trigger, echo):
    GPIO.output(trigger, False)
    time.sleep(0.2)
    GPIO.output(trigger, True)
    time.sleep(0.00001)
    GPIO.output(trigger, False)
    
    start, stop = time.time(), time.time()
    while GPIO.input(echo) == 0:
        # print("trig1: ", GPIO.input(16))
        print("echo1: ", GPIO.input(18))
        start = time.time()
    while GPIO.input(echo) == 1:
        # print("trig2: ", GPIO.input(16))
        # print("-------------------echo2---------------------")
        stop = time.time()
        # print(stop - start)
    print("trig: ", GPIO.input(16))
    print("echo:", GPIO.input(18))
    elapsed = stop - start
    distance = elapsed * 34000 / 2

    return distance

while True:
    try:
        

        print('\n')
        print("Central = ",measure_distance(16,18))
        print("right = ",measure_distance(33,35))
        print("left = ",measure_distance(38,40))
        print('\n')
        
        print(GPIO.input(16))
        # if GPIO.input(18) == GPIO.LOW:
        #     print("Sensor is connected.")
        # else:
        #     print("Sensor is disconnected!")
        #     cleargpios()
        #     break
        # time.sleep(2)
    except KeyboardInterrupt:
        cleargpios()
        break
