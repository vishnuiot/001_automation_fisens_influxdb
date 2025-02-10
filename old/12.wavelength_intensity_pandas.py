import time,serial
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
#to get the current working directory
directory = os.getcwd()
print(directory)
# step 1: set serial data parameters
serialPort = serial.Serial(port = "com3", baudrate=3000000,parity=serial.PARITY_NONE,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
serialPort.close()
print(serialPort.name)
serialPort.close()
time.sleep(0.1)  # Delay between communications
serialPort.open()
 
# step 2: set integration time
serialPort.write(b"iz,150000>")  # ( iz,x= 30-65,000,000)
time.sleep(0.15)
# step 3: Turn LED ON
serialPort.write(b"LED,1>")# LED,(x=1)-ON;LED,(x=0)-OFF
print('LED ON')
time.sleep(0.1)  # Delay between communications
# step 4: Start Global measurements
serialPort.write(b"a>")
# step5: Swithch on on-board calculation
serialPort.write(b"OBB,0>")
time.sleep(0.1)  # Delay between communications

# step6: wavelength_generation
c=np.linspace(800,900,1492)
g=list(c)
wavelength = [round(num, 3) for num in g]
df1=pd.DataFrame(wavelength)
df1.columns=['wavelength']
# step7: run empty scan to flush data buffer
for i in range(1):
    serialPort.write(b"s>")
    x = serialPort.read(10000)
# step8: data acquisition begins
for i in range(5):
    # step6: Get spectrum
    serialPort.write(b"s>")
    x = serialPort.read(10000)
    g=len(x)
    h=g-4
    y=x[0:h]
    #print (len(y))
    #time.sleep(0.1)  # Delay between communications
    deserialized_bytes = np.frombuffer(y, dtype=np.uint16)
    deserialized_x = np.reshape(deserialized_bytes, newshape=(1495))
    #print (deserialized_x)
    spectrum_list=list(deserialized_x)
    spectrum_list=spectrum_list[3:]
            # print('spectrum_unfiltered=',len(deserialized_x))  # prints the list values
            # print('spectrum_filtered=',len(spectrum_list))  # prints the list values
    #Pandas data frame
    df2=pd.DataFrame(spectrum_list)
    df1.insert(i+1, "Intensity "+str(i), df2, allow_duplicates=True)
    # step7: plot spectrum
    plt.plot(wavelength,spectrum_list)
    # naming the x axis,yaxis&plot title
    plt.xlabel('wavelength (nm)')
    plt.ylabel('Intensity (a.u)')
    plt.title('FBG Spectrum!')
    #plt.show()
    print ('counter =',str(i))
print (df1)
time.sleep(0.1)  # Delay between communications
serialPort.write(b"LED,0>")# LED,(x=1)-ON;LED,(x=0)-OFF
print('LED OFF')
serialPort.close()

time.sleep(0.1)  # Delay between communications
# step8: plot Data analysis
print (df1)

# step 9 : save dataframe as csv
df1.to_csv('raw_data.csv', index=False)

# Step 10 : Begin data analysis

column=df1['Intensity 0']
max_value = column.max()
print (max_value)
max_index = column.idxmax()
print(max_index)

#max_wavelength=df1[max_index,'wavelength']
max_wavelength=df1.loc[max_index, 'wavelength']
print ('wavelength = ',max_wavelength)

# column = df1[1]
# max_value = column.max()
# print (max_value)


