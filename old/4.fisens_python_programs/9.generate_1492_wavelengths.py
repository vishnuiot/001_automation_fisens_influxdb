import numpy as np
c=np.linspace(800,900,1492)
print (c)
print (len(c))
print (type(c))
g=list(c)
print (g)
round_to_tenths = [round(num, 3) for num in g]
print(round_to_tenths)
print (len(round_to_tenths))

