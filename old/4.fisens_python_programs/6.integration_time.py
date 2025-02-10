import time,serial

serialPort = serial.Serial(port = "/dev/ttyUSB0", baudrate=3000000,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
print(serialPort.name)
serialPort.close()
time.sleep(0.1)  # Delay between communications
serialPort.open()
# step 1: get device ID
serialPort.write(b"?>")
x = serialPort.read(100) 
print(x) 
# step 2: set integration time
serialPort.write(b"iz,50000>")  # ( iz,x= 30-65,000,000)
time.sleep(1)
# step 3: Turn LED ON
serialPort.write(b"LED,1>")# LED,(x=1)-ON;LED,(x=0)-OFF
print('LED ON')
# step 4: get wavelength of each pixel
serialPort.write(b"WLL>")
x = serialPort.read(100000) 
print(x)
time.sleep(0.2)  # Delay between communications
# step 5: internally measured wavelengths
serialPort.write(b"aRWL?>")
x = serialPort.read(100000) 
print(x)
serialPort.write(b"LED,0>")# LED,(x=1)-ON;LED,(x=0)-OFF
print('LED OFF')
serialPort.close()
time.sleep(0.1)  # Delay between communications
