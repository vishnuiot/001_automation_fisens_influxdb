import time,serial
#import numpy as np

serialPort = serial.Serial(port = "com3", baudrate=3000000,parity=serial.PARITY_NONE,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
serialPort.close()
print(serialPort.name)
serialPort.close()
time.sleep(0.1)  # Delay between communications

serialPort.open()
serialPort.write(b"s>")
x = serialPort.read(5000) 
print(x) # with ende
#print (type(x))
a= (int.from_bytes(x,"big"))
print (a)
#print(x.decode()) 
# g=len(x)
# print(g)
# h=g-4
# print(h)
# y=x[0:h]
# print(y)
# print (type(y))

# a= list(bytes(y))
# print (a)
# print (type(a))                                                                                                                                                                        
# a=int.from_bytes(a, byteorder='big')
# print (a)
# print(type(a))
#hexadecimal_string =y.hex()
#print (hexadecimal_string)

#g=int(hexadecimal_string,base=16)
#print (g)

serialPort.close()
time.sleep(0.1)  # Delay between communications