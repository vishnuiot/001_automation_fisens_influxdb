import time,serial,sys
import serial
import time



ser = serial.Serial('/dev/ttyACM0', 3000000)
time.sleep(2)
if ser.isOpen():
    print ("Port Open")
print(ser.write("START\n")) 
ser.close()
