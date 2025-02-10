# prints wavelenth pixel list
import time,serial
import numpy as np
import matplotlib.pyplot as plt
serialPort = serial.Serial(port = "com3", baudrate=3000000,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
serialPort.close()
print(serialPort.name)
serialPort.close()
time.sleep(0.1)  # Delay between communications

serialPort.open()
serialPort.write(b"WLL>")
x = serialPort.read(10000) 
#print(x) 
g=len(x)
h=g-4
y=x[0:h]
time.sleep(0.1)  # Delay between communications
print (len(y))
deserialized_bytes = np.frombuffer(y, dtype=np.uint16)
deserialized_x = np.reshape(deserialized_bytes, newshape=(2990))
print (deserialized_x)
wavelength_list=list(deserialized_x)
#print (wavelength_list)
plt.plot(wavelength_list)
plt.ylabel('some numbers')
#plt.show()
serialPort.close()
time.sleep(0.1)  # Delay between communications