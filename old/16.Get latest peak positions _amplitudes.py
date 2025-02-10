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
serialPort.write(b"P>")
x = serialPort.read(10000)
g=len(x)
print (g)
print (x)
# h=g-4
# y=x[0:h]
# time.sleep(0.1)  # Delay between communications
deserialized_bytes = np.frombuffer(x, dtype=np.uint16)
print (deserialized_bytes)
print (len(deserialized_bytes))
deserialized_x = np.reshape(deserialized_bytes, newshape= (len(deserialized_bytes)))
print (deserialized_x)
print (max(deserialized_bytes))
# spectrum_list=list(deserialized_x)
# spectrum_list=spectrum_list[3:]
# print('spectrum_unfiltered=',len(deserialized_x))  # prints the list values
# print('spectrum_filtered=',len(spectrum_list))  # prints the list values
# plt.plot(spectrum_list)
# plt.ylabel('some numbers')
# #plt.show()
serialPort.close()
time.sleep(0.1)  # Delay between communications

# importing the required module
