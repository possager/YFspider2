import re




Re_find=re.compile('http:\/\/en\.boxun\.com\/\d{4}\/\d{2}\/\d{2}\/.*?\/(.+)')
data=Re_find.findall('http://en.boxun.com/2015/08/06/set-up-police-offices-in-all-major-websites-and-internet-companies/')

if data:
    print data