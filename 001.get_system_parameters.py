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
# print("information on the serial port =",ser,"\n")
# # ser.close()
# # serial.open()
# serial.write(b"?>")
# x = serialPort.read(100) 
# print(x) 
# ser.close()
# time.sleep(0.1)  # Delay between communications

