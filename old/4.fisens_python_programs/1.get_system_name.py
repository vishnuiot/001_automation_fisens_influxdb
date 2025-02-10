import time,serial

serialPort = serial.Serial(port = "com3", baudrate=3000000,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

print(serialPort.name)
serialPort.close()
time.sleep(0.1)  # Delay between communications
serialPort.open()
serialPort.write(b"?>")
x = serialPort.read(100) 
print(x) 
serialPort.close()
time.sleep(0.1)  # Delay between communications
