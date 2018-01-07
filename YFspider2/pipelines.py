# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

BASIC_FILE="E:/data_ll"
import json
import time
import datetime
import os
import hashlib



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

        publish_time_split_2=publish_time.split(' ')
        filename=plant_form+'_'+plant_form+'_'+publish_time_stramp_str_13+'_'+urlhashlib_str+'_'+newsidOrtid

        file_path=BASIC_FILE+'/'+plant_form+'/'+'data'+'/'+publish_time_split_2[0]#需要文件的名，还需要文件之前的路径。
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
        if os.path.exists(file_path):
            with open(file, 'w+') as cmfl:
                json.dump(full_data, cmfl)
        else:
            os.makedirs(file_path)
            with open(file, 'w+') as cmfl:
                json.dump(full_data, cmfl)

