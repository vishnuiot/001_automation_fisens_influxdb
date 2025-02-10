#!/home/vishnu/Documents/001_automation_fisens_influxdb/.venv/bin/python
# Important to specify working directory in os.chdir
import time,serial,sys,os
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
#date time for data frame
from datetime import datetime
# datetime object containing current date and time
now = datetime.now()
print(now)

#set absolute path for automated data saving into this directory
os.chdir("/home/vishnu/Documents/001_automation_fisens_influxdb")

serialPort = serial.Serial(port='/dev/ttyUSB0',baudrate= 3000000,parity=serial.PARITY_NONE,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
time.sleep(2)
serialPort.flushInput()
serialPort.flushOutput()
iter = 1
max = 10
if serialPort.isOpen():
    ### Step 1(10): Print device ID
    print ("Port Open =",serialPort.name,"\n")
    serialPort.write(b"?>")
    device_model = serialPort.read(20) 
    # print(device_model)
    # print (type(device_model))
    print (device_model.decode(),'\n')   # removes byte string  
    time.sleep(.1)                   # Delay between communications
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
    while iter<=1:
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
        # print('spectrum_unfiltered=',len(deserialized_x))  # prints the list values
        # print('spectrum_filtered=',len(spectrum_list))     # prints the list values
        # wavelength_generation
        c=np.linspace(800,840,1492)  # chanage between 800 to 900
        g=list(c)
        wavelength = [round(num, 3) for num in g]
        time.sleep(0.1)  # Delay between communications
        ### pandas data frame operations
        data={
        "wavelength":wavelength,
        "amplitude":spectrum_list}
        #load data into a DataFrame object:
        df = pd.DataFrame(data)
        # print(df)
        print(df.loc[df['amplitude'].idxmax()])
        # print(df.nlargest(10, ['amplitude']))   # prints top 10 values
        
        ### Influxdb operations
        # process data for ingestion into influxdB
        influxdb_df=df.loc[df['amplitude'].idxmax()]    
        print(influxdb_df)  
        tag1=list(influxdb_df.keys())
        print(tag1)
        
        value=influxdb_df.values.tolist()
        value = np.array(value)
        value=value.flatten().tolist()
        print (value)
        data_for_influxdb={'value':value,'tag1':tag1}
        # print(data_for_influxdb)
        df = pd.DataFrame(data_for_influxdb)
        print(df)  
         
        points=[]  
        for index,row in df.iterrows():
            point={'measurement':'cpu_parameters','tags':{'tag1':row['tag1']},'time':None,'fields':{'value':row['value'] }}
            points.append(point)  
              # Influxdb Section to upload wavelenth,amplitude
            import influxdb_client, os, time
            from influxdb_client import InfluxDBClient, Point, WritePrecision
            from influxdb_client.client.write_api import SYNCHRONOUS
            # Section to load token
            from dotenv import load_dotenv
            import os
            load_dotenv('apikey.env')
            user = os.getenv('INFLUXDB_TOKEN')
            #print (user)  prints api token - pre production  
            token = os.environ.get("INFLUXDB_TOKEN")
            org = "zurich"
            url = "http://localhost:8086"
            bucket="fbg"

            client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
            write_api = client.write_api(write_options=SYNCHRONOUS)
            write_api.write(bucket=bucket, org="zurich", record=point)  
          
        print(iter)
        iter += 1   
        ### Switch of SLED
    serialPort.write(b"LED,0>")# LED,(x=1)-ON;LED,(x=0)-OFF
    print('SLED OFF','\n')    
serialPort.close()


