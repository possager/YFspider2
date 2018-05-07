import time


timestr1='1970-01-01 08:00:02'
timetuple=time.strptime(timestr1,'%Y-%m-%d %H:%M:%S')

timestamp=time.mktime(timetuple)
print str(int(timestamp*1000))