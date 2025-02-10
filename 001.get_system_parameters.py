import time,serial,sys
from serial import Serial
#increase the limit for string conversion
import sys
sys.set_int_max_str_digits(0)

serialPort = serial.Serial(port='/dev/ttyUSB0',baudrate= 3000000,parity=serial.PARITY_NONE,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
time.sleep(2)
serialPort.flushInput()
serialPort.flushOutput()
if serialPort.isOpen():
    print ("Port Open =",serialPort.name,"\n")
    serialPort.write(b"?>")
    device_model = serialPort.read(20) 
    print(device_model)
    print (type(device_model))
    print (device_model.decode())   # removes byte string  
    time.sleep(1)                   # Delay between communications
    serialPort.write(b"s>")         #get spectrum
    x = serialPort.read(10000) 
    print(x)
    #print (type(x))
    a= (int.from_bytes(x,"big"))
    print (a)
serialPort.close()



# ser = serial.Serial('/dev/ttyUSB0', 3000000)
# time.sleep(2)
# ser.write(b"?>")
# device_model = ser.read(100) 
# print(device_model)
# print (type(device_model))
# print (device_model.decode())  # removes byte string  

#  SerialPort.Parity = Parity.None;
#  SerialPort.StopBits = StopBits.One;
#  SerialPort.DataBits = 8;
#  SerialPort.Handshake = Handshake.None;
#  SerialPort.RtsEnable = true;
#  SerialPort.ReadBufferSize = 32768;


