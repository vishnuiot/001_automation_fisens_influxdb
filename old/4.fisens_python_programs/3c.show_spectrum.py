import time,serial
import numpy as np
import matplotlib.pyplot as plt

serialPort = serial.Serial(port = "com3", baudrate=3000000,parity=serial.PARITY_NONE,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
serialPort.close()
print(serialPort.name)
serialPort.close()
time.sleep(0.1)  # Delay between communications
serialPort.open()
serialPort.write(b"s>")
x = serialPort.read(10000)
g=len(x)
h=g-4
y=x[0:h]
time.sleep(0.1)  # Delay between communications
deserialized_bytes = np.frombuffer(y, dtype=np.uint16)
deserialized_x = np.reshape(deserialized_bytes, newshape=(1495))
print (deserialized_x)
spectrum_list=list(deserialized_x)
spectrum_list=spectrum_list[3:]
print('spectrum_unfiltered=',len(deserialized_x))  # prints the list values
print('spectrum_filtered=',len(spectrum_list))  # prints the list values
plt.plot(spectrum_list)
plt.ylabel('some numbers')
plt.show()
serialPort.close()
time.sleep(0.1)  # Delay between communications

# importing the required module
