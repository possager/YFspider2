# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json
import time
import datetime
import os
import hashlib
import platform
from YFspider2.othermodule.pipeline_nameEN_to_nameCN import getNameCN






BASIC_FILE="E:/data_ll_xz"
BASIC_FILE2='E:/data_ll_all_xz'
if platform.system()=='Linux':#BigDATA's workstation
    BASIC_FILE='/home/spider/silence/spider_test/spider_content'
    BASIC_FILE2='/home/spider/silence/spider_test/spider_content_all'




class Yfspider2Pipeline(object):
    def process_item(self, item, spider):
        return item



class YfspidersetdefaultValue(object):
    def process_item(self,item,spider):
        for itemkey in item.fields:
            item.setdefault(itemkey,None)
        return item


class save_data_to_file(object):
    def process_item(self,item,spider):
        item_dict=dict(item)
        plant_form=spider.name
        publish_time=item['publish_time']
        urlOruid=item['url']
        newsidOrtid=item['id']
        datatype='news'

        filename,file_path=self.create_file_str(publish_time=publish_time,plant_form=plant_form,urlOruid=urlOruid,newsidOrtid=newsidOrtid,datatype=datetime)

        self.save_data(file_path=file_path,file=filename,full_data=item_dict)

        # try:
        #     self.save_data(file_path='E:/data_all_xizang',file='E:/data_all_xizang/'+filename.split('/')[-1],full_data=item_dict)
        # except Exception as e:
        #     print e

        return item



    def create_file_str(self,publish_time,plant_form,urlOruid,newsidOrtid,datatype):
        try:
            publish_time_array = self.examing_datetime_format(publish_time)
            publish_time_stramp=time.mktime(publish_time_array)
            publish_time_stramp_str_13=str(int(publish_time_stramp*1000))
        except:
            print 'wrong in create publish_time_stramp_str_13'
            publish_time_stramp_str_13='time_wrong'

        urlhashlib=hashlib.md5(urlOruid).hexdigest()
        urlhashlib_str=str(urlhashlib)

        CNname=getNameCN(plant_form)

        try:
            publish_time_split_2=publish_time.split(' ')
            publish_time_split_2=[str(x) for x in publish_time_split_2]
        except Exception as e:
            publish_time_split_2=['time_wrong','time_wrong']
        filename=publish_time_stramp_str_13+'_'+CNname+'_speeches_'+str(publish_time_split_2[0])+'_'+plant_form+'_'+publish_time_stramp_str_13+'_'+urlhashlib_str

        file_path=BASIC_FILE+'/speeches'+'/'+CNname+'/'+publish_time_split_2[0]#需要文件的名，还需要文件之前的路径。
        filename=file_path+'/'+filename

        return filename,file_path


    def examing_datetime_format(self,timestr):
        try:
            timestrlist = time.strptime(timestr, '%Y-%m-%d %H:%M:%S')
            return timestrlist
        except:
            try:
                timestrlist = time.strptime(timestr, '%Y-%m-%d %H:%M')
                return timestrlist
            except:
                try:
                    timestrlist = time.strptime(timestr, "%Y-%m-%d")
                    return timestrlist
                except:
                    print '时间格式有误'
                    print timestr
                    return time.strptime('1111-11-11 11:11:11','%Y-%m-%d %H:%M:%S')

    def save_data(self,file_path, file, full_data):  # 因为后来要用到存储的时候的文件名，先要调用里边的文件名，所以生成文件名和爬取数据结果应该分开写。
        #file相当于是file_path+'/'+filename
        if os.path.exists(file_path):
            with open(file, 'w+') as cmfl:
                json.dump(full_data, cmfl)
        else:
            os.makedirs(file_path)
            with open(file, 'w+') as cmfl:
                json.dump(full_data, cmfl)


class save_data_to_RemoteFile_XMX(object):
    def process_item(self,item,spider):
        item_dict = dict(item)
        plant_form = spider.name
        publish_time = item['publish_time']
        urlOruid = item['url']
        newsidOrtid = item['id']
        datatype = 'news'


        def create_file_name(publish_time,plant_form,urlOrtid,datatype):
            try:
                publish_time_tuple=time.strptime(publish_time,'%Y-%m-%d %H:%M:%S')
                timestamp=time.mktime(publish_time_tuple)
                timestamp_str_13=str(int(timestamp*1000))
            except Exception as e:
                print e
                publish_time_tuple=time.strptime('2018-02-01 00:00:00','%Y-%m-%d %H:%M:%S')
                timestamp=time.mktime(publish_time_tuple)
                timestamp_str_13=str(int(timestamp*1000))

            urlhashlib = hashlib.md5(urlOruid).hexdigest()
            urlhashlib_str = str(urlhashlib)


            CNname=getNameCN(plant_form)

            try:
                publish_time_split_2 = publish_time.split(' ')
                publish_time_split_2=[str(x) for x in publish_time_split_2]
            except Exception as e:
                publish_time_split_2 = ['time_wrong', 'time_wrong']

            filename = timestamp_str_13 + '_speeches_' + CNname + '_' + str(publish_time_split_2[
                0]) + '_'+ plant_form + '_' + timestamp_str_13 + urlhashlib_str

            return filename

        def save_data(file_path, file, full_data):  #
            if os.path.exists(file_path):
                with open(file, 'w+') as cmfl:
                    json.dump(full_data, cmfl)
            else:
                os.makedirs(file_path)
                with open(file, 'w+') as cmfl:
                    json.dump(full_data, cmfl)

        filename=create_file_name(publish_time,plant_form,urlOruid,datatype)

        save_data(file_path=BASIC_FILE2,file=BASIC_FILE2+'/'+filename,full_data=item_dict)

        return item


class adjust_type(object):
    '''
    to change the form of data,beacause some normal has changed!such as spider_time,publish_user,
    beacuse the spider_time are timestamp
    '''

    def process_item(self,item,spider):
        #change spider_time
        spider_time=item['spider_time']
        time_tuple=time.localtime(int(spider_time/1000))
        spider_date=time.strftime('%Y-%m-%d %H:%M:%S',time_tuple)
        item['spider_time']=spider_date


        #change publish_user
        publish_user=item['publish_user']
        if not publish_user:
            publish_user=spider.name
        item['publish_user']=publish_user

        return item
