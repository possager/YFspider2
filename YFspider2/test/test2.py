#_*_coding:utf-8_*_
import requests

str1 = '00012313111'
for i in range(3):

    str_index= str1.index('1',0,len(str1))
    str1=str1.replace('1',' ',1)
    print str_index

print str1