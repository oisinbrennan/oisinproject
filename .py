import Adafruit_DHT as DHT                #imports dht for sensors
import RPi.GPIO as GPIO                   #imports gpio pin commands
from time import sleep                    #imports sleep command
from firebase import firebase             #imports firebase commands
              
GPIO.setmode(GPIO.BCM)                    #sets up gpio pins

GPIO.setup(23, GPIO.IN)                   #sets up input on pin 23

firebase = firebase.FirebaseApplication('https://getupsonyup-default-rtdb.firebaseio.com/',None)  #api key for my firebase database

peoplecount = 0                           #sets the peoplecount to 0 on startup

welcome = input("Welcome to the mask break calculator, do you wish to continue and start the program? Please type 'Y' for yes or anything else to kill the program")   #welcome message 

if welcome=="Y":
  
  sleep(0.5)
  while True:                               #everything after this loops 
      humid, temp = DHT.read_retry(DHT.DHT11, 4)                         #sets up humidity and temperature sensor
      #print(humid, temp)
      result = firebase.patch('/sensor/dht/', {'Temperature': temp, 'Humidity': humid})       #sends the results of the sensor to firebase
      sleep(1)

      sensor = GPIO.input(23)
      #print(sensor)


      if sensor ==1:
          #print("That is someone")
          sleep(1)
          peoplecount += 1
          result = firebase.patch('/sensor/', {'Number of People': peoplecount})
    
      elif sensor==0:
          #print("No one there.")
          sleep(1)
          result = firebase.patch('/sensor/', {'Number of People': peoplecount})
        
      print("The latest temperature was:")
      resulttemp = firebase.get('/sensor/dht/Temperature', None)
      print(resulttemp)
    
      sleep(.2)
    
      print("The latest humidity was:")
      resulthumid = firebase.get('/sensor/dht/Humidity', None)
      print(resulthumid)
    
      sleep(.2)
    
      print("The latest people count was:")
      resultpeep = firebase.get('/sensor/Number of People', None)
      print(resultpeep)
      sleep(.2)
    
      #resulttemp = 20
      #resulthumid = 5
      #resultpeep = 20
      #equation
      print("Now for the equation...")
      timeish = (((resultpeep*2)/(resulttemp*resulthumid))*3)
      print((round(timeish*10))/10)
      print("... hours until next mask break")
      
else:
  exit()
