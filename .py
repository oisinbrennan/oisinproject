import Adafruit_DHT as DHT                #imports dht for sensors
import RPi.GPIO as GPIO                   #imports gpio pin commands
from time import sleep                    #imports sleep command
from firebase import firebase             #imports firebase commands
              
GPIO.setmode(GPIO.BCM)                    #sets up gpio pins

GPIO.setup(23, GPIO.IN)                   #sets up input on pin 23

firebase = firebase.FirebaseApplication('https://getupsonyup-default-rtdb.firebaseio.com/',None)  #api key for my firebase database

peoplecount = 0                           #sets the peoplecount to 0 on startup

welcome = input("Welcome to the mask break calculator, do you wish to continue and start the program? Please type 'Y' for yes or anything else to kill the program")   #welcome message 

if welcome=="Y":                          #starts the program if requested
  
  sleep(0.5)
  while True:                               #everything after this loops 
      humid, temp = DHT.read_retry(DHT.DHT11, 4)                         #sets up humidity and temperature sensor
      result = firebase.patch('/sensor/dht/', {'Temperature': temp, 'Humidity': humid})       #sends the results of the sensor to firebase
      sleep(1)

      sensor = GPIO.input(23)              #gets light sensor data

      if sensor ==1:                       #if positive signal sent from sensor
          sleep(1)
          peoplecount += 1                 #adds one to the peoplecount
          result = firebase.patch('/sensor/', {'Number of People': peoplecount})              #sends the new peoplecount to the firebase
    
      elif sensor==0:                     #if negative singal sent from sensor
          sleep(1)
          result = firebase.patch('/sensor/', {'Number of People': peoplecount})              #semds the current peoplecount to firebase
        
      print("The latest temperature was:")
      resulttemp = firebase.get('/sensor/dht/Temperature', None)                         #gets data from firebase, temperature
      print(resulttemp)                                                                  #prints this data
    
      sleep(.2)
    
      print("The latest humidity was:")
      resulthumid = firebase.get('/sensor/dht/Humidity', None)                           #gets data from firebase, humidity
      print(resulthumid)                                                                 #prints this data
     
      sleep(.2)
    
      print("The latest people count was:")
      resultpeep = firebase.get('/sensor/Number of People', None)                        #gets data from firebase, light sensor
      print(resultpeep)                                                                  #prints this data
      sleep(.2)
    
      print("Now for the equation...")
      timeish = (((resultpeep*2)/(resulttemp*resulthumid))*3)                            #equation for the final output made from several data points
      print((round(timeish*10))/10)                                                      #second part to equation and prints it
      print("... hours until next mask break")                                           #repeats the process
      
else:                               #otherwise if answer is not yes, program terminates
  exit()
