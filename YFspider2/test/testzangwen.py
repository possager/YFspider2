#_*_coding:utf-8_*_
import requests


url='http://bod.asia/2017/12/%E0%BC%84%E0%BC%85%E0%BC%8D-%E0%BC%8D%E0%BC%B8%E0%BD%82%E0%BD%BC%E0%BD%84%E0%BC%8B%E0%BD%A6%E0%BC%8B%E0%BC%B8%E0%BD%A6%E0%BE%90%E0%BE%B1%E0%BD%96%E0%BD%A6%E0%BC%8B%E0%BD%98%E0%BD%82%E0%BD%BC%E0%BD%93/'
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
}


response=requests.get(url=url)
print response.text