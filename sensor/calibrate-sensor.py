# Libraries
import configparser
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

# Calibration Settings
empty_hopper = config['calibration']['empty']
full_hopper = config['calibration']['full']




# ========== FUNCTIONS ========== #

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
    final = round(avg,2)

    return final




# ========== MAIN ========== #
if __name__ == '__main__':

    raw_input('Press [ENTER] to take EMPTY HOPPER measurement')
    empty_measurement = calc_remaining()

    raw_input('Press [ENTER] to take FULL HOPPER measurement')
    full_measurement = calc_remaining()

    print ""
    print "Empty Measurement: " + str(empty_measurement)
    print "Full Measurement: " + str(full_measurement)
    print ""
    print "Writing to configuration..."
    config.set('calibration','empty',str(empty_measurement))
    config.set('calibration','full',str(full_measurement))
    
    with open('settings.conf', 'wb') as configfile:
	config.write(configfile)


    print "Update Complete!"
    GPIO.cleanup()





