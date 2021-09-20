# Libraries
import configparser
import paho.mqtt.client as mqtt
from re import X
import RPi.GPIO as GPIO
import time


# ========== LOAD CONFIG ========== #
config = configparser.ConfigParser()
config.read('/opt/sensor/settings.conf')

# GPIO Settings
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO_TRIGGER = config.getint("hardware", "sensor_trigger")
GPIO_ECHO = config.getint("hardware", "sensor_echo")
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

# MQTT Settings
mqtt_broker_address = config['mqtt']['broker_address']
mqtt_broker_port = config['mqtt']['broker_port']
mqtt_level_topic = config['mqtt']['level_topic']
mqtt_pellet_topic = config['mqtt']['pellet_topic']
mqtt_user = config['mqtt']['user']
mqtt_pass = config['mqtt']['pass']

# Calibration Settings
empty_hopper = config['calibration']['empty']
full_hopper = config['calibration']['full']

# Miscellaneous
pellet_type = config['misc']['current_pellets']



# ========== FUNCTIONS ========== #

# Function: Send Data to MQTT
def report(p):
    client = mqtt.Client("smoker")
    client.username_pw_set(username=mqtt_user,password=mqtt_pass)
    client.connect(mqtt_broker_address)
    client.publish(mqtt_level_topic,str(p))
    client.publish(mqtt_pellet_topic,pellet_type)
    print "Hopper Level: " + str(p) + "%"
    print "Pellets: " + pellet_type

# Function: Take Measurement of Hopper Level
def take_measurement():
    # Set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # Set Trigger to LOW (slight delay)
    #time.sleep(0.00001)
    time.sleep(0.1)
    GPIO.output(GPIO_TRIGGER, False)
 
    # Timer
    StartTime = time.time()
    StopTime = time.time()
 
    # Set StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # Set StopTime
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # Get time difference
    TimeElapsed = StopTime - StartTime

    # Calculate measurement (cm)
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    hopper_level = (TimeElapsed * 34300) / 2
 
    return hopper_level


# Function: Calculate Percentage of Pellets Remaining
def calc_remaining():

    # Setup variables
    i = 0
    avg = 0

    # Grab several measurements and get the average
    while (i < 9):

        # Skip the first measurement, sometimes the first measurement is junk
        if (i == 0 ):
            take_measurement()
            i+=1

        # Add up the measurements to get the average
        else: 
            x = take_measurement()
            avg = avg+x
            i+=1


    # Calculate
    avg = avg/8
    max = float(full_hopper)
    min = float(empty_hopper)
    p = ((avg-min) * 100) / (max-min)
    final = round(p,0)

    # Correct measurements out of range
    if final < 0:
	    final = 0
    elif final > 100:
	    final = 100    

    return final




# ========== MAIN ========== #
if __name__ == '__main__':
        level_remaining = calc_remaining()
        report(level_remaining)
        GPIO.cleanup()





