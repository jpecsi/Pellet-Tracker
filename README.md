# Pellet-Tracker     

## About      
Pellet-Tracker is a dedicated sensor that monitors the remaining level of pellets in the hopper of a pellet smoker.  The sensor relies on an ultrasonic hardware sensor to take measurements periodically and report the data back to home assistant.     


### Hardware     
- Raspberry Pi Zero W
- HC-SR04 Ultrasonic Sensor
- 2x Resistors (330 ohm 1/2w)     


### Software     
- Raspbian Lite
- Python     
- Home Assistant     



## Setup     

### Overview
1. Clone this repository somewhere on your system     
2. Move the 'sensor/' directory to '/opt/'     
3. Adjust the permissions on the '/opt/sensor/' directory:     
      `sudo chmod -R /opt/sensor`     
4. Configure the 'settings.conf' file, this file currently has sample data that will need to be adjusted for your environment     
5. Use crontab to execute the script periodically, I personally run it every 30 minutes:     

      `sudo crontab -e`          
      `*/30 * * * * /usr/bin/python /opt/sensor/sensor.py`     


### Calibration     
1. Mount the sensor in your smoker's hopper (to the underside of the lid, sensor should be pointing straight down into the hopper)     
2. Empty the hopper completely     
3. Execute the calibration script:     
      `python /opt/sensor/calibrate-sensor.py`     

This script will take a measurement of the hopper empty, ask you to fill it with pellets and takes a new measurement. The script will automatically update the configuration file (settings.conf) with the new values. 
     
          


## Notes     
- This might be a little hacky, but it works so far :)     
- This is still in breadboard form on my desk and not fully tested "in production"     
- I have noticed that I will occassioanlly get very random out of range measurements from the sensor, this may be due to frequency of measurements (in my testing), hopefully that won't be an issue in production     
- I will post drawings/designs of a case for this once I finish one     
- Pictures and detailed setup will be documented eventually on my blog