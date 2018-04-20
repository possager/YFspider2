import re



def deal_ftchinese_url(url):
    Re_match=re.compile(r'www\.ftchinese\.com\/story\/\d*')
    is_suit=Re_match.findall(url)
    print (is_suit)
    if is_suit:
        return 'http://'+is_suit[0]+'?full=y'





if __name__ == '__main__':
    url1='http://www.ftchinese.com/story/987654321'

    print (deal_ftchinese_url(url1))