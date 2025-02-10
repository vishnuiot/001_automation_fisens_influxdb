import time,serial


serialPort = serial.Serial(port = "com3", baudrate=3000000,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
serialPort.close()
print(serialPort.name)
serialPort.close()
time.sleep(0.1)  # Delay between communications

serialPort.open()
serialPort.write(b"p?>")
x = serialPort.read(1000) 
print(x) 
print (type(x))
print (x.decode())  # removes byte string
serialPort.close()
time.sleep(0.1)  # Delay between communications
