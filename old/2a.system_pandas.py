import time,serial
import  pandas as pd

serialPort = serial.Serial(port = "/dev/ttyUSB0", baudrate=3000000,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
serialPort.close()
print(serialPort.name)
serialPort.close()
time.sleep(0.1)  # Delay between communications

serialPort.open()
time.sleep(1)  # Delay between communications
serialPort.write(b"p?>")
x = serialPort.read(1000) 
#print(x)  # print serial port with byte value
# Remove byte string
print ('byte string removed') 
print (x.decode())  # removes byte string
g=(x.decode())
print (g.split('#'))
hh=g.split('#')
gg=len(hh)
for i in range(len(hh)):
    #print (i)
    print (hh[(i)])
serialPort.close()
time.sleep(0.1)  # Delay between communications


