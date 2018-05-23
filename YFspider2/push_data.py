#_*_coding:utf-8_*_
import requests
import json
import os
from YFspider2.pipelines import BASIC_FILE2,BASIC_FILE
from YFspider2.othermodule.pipeline_nameEN_to_nameCN import getNameCN
import re
from KafkaConnector1 import Producer
import time



url_post='http://192.168.6.47:2348/mapDatas'




def get_file():
    file_list=os.listdir(BASIC_FILE+'/speeches')
    for one_file in file_list:
        if one_file=='CFTchinese':
            continue
        BASIC_FILE_webname=BASIC_FILE+'/speeches'+'/'+one_file
        # BASIC_FILE_webname2=BASIC_FILE+'/speeches'+'/'+one_file.decode('gbk').encode('utf-8')
        file_list2=os.listdir(BASIC_FILE_webname)
        for one_date_dir in file_list2:
            BASIC_FILE_webname_data_date=BASIC_FILE_webname+'/'+one_date_dir
            # BASIC_FILE_webname_data_date2 = BASIC_FILE_webname2 + '/' + one_date_dir
            jsonfile_list=os.listdir(BASIC_FILE_webname_data_date)
            for one_jsonfile in jsonfile_list:
                print one_jsonfile
                # Re_find_rightName=re.compile(r'\d{13}_speeches_.*?_\d{4}\-\d{2}\-\d{2}_\S*?_\d{13}_\S*?_')
                # result_one_jsonfile=Re_find_rightName.findall(one_jsonfile)
                # if not result_one_jsonfile:
                #     continue
                # CNname=getNameCN(one_file)
                # dict_post={
                #     'fileName':result_one_jsonfile[0].strip('_'),
                #     'path':BASIC_FILE_webname_data_date.replace('/','\\').split('data_ll_xz')[-1].replace(one_file,CNname)+'\\',
                #
                # }
                #
                # file222=open(BASIC_FILE_webname_data_date+'/'+one_jsonfile,'rb')
                #
                # response1=requests.post(url=url_post,data=dict_post,files={'file':file222})
                # print response1.text
                # pass
                # CNname=getNameCN(one_file)
                # CN_one_jsonfile_raw1=one_jsonfile.split('speeches')
                # CN_one_jsonfile_raw2=CN_one_jsonfile_raw1[1].split(one_file)[-1]
                # CN_one_jsonfile=CN_one_jsonfile_raw1[0]+'speeches_'+CNname+'_'+one_date_dir+'_'+one_file+CN_one_jsonfile_raw2[-1]
                #
                # os.rename(os.path.join(BASIC_FILE_webname_data_date,one_jsonfile),os.path.join(BASIC_FILE_webname_data_date,CN_one_jsonfile))


                #-----------------------------------------------------------------------------------------------------
                dict1={
                    'fileName':one_jsonfile,
                    # 'path':BASIC_FILE_webname_data_date.replace('/','\\').split('data_ll_xz')[-1].lstrip('\\'),
                    'path': BASIC_FILE_webname_data_date.split('data_ll_xz')[-1].lstrip('/')

                }

                # file222=open(BASIC_FILE_webname_data_date+'/'+one_jsonfile,'rb')
                # response1=requests.post(url=url_post,data=dict1,files={'file':file222})
                # print response1.text
                with open(BASIC_FILE_webname_data_date+'/'+one_jsonfile,'rb') as fl:
                    file222=json.load(fl)
                yield (file222,one_jsonfile)



if __name__ == '__main__':
    # get_file()
    host = '192.168.6.187:9092,192.168.6.188:9092,192.168.6.229:9092,192.168.6.230:9092'
    p = Producer(host)
    i = 0
    ztids = [339, 338]


    for onefile in get_file():
        print(onefile)
        i+=1
        if i>100:
            break
        p.send('test',{'data':onefile[0]},onefile[1],time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(time.time()))))