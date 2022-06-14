import RPi.GPIO as GPIO
import board
import busio
import adafruit_am2320
import time
from websocket import create_connection

#sets up all the equipment
MSensor = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(6,GPIO.OUT)
GPIO.setup(MSensor,GPIO.IN)

i2c = busio.I2C(board.SCL, board.SDA)
ws = create_connection("ws://172.20.10.3:3001")

#meassure data and store it in data
def MessureData():
   data = ''
   if GPIO.input(MSensor):
      data = data + "Dry"
      GPIO.output(27,True)
   else:
      data = data + "Wet"
      GPIO.output(27,False)
   sensor = adafruit_am2320.AM2320(i2c)
   data = data + ' Humidity: {0}%'.format(sensor.relative_humidity)
   data = data + ' Temperature: {0}C'.format(sensor.temperature)
   return data
   
   
#sending data to webServer and recieves a message   
def DataToServer(DataMeassured):
   ws.send(DataMeassured)
   print (ws.recv())


   
while True:
   
   #for testing purpose
   testPrompt = input("y/n")
   
   #the program fetches meassured data and sends it to the DataToServer Function
   if testPrompt == "y":
      #waiting a hour to execute and
      #time.sleep(3600)
      GPIO.output(6,False)
      time.sleep(2)
      DataMeassured = MeassureData()
      DataToServer(DataMeassured)
      GPIO.output(6,True)
   if testPrompt == "n":
      break;

ws.close()


   

