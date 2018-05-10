#_*_coding:utf-8_*_
import os
import platform



ENCNname_dict={
    'AtcOrgAu':'澳大利亚藏人协会',
    'CFTchinese':'FT中文网',
    'chinaaid':'对华援助网',#有中文引文的区别
    'chinainperspective':'纵览中国',
    'chinesepen':'独立中文笔会',
    'chushigangdrug':'欧洲四水六岗',
    'dhokhamchushigangdrug':'多康四水六岗',
    'savetibet':'国际西藏运动',
    'dorjeshugden':'多杰雄登EN',
    'khabdha':'喀达网',
    'kirti92':'印度格尔登寺',
    'middleway':'看不见的西藏',
    'middleway-visiontimes':'看中国EN',
    'minghui':'明慧网',
    'radiosoh':'希望之声EN',
    'rtycnynj':'藏青会纽约和新泽西分会',
    'secretchina':'看中国CH',
    'studentsforafreetibet':'自由西藏学生运动官网',
    'tchrd':'西藏人权中心CN',
    'tibetanentrepreneurs':'西藏创业发展',
    'tibetanwomen':'藏妇会官网',
    'tibetanyouthcongress':'藏青会官网',
    'tibetsociety':'西藏协会',
    'tibetsun':'西藏太阳',
    'tibetswiss':'瑞士和比利时藏人协会',
    'uyghurcongress':'世界维吾尔大会',
    'xiongdeng':'多杰雄登CN',
    # 'sherig':'藏人行政中央文化部',
    
    
    'dalailamaworld':'达赖喇嘛官网',#中文
    'kagyuoffice':'嘎玛巴官网',#中文
    'tibetanparliament':'西藏流亡议会官网',#英文
    'xizang_zhiye':'藏人行政中央官网',
    'tibetexpress':'西藏快报',



}

def getNameCN(ENname):

    if ENname in ENCNname_dict.keys():
        cnName= ENCNname_dict[ENname]
    else:
        cnName= '未知网站'
    if platform.system() != 'Linux':
        # cnName=cnName.decode('utf-8').encode('gbk')
        cnName=cnName#全程使用utf-8以免出错

    return cnName