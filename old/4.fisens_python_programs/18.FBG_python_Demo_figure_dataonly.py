# Author  : Dr. Vishnu Prasad 
# Project : Customer request code - G18922021
# Version : 1.5
# Security class : none
import time,serial
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
#to get the current working directory
directory = os.getcwd()
print(directory)

serialPort = serial.Serial(port = "COM3", baudrate=3000000,parity=serial.PARITY_NONE,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
serialPort.close()
print(serialPort.name)
serialPort.close()
time.sleep(0.1)  # Delay between communications
serialPort.open()
 
# step 2: set integration time
serialPort.write(b"iz,200000>")  # ( iz,x= 30-65,000,000)
time.sleep(0.15)
# step 3: Turn LED ON
serialPort.write(b"LED,1>")# LED,(x=1)-ON;LED,(x=0)-OFF
print('SLED ON')
time.sleep(0.1)  # Delay between communications
# step 4: Start Global measurements
serialPort.write(b"a>")
# step5: Swithch on on-board calculation
serialPort.write(b"OBB,0>")
time.sleep(0.1)  # Delay between communications
# Flush serial data in buffer - output is not recorded here

# wavelength_generation
c=np.linspace(800,900,1492)
g=list(c)
wavelength = [round(num, 3) for num in g]

for i in range(1):
    serialPort.write(b"s>")
    x = serialPort.read(10000)
    time.sleep(0.2)  # Delay between communications
# data acquisition begins
for i in range(3):
    # step6: Get spectrum
    serialPort.write(b"s>")
    x = serialPort.read(10000)
    g=len(x)
    h=g-4
    y=x[0:h]
    print (len(y))
    time.sleep(0.2)  # Delay between communications
    deserialized_bytes = np.frombuffer(y, dtype=np.uint16)
    deserialized_x = np.reshape(deserialized_bytes, newshape=(1495))
    #print (deserialized_x)
    spectrum_list=list(deserialized_x)
    spectrum_list=spectrum_list[3:]
    # print('spectrum_unfiltered=',len(deserialized_x))  # prints the list values
    # print('spectrum_filtered=',len(spectrum_list))  # prints the list values
    #Pandas data frame
    df = pd.DataFrame (wavelength,columns = ['wavelength'])
    df = pd.DataFrame ([wavelength,spectrum_list]).transpose()
    df.columns=['wavelength','Amplitude']
    maxamplitude=df['Amplitude'].max()
    maxindex=df['Amplitude'].idxmax()
    max_wavelength=df['wavelength'].iloc[maxindex]
    print (df)
    print ('index=',maxindex,'Max_amplitude=',maxamplitude,'max_wavelength=',max_wavelength)
    # step7: plot spectrum
    plt.plot(wavelength,spectrum_list)
    # naming the x axis,yaxis&plot title
    plt.xlabel('wavelength (nm)')
    plt.ylabel('Intensity (a.u)')
    plt.title('FBG Spectrum !!')
    plt.show()
    plt.close("all")
    
    print ("scan no =",i)

    # max_index =df.spectrum_list.max()
    # print (max_index)
time.sleep(0.1)  # Delay between communications
serialPort.write(b"LED,0>")# LED,(x=1)-ON;LED,(x=0)-OFF
print('SLED OFF')
serialPort.close()

time.sleep(0.1)  # Delay between communications
# importing the required module
