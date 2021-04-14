from datetime import datetime, timedelta
import math
day = '20210303'
first_day = '20200202'
first_day =datetime.strptime(first_day,'%Y%m%d')#.strftime('%Y%m%d')

day =datetime.strptime(day,'%Y%m%d')#.strftime('%Y%m%d')

interval = (day - first_day).days
intv = math.floor(interval /10)
for ii in range(0,10):
    print((first_day + timedelta(days=intv*ii)).strftime('%Y-%m') )

