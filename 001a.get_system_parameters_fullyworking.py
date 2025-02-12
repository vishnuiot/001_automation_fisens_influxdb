import time,serial,sys
from serial import Serial
#increase the limit for string conversion
import sys
sys.set_int_max_str_digits(0)
# import numpy for data operations
import numpy as np
#import matplotlib for data visualization
import matplotlib.pyplot as plt

serialPort = serial.Serial(port='/dev/ttyUSB0',baudrate= 3000000,parity=serial.PARITY_NONE,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
time.sleep(2)
serialPort.flushInput()
serialPort.flushOutput()
if serialPort.isOpen():
    print ("Port Open =",serialPort.name,"\n")
    serialPort.write(b"?>")
    device_model = serialPort.read(20) 
    print(device_model)
    print (type(device_model))
    print (device_model.decode())   # removes byte string  
    time.sleep(1)                   # Delay between communications
    serialPort.write(b"s>")         #get spectrum
    x = serialPort.read(10000) 
    print(x,'\n')
    print (type(x),'\n')
    a= (int.from_bytes(x,"big"))
    print (a)
    ## raw data processing
    g=len(x)
    h=g-4
    y=x[0:h]
    time.sleep(0.1)                 # Delay between communications
    deserialized_bytes = np.frombuffer(y, dtype=np.uint16)
    deserialized_x = np.reshape(deserialized_bytes, newshape=(1495))
    print (deserialized_x)
    spectrum_list=list(deserialized_x)
    spectrum_list=spectrum_list[3:]
    print(spectrum_list)  
    print('spectrum_unfiltered=',len(deserialized_x))  # prints the list values
    print('spectrum_filtered=',len(spectrum_list))     # prints the list values
    plt.plot(spectrum_list)
    plt.ylabel('some numbers')
    plt.show() 
    ###get wavelength values
    serialPort.write(b"WLL>")                           
    x = serialPort.read(10000) 
    #print(x) 
    g=len(x)
    h=g-4
    y=x[0:h]
    time.sleep(0.1)                                     # Delay between communications
    print (len(y))
    deserialized_bytes = np.frombuffer(y, dtype=np.uint16)
    deserialized_x = np.reshape(deserialized_bytes, newshape=(2990))
    print (deserialized_x)
    wavelength_list=list(deserialized_x)
    print (wavelength_list)  
    
    plt.plot(wavelength_list)
    plt.ylabel('some numbers')  
    # plt.show()      ## plot y vs wavelenth(x axis)
    # serialPort.write(b"LED,1>")# LED,(x=1)-ON;LED,(x=0)-OFF   # LED Section
    # print('LED ON')
    # serialPort.write(b"WLL>")
    # x = serialPort.read(100000) 
    # print(x)
    # time.sleep(0.2)  # Delay between communications
    # serialPort.write(b"LED,0>")# LED,(x=1)-ON;LED,(x=0)-OFF
    # print('LED OFF')
    # serialPort.close()
    # time.sleep(0.1)  # Delay between communications
serialPort.close()

