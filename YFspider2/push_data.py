#_*_coding:utf-8_*_
import requests
import json
import os





BASIC_FILE='E:/data_ll'

url_post='http://192.168.6.211:2348/mapDatas'



def get_file():
    file_list=os.listdir(BASIC_FILE)
    for one_file in file_list:
        BASIC_FILE_webname=BASIC_FILE+'/'+one_file
        file_list2=os.listdir(BASIC_FILE_webname+'/data')
        for one_date_dir in file_list2:
            BASIC_FILE_webname_data_date=BASIC_FILE_webname+'/data/'+one_date_dir
            jsonfile_list=os.listdir(BASIC_FILE_webname_data_date)
            for one_jsonfile in jsonfile_list:
                print one_jsonfile


                #with  as fl:
                    #filedata=fl.read()

                dict_post={
                    'fileName':one_jsonfile,
                    'path':BASIC_FILE_webname_data_date.replace('/','\\').replace('E:\\data_ll\\','')+'\\',

                }
                file = {'file': open(BASIC_FILE_webname_data_date+'/'+one_jsonfile,'rb')}



                filename1='E:/data_ll/atc_org_au/data/2009-07-03/1521608222000_speeches_2018-03-21_TouTiao_1521608222000_0cec332edf2fc54376f1a0040691ac19'
                file222=open(BASIC_FILE_webname_data_date+'/'+one_jsonfile,'rb')

                response1=requests.post(url=url_post,data=dict_post,files={'file':file222})
                print response1.text
                pass



if __name__ == '__main__':
    get_file()