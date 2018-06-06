#_*_coding:utf-8_*_
import requests
import json
import os
from YFspider2.pipelines import BASIC_FILE2,BASIC_FILE
from YFspider2.othermodule.pipeline_nameEN_to_nameCN import getNameCN
import re
from KafkaConnector1 import Producer
import time



url_post='http://192.168.6.211:2348/mapDatas'




def push_to_XMX():
    file_list=os.listdir(BASIC_FILE+'/speeches')
    for one_file in file_list:
        if one_file=='CFTchinese':
            continue
        BASIC_FILE_webname=BASIC_FILE+'/speeches'+'/'+one_file
        file_list2=os.listdir(BASIC_FILE_webname)
        for one_date_dir in file_list2:
            BASIC_FILE_webname_data_date=BASIC_FILE_webname+'/'+one_date_dir
            jsonfile_list=os.listdir(BASIC_FILE_webname_data_date)
            for one_jsonfile in jsonfile_list:
                print one_jsonfile
                #-----------------------------------------------------------------------------------------------------
                dict1={
                    'fileName':one_jsonfile,
                    'path':BASIC_FILE_webname_data_date.replace('/','\\').split('data_ll2_xz')[-1].lstrip('\\'),
                }
                with open(BASIC_FILE_webname_data_date+'/'+one_jsonfile,'rb') as fl:
                    try:
                        jsondict=json.load(fl)
                        jsondict2={
                            'data':jsondict
                        }
                        jsondict3={
                            'content':jsondict2,
                            'update_time':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(time.time())))
                        }
                    except:
                        continue
                with open(BASIC_FILE_webname_data_date+'/'+one_jsonfile,'w+') as fl2:
                    json.dump(jsondict3, fl2)


                file222=open(BASIC_FILE_webname_data_date+'/'+one_jsonfile,'rb')
                response1=requests.post(url=url_post,data=dict1,files={'file':file222})
                print response1.text


def push_to_kafka():
    def get_file():
        file_list = os.listdir(BASIC_FILE + '/speeches')#
        for one_file in file_list:
            BASIC_FILE_webname = BASIC_FILE + '/speeches' + '/' + one_file
            file_list2 = os.listdir(BASIC_FILE_webname)
            for one_date_dir in file_list2:
                BASIC_FILE_webname_data_date = BASIC_FILE_webname + '/' + one_date_dir
                jsonfile_list = os.listdir(BASIC_FILE_webname_data_date)
                for one_jsonfile in jsonfile_list:
                    with open(BASIC_FILE_webname_data_date + '/' + one_jsonfile, 'rb') as fl:
                        file222 = json.load(fl)
                    yield (file222, one_jsonfile)

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

if __name__ == '__main__':
    push_to_XMX()



    # host = '192.168.6.187:9092,192.168.6.188:9092,192.168.6.229:9092,192.168.6.230:9092'
    # p = Producer(host)
    # i = 0
    # ztids = [339, 338]
    #
    #
    # for onefile in get_file():
    #     print(onefile)
    #     i+=1
    #     if i>100:
    #         break
    #     p.send('test',{'data':onefile[0]},onefile[1],time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(time.time()))))