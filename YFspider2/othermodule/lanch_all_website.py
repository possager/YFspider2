#_*_coding:utf-8_*_
import redis
import requests
import random

#
redis1=redis.StrictRedis(host='127.0.0.1',port=6379,db=1)
# pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
# redis1 = redis.Redis(connection_pool=pool)


# pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
# redis1 = redis.Redis(connection_pool=pool)
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

# def begin_start_urls_to_redis(web_name):
#     if web_name=='kirti92':
#         redis1.lpush('kirti92:start_urls','http://www.kirti92.org/')
#     elif web_name=='tibetanwomen':
#         redis1.lpush('tibetanwomen:start_urls','http://tibetanwomen.org/')
#     elif web_name=='tchrd':
#         redis1.lpush('tchrd:start_urls','http://tchrd.org/chinese/')
#     elif web_name == 'uyghurcongress':
#         redis1.lpush('uyghurcongress:start_urls', 'http://www.uyghurcongress.org/cn/')
#     elif web_name=='ftchinese':
#         redis1.lpush('ftchinese:start_urls','http://www.ftchinese.com/')
#     elif web_name=='chushigangdrug':
#         redis1.lpush('chushigangdrug:start_urls','http://www.chushigangdrug.ch/')
#     elif web_name=='middleway':
#         redis1.lpush('middleway:start_urls','http://woeser.middle-way.net/')
#     elif web_name=='tibetsun':
#         redis1.lpush('tibetsun:start_urls','https://www.tibetsun.com/')
#     elif web_name=='tibetanwomen':
#         redis1.lpush('tibetanwomen:start_urls','http://tibetanwomen.org/')
#     elif web_name=='sherig':
#         redis1.lpush('sherig:start_urls','http://www.sherig.org/tb/')
#     elif web_name=='xiongdeng':
#         redis1.lpush('xiongdeng:start_urls','http://xiongdeng.com/')
#     elif web_name=='secretchina':
#         redis1.lpush('secretchina:start_urls','https://www.secretchina.com/')
#     elif web_name=='tibetsociety':
#         redis1.lpush('tibetsociety:start_urls','http://www.tibetsociety.com/')
#     elif web_name=='dhokhamchushigangdrug':
#         redis1.lpush('dhokhamchushigangdrug:start_urls','http://dhokhamchushigangdrug.com/')
#     elif web_name=='tibetanentrepreneurs':
#         redis1.lpush('tibetanentrepreneurs:start_urls','http://tibetanentrepreneurs.org/')
#     elif web_name=='khabdha':
#         redis1.lpush('khabdha:start_urls','http://www.khabdha.org/')
#     elif web_name=='atc_org_au':
#         redis1.lpush('atc_org_au:start_urls','http://www.atc.org.au/')
#     elif web_name=='dorjeshugden':
#         redis1.lpush('dorjeshugden:start_urls','http://www.dorjeshugden.com/')
#     elif web_name=='chinesepen':
#         redis1.lpush('chinesepen:start_urls','http://www.chinesepen.org/')
#     elif web_name=='minghui':
#         redis1.lpush('minghui:start_urls','http://www.minghui.org/')
#     elif web_name=='tibetanyouthcongress':
#         redis1.lpush('tibetanyouthcongress:start_urls','https://www.tibetanyouthcongress.org/')
#     elif web_name=='studentsforafreetibet':
#         redis1.lpush('studentsforafreetibet:start_urls','http://www.studentsforafreetibet.org/')
#     elif web_name=='chinainperspective':
#         redis1.lpush('chinainperspective:start_urls','http://chinainperspective.com/')
#     elif web_name=='radiosoh':
#         redis1.lpush('radiosoh:start_urls','http://radiosoh.com/')
#     elif web_name=='chinaaid':
#         redis1.lpush('chinaaid:start_urls','http://www.chinaaid.net/')
#     elif web_name=='tibetswiss':
#         redis1.lpush('tibetswiss:start_urls','http://www.tibetswiss.ch/index-bo.html')










if __name__ == '__main__':
    # for n,one in enumerate(get_all_Rediswebsite_name()):
    #     # send_start_url_to_redis(one)
    #     deal_web_dupefilter(one)
    #     deal_web_items(one)
    #     deal_web_requests(one)
    #     deal_web_start_urls(one)
    send_ConfigWebname_to_redis()
    # deal_web_dupefilter('atc_org_au')
    # send_start_url_to_redis('bbc_com_zhongwen_simp')