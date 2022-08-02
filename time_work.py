import datetime
from datetime import datetime
import time
from time import strftime,localtime
timenow = time.ctime()
import re

date_stamp = strftime("%d %b %Y",localtime())

time_stamp2 = strftime(time.ctime())

print(date_stamp)
print(time_stamp2)


time_stamp = datetime.now()
# mat = re.match(r'(.+)\.(.+)', str(time_stamp), re.M|re.I)

print(time_stamp)
# print(mat.group(1))

hour_and_minute = datetime.now().strftime("%H:%M")
print(hour_and_minute)

#"Thu Jul 21 08:46:48 2022"
