#_*_coding:utf-8_*_
import redis
import requests



redis1=redis.Redis(host='127.0.0.1',port=6379,db=0)
all_website_key= redis1.keys('*')


web_begin_url_config={
    'kirti92':'www.kirti92.org',
    'tibetanwomen':'tibetanwomen.org',
    'tchrd':'tchrd.org/chinese/',
    'uyghurcongress':'www.uyghurcongress.org',
    'ftchinese':'http://www.ftchinese.com/',#这个进去就有广告
    'chushigangdrug':'www.chushigangdrug.ch',
    'middleway':'woeser.middle-way.net',
    'tibetsun':'www.tibetsun.com',
    'sherig':'www.sherig.org/tb/',
    'xiongdeng':'xiongdeng.com',#这个分中英文，这个是中文的
    'secretchina':None,#?
    'tibetsociety':'www.tibetsociety.com',
    'dhokhamchushigangdrug':'dhokhamchushigangdrug.com',
    'tibetanentrepreneurs':'tibetanentrepreneurs.org',
    'khabdha':'www.khabdha.org',
    'atc_org_au':'www.atc.org.au',
    'dorjeshugden':'www.dorjeshugden.com',#多杰雄登英文版
    'chinesepen':'www.chinesepen.org',
    'minghui':'www.minghui.org',
    'tibetanyouthcongress':'www.tibetanyouthcongress.org',
    'studentsforafreetibet':'www.studentsforafreetibet.org',
    'chinainperspective':'chinainperspective.com',
    'radiosoh':'www.radiosoh.com',#希望之声英文版，分中英文
    'chinaaid':'www.chinaaid.net',
    'tibetswiss':'www.tibetswiss.ch',



}





def get_all_website_name():
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


def send_start_url_to_redis(web_name,start_url):
    redis_command=''




if __name__ == '__main__':
    get_all_website_name()