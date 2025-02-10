import time,serial,sys
from serial import Serial
#increase the limit for string conversion
import sys
sys.set_int_max_str_digits(0)
# import numpy for data operations
import numpy as np
#import matplotlib for data visualization
import matplotlib.pyplot as plt
#import pandas for data processing
import pandas as pd

serialPort = serial.Serial(port='/dev/ttyUSB0',baudrate= 3000000,parity=serial.PARITY_NONE,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
time.sleep(2)
serialPort.flushInput()
serialPort.flushOutput()
if serialPort.isOpen():
    ### Step 1(10): Print device ID
    print ("Port Open =",serialPort.name,"\n")
    serialPort.write(b"?>")
    device_model = serialPort.read(20) 
    # print(device_model)
    # print (type(device_model))
    print (device_model.decode(),'\n')   # removes byte string  
    time.sleep(1)                   # Delay between communications
    ### step 2(10): set integration time
    serialPort.write(b"iz,60,000")  # ( iz,x= 30-65,000,000)
    time.sleep(0.1)
    ### step 3(10): Turn LED ON
    serialPort.write(b"LED,1>")# LED,(x=1)-ON;LED,(x=0)-OFF
    print('SLED ON','\n')
    time.sleep(0.1)  # Delay between communications
    ### step 4: Start Global measurements
    serialPort.write(b"a>")    
    ### step5: Swithch on on-board calculation
    serialPort.write(b"OBB,0>")
    time.sleep(0.1)  # Delay between communications
    ### step6: Get spectrum
    serialPort.write(b"s>")         #get spectrum
    x = serialPort.read(10000) 
    # print(x,'\n')
    # print (type(x),'\n')
    a= (int.from_bytes(x,"big"))
    # print (a)
    ## raw data processing
    g=len(x)
    h=g-4
    y=x[0:h]
    time.sleep(0.1)                 # Delay between communications
    deserialized_bytes = np.frombuffer(y, dtype=np.uint16)
    deserialized_x = np.reshape(deserialized_bytes, shape=(1495))
    print (deserialized_x)
    spectrum_list=list(deserialized_x)
    spectrum_list=spectrum_list[3:]
    # print(spectrum_list)  
    print('spectrum_unfiltered=',len(deserialized_x))  # prints the list values
    print('spectrum_filtered=',len(spectrum_list))     # prints the list values
    # wavelength_generation
    c=np.linspace(800,900,1492)
    g=list(c)
    wavelength = [round(num, 3) for num in g]
    time.sleep(0.1)  # Delay between communications
    ### Switch of SLED
    serialPort.write(b"LED,0>")# LED,(x=1)-ON;LED,(x=0)-OFF
    print('SLED OFF','\n')
    
    ### Plotting the data
    plt.plot(wavelength,spectrum_list)
    # naming the x axis
    plt.xlabel('wavelength (nm)')
    # naming the y axis
    plt.ylabel('Intensity (a.u)')
    
    # giving a title to my graph
    plt.title('My first graph!')
    plt.show()
    serialPort.close()
    time.sleep(0.1)  # Delay between communications 


serialPort.close()

