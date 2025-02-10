# import the pandas library
import pandas as pd
import numpy as np
# Dictionary of key pair values called data
dg=[]
x=np.linspace(800,900,1492)
for i in range (1):
    dg=pd.DataFrame()
    y=np.linspace(1000,1100,1492)
    print (x,y)
    df = pd.DataFrame ([x,y]).transpose()
    print (df)
    # pd.concat(df)

rows = []
for i in range(10):
    #  rows.append([i, i + 1])
     rows = [[i, i+1] for i in range(10)]
df = pd.DataFrame(rows, columns=["A", "B"])
print(df)

rows = []
for i in range(10):
    #  rows.append([i, i + 1])
     rows = [[i, i+1] for i in range(10)]
df = pd.DataFrame(rows, columns=["A", "B"])
print(df)

rows = []
for i in range(3):
     rows.append([i, i + 1])
print(rows)
for x in range(1):
    a=[1,2]
    b=[2,4]
    c=[a+b]
print (c)
d=[]
for i in range (5):
    a=[i]
    b=[i*i]
    c=[a,b]
    d=[d,c]
print (d)
a=pd.DataFrame(d)
print (a)