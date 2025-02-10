import time,serial
import numpy as np

serialPort = serial.Serial(port = "com3", baudrate=3000000,parity=serial.PARITY_NONE,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
serialPort.close()
print(serialPort.name)
serialPort.close()
time.sleep(0.1)  # Delay between communications

serialPort.open()
serialPort.write(b"s>")
x = serialPort.read(10000)
#print(x.decode()) 
g=len(x)
h=g-4
print(h)
y=x[0:h]
print(y)
print (type(y)) # without the ende

#print (y.hex(':',1))

# # a= list(bytes(y))
# # print (a)
# # print (type(a))
# # a=int.from_bytes(a, byteorder='big')
# # print (a)
# # print(type(a))
# hexadecimal_string =y.hex()
# print (hexadecimal_string)

# g=int(hexadecimal_string,base=16)
# print (g)

serialPort.close()
time.sleep(0.1)  # Delay between communications


import numpy as np

#x = np.array([[0, 1], [2, 3]], np.uint16)
#bytes = x.tobytes()
#print (bytes)
#assert len(bytes) == 8

deserialized_bytes = np.frombuffer(y, dtype=np.uint16)
deserialized_x = np.reshape(deserialized_bytes, newshape=(1495))
print (deserialized_x)
#assert np.array_equal(x, deserialized_x)
