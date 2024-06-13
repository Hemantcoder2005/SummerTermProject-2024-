import RPi.GPIO as GPIO
import time

# Define GPIO pin numbers for the ultrasonic sensors
# Adjust these pin numbers according to your setup
sensors = [ 
    {'trigger': 16, 'echo': 18},
  {'trigger': 33, 'echo': 35},
     {'trigger': 38, 'echo': 40}
]

def setup():
    GPIO.setmode(GPIO.BCM)
    for sensor in sensors:
        GPIO.setup(sensor['trigger'], GPIO.OUT)
        GPIO.setup(sensor['echo'], GPIO.IN)

def check_sensor(sensor):
    GPIO.output(sensor['trigger'], False)
    time.sleep(0.01)  # Short delay to ensure previous pulse has ended

    # Send a 10us pulse to trigger
    GPIO.output(sensor['trigger'], True)
    time.sleep(0.00001)
    GPIO.output(sensor['trigger'], False)

    # Measure response time
    start_time = time.monotonic()
    pulse_start = 0
    pulse_end = 0

    # Wait for the echo to start
    while GPIO.input(sensor['echo']) == 0:
        pulse_start = time.monotonic()
        if pulse_start - start_time > 0.1:
            print("Sensor not detected - echo start timeout")
            return False

    # Wait for the echo to end
    while GPIO.input(sensor['echo']) == 1:
        pulse_end = time.monotonic()
        if pulse_end - pulse_start > 0.1:
            print("Sensor not detected - echo end timeout")
            return False

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    print(f"Sensor connected: Distance = {distance} cm")
    return True


def main():
    setup()
    for i, sensor in enumerate(sensors):
        print(f"Checking Sensor {i+1}")
        if not check_sensor(sensor):
            print(f"Sensor {i+1} is not properly connected.")
        else:
            print(f"Sensor {i+1} is working correctly.")

    GPIO.cleanup()

if __name__ == "__main__":
    main()
