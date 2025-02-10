import time,serial,sys
from serial import Serial

ser = serial.Serial('/dev/ttyUSB0', 3000000)
time.sleep(2)
if ser.isOpen():
    print ("Port Open =",ser.name,"\n")
    ser.write(b"?>")
    device_model = ser.read(15) 
    print(device_model)
    print (type(device_model))
    print (device_model.decode())  # removes byte string  
ser.close()

# ser = serial.Serial('/dev/ttyUSB0', 3000000)
# time.sleep(2)
# ser.write(b"?>")
# device_model = ser.read(100) 
# print(device_model)
# print (type(device_model))
# print (device_model.decode())  # removes byte string  


