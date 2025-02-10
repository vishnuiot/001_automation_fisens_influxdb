import time,serial
import numpy as np
import matplotlib.pyplot as plt

serialPort = serial.Serial(port = "com3", baudrate=3000000,parity=serial.PARITY_NONE,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
serialPort.close()
print(serialPort.name)
serialPort.close()
time.sleep(0.5)  # Delay between communications
for x in range(10):
    serialPort.open()
    # step 2: set integration time
    serialPort.write(b"iz,150000>")  # ( iz,x= 30-65,000,000)
    time.sleep(0.1)
    # step 3: Turn LED ON
    serialPort.write(b"LED,1>")# LED,(x=1)-ON;LED,(x=0)-OFF
    print('LED ON')
    time.sleep(0.1)  # Delay between communications
    # step 4: Start Global measurements
    serialPort.write(b"a>")
    # step5: Swithch on on-board calculation
    serialPort.write(b"OBB,0>")
    time.sleep(0.1)  # Delay between communications
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
    print('spectrum_unfiltered=',len(deserialized_x))  # prints the list values
    print('spectrum_filtered=',len(spectrum_list))  # prints the list values
    # wavelength_generation
    c=np.linspace(800,900,1492)
    g=list(c)
    wavelength = [round(num, 3) for num in g]


    time.sleep(0.1)  # Delay between communications
    serialPort.write(b"LED,0>")# LED,(x=1)-ON;LED,(x=0)-OFF
    print('LED OFF')

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

# importing the required module
