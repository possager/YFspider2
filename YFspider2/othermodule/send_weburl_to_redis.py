#_*_coding:utf-8_*_
import redis
import requests
import random

#
redis1=redis.StrictRedis(host='127.0.0.1',port=6379,db=1)

all_website_key= redis1.keys('*')


web_begin_url_config={
    'kirti92':'http://www.kirti92.org/',
    'tibetanwomen':'http://tibetanwomen.org/',
    'tchrd':'http://tchrd.org/chinese/',
    'uyghurcongress':'http://www.uyghurcongress.org/cn/',
    'CFTchinese':'http://www.ftchinese.com/',#这个进去就有广告
    'chushigangdrug':'http://www.chushigangdrug.ch/',
    'middleway':'http://woeser.middle-way.net/',
    'tibetsun':'https://www.tibetsun.com/',
    'sherig':'http://www.sherig.org/tb/',
    'xiongdeng':'http://xiongdeng.com/',#这个分中英文，这个是中文的
    'secretchina':'https://www.secretchina.com/',#?
    'tibetsociety':'http://www.tibetsociety.com/',
    'dhokhamchushigangdrug':'http://dhokhamchushigangdrug.com/',
    'tibetanentrepreneurs':'http://tibetanentrepreneurs.org/',
    'khabdha':'http://www.khabdha.org/',
    'AtcOrgAu':'http://www.atc.org.au/',
    'dorjeshugden':'http://www.dorjeshugden.com/',#多杰雄登英文版
    'chinesepen':'http://www.chinesepen.org/',
    'minghui':'http://www.minghui.org/',
    'tibetanyouthcongress':'https://www.tibetanyouthcongress.org/',
    'studentsforafreetibet':'https://www.studentsforafreetibet.org/media-center/',
    'chinainperspective':'http://chinainperspective.com/',
    'radiosoh':'http://radiosoh.com/',#希望之声英文版，分中英文
    'chinaaid':'http://www.chinaaid.net/',
    'tibetswiss':'http://www.tibetswiss.ch/index-bo.html',
    'savetibet':'http://www.savetibet.org/#',
    'tibetwomenBo':'http://tibetanwomen.org/bo/',
    'tibetanparliament':'http://tibetanparliament.org/',
    'kagyuoffice':'https://www.kagyuoffice.org.tw/news?start=100',#这个不是网站的主页
    'dalailamaworld':'http://www.dalailamaworld.com/',
    'xizang_zhiye':'http://xizang-zhiye.org/',
    'tibetexpress':'http://tibetexpress.net/',
    'liaowangxizang':'https://liaowangxizang.net/',
    'sputniknews':'http://sputniknews.cn/',
    'tibettimes':'http://tibettimes.net/',
    'phayul':'http://www.phayul.com/',
    'potalapost':'http://potalapost.com/',
    'nytimes':'https://cn.nytimes.com/',
    'aboluowang':'http://www.aboluowang.com/',
    'kearyhuang':'https://kearyhuang.wordpress.com/',
    'epochtimes':'http://www.epochtimes.com',
    'boxun':'https://boxun.com/',
    'dwnews':'http://news.dwnews.com/',
    'cn_rfi_fr':'http://cn.rfi.fr/',
    'bbc_com_zhongwen_simp':'http://www.bbc.com/zhongwen/simp',
    'dw':'http://www.dw.com/',
    'voachinese':'https://www.voachinese.com',
    'rfa_org':'https://www.rfa.org/mandarin/',
    'thetibetpost':'http://www.thetibetpost.com/en/',
    'vot_org':'http://www.vot.org/',
    'chithu':'http://chithu.org/',
    'kagyuofficeE':'http://kagyuoffice.org',#英文版，注意跟之前版本的区别
    'dalailama':'https://www.dalailama.com/',
    'boxunE':'http://en.boxun.com/',
    'ntd':'http://www.ntd.tv',
    'tibet':'http://tibet.net/',
    'bod':'http://bod.asia/',
}




def send_ConfigWebname_to_redis():
    for webname in web_begin_url_config.keys():
        try:
            redis1.lpush(webname+':start_urls',web_begin_url_config[webname])
        except Exception as e:
            print(e)

def get_all_Rediswebsite_name():
    webname=set()
    for onewebsite in all_website_key:
        try:
            if ':' in onewebsite:
                website_name=onewebsite.split(':')[0]
                webname.add(website_name)
        except Exception as e:
            print e

    print len(webname)
    for onewebname in webname:
        print onewebname

    return list(webname)

def send_start_url_to_redis(web_name):
    if web_name in web_begin_url_config.keys():
        redis1.lpush(str(web_name)+':start_urls',str(web_begin_url_config[web_name]))
    else:
        print (web_name,' is not defined')

def deal_web_dupefilter(web_name):
    try:
        redis1.delete(web_name+':dupefilter')
    except Exception as e:
        print (e)

def deal_web_items(web_name):
    try:
        redis1.delete(web_name+':items')
    except Exception as e:
        print (e)

def deal_web_start_urls(web_name):
    try:
        redis1.delete(web_name+':start_urls')
    except Exception as e:
        print(e)

def deal_web_requests(web_name):
    try:
        redis1.delete(web_name+':requests')
    except Exception as e:
        print(e)



def clear_redis():
    for n,one in enumerate(get_all_Rediswebsite_name()):
        # send_start_url_to_redis(one)
        deal_web_dupefilter(one)
        deal_web_items(one)
        deal_web_requests(one)
        deal_web_start_urls(one)







if __name__ == '__main__':
    # clear_redis()

    # send_ConfigWebname_to_redis()

    # deal_web_dupefilter('tchrd')

    send_start_url_to_redis('tchrd')