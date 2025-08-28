import sys
print(sys.prefix)

#!/path/to/001_automation_fisens_influxdb/.venv/bin/python
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
