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
serialPort.write(b"LED,1>")# LED,(x=1)-ON;LED,(x=0)-OFF
print('LED ON')
serialPort.write(b"WLL>")
x = serialPort.read(100000) 
print(x)
time.sleep(0.2)  # Delay between communications
serialPort.write(b"LED,0>")# LED,(x=1)-ON;LED,(x=0)-OFF
print('LED OFF')
serialPort.close()
time.sleep(0.1)  # Delay between communications
