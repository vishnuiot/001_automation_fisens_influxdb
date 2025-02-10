import time,serial,sys
# import serial
# import time
from serial import Serial



ser = serial.Serial('/dev/ttyUSB0', 3000000)
time.sleep(2)
if ser.isOpen():
    print ("Port Open")
ser.close()

ser = serial.Serial('/dev/ttyUSB0', 3000000)
# print(serialPort.name)
# serialPort.close()
# time.sleep(0.1)  # Delay between communications
# serialPort.open()
# serialPort.write(b"?>")
# x = serialPort.read(100) 
# print(x) 
# serialPort.close()
# time.sleep(0.1)  # Delay between communications

