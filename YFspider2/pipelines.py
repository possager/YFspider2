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





#BASIC_FILE是存放本地备份文件的数据的，里边会有很多网站名的文件夹，文件夹里会有publish_time文件夹，之后再里边就是数据文件
#BASIC_FILE2是一个数据缓存的文件夹，原计划是里边存放所有的文件，没有文件夹了，就是数据文件，之后定期网服务器推送，推送一个删一个
#       但是但是，这个功能还没有设计完全，这要要在push_data或者KafkaConnector1中去修改，目前还没有这样设置。

#       所以现在的实际情况是，push_data会直接从BASIC_FILE中逐层遍历所有文件，再完成推送，还不会删除文件。这个再第一次历史数据抓取时
#       还可以这么用，但是后边的增量爬取的时候，就必须需要增加BASXIC_FILE2这个文件夹已经对应的程序功能。

BASIC_FILE="E:/data_ll2_xz"
BASIC_FILE2='E:/data_ll2_all_xz'
if platform.system()=='Linux':#BigDATA's workstation
    BASIC_FILE='/home/spider/silence/spider_test/spider_content'
    BASIC_FILE2='/home/spider/silence/spider_test/spider_content_all'




class Yfspider2Pipeline(object):#这个类系统默认生成的，没使用过。
    def process_item(self, item, spider):
        return item



class YfspidersetdefaultValue(object):
    '''
    这个类用来设置数据的默认格式，如like_count默认是0，content默认是'',
    '''
    def process_item(self,item,spider):
        for itemkey in item.fields:
            if itemkey in ['read_count','reproduce_count','reply_count','dislike_count','like_count']:
                item.setdefault(itemkey,0)
            elif itemkey in ['reply_nodes','like_nodes','img_urls','video_urls']:
                item.setdefault(itemkey,[])
            else:
                item.setdefault(itemkey,None)

        return item


class save_data_to_file(object):
    '''
    文件存储模块，将解析出来的数据以json的格式存储到硬盘中去，路径最上边的BASIC_FILE，不是BASIC_FILE2，BASIC_FILE2在save_data_to_RemoteFile_XMX中。
    '''
    def process_item(self,item,spider):
        '''
        标准的middleware函数，具体参考官方文档。

        :param item: 从spider中解析出来的对象，或者从其它middleware中解析出来的item，具体顺序可以在setting中设置，详细参见官方帮助文档。
        :param spider: spider的名称，可以提取spider中的某些字段，比如spdier_name
        :return: 这里没有返回对象，直接存储到了本地文件中。   如有需要，具体如何返回数据，参见官方文档。
        '''
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
        '''
        数据文件名的生成函数，根据参数来生成1101中要求的数据文件的格式名。
        还要根据BASIC_FILE中的字段来生成相应的路径，如果没有，就自动创建。


        :param publish_time:
        :param plant_form:
        :param urlOruid:
        :param newsidOrtid:
        :param datatype:
        :return: file_path是文件的具体存储路径，注意：filename不只是文件名，还包括了前边的文件路径，比如：
                /home/spider/silence/spider_test/spider_content/具体一个1101中的文件的名称。
        '''
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

        file_path=BASIC_FILE+'/speeches'+'/'+CNname+'/'+publish_time_split_2[0]
        filename=file_path+'/'+filename#看到没有，这里就把前边的路径名加在filename之前了，所以filename不单单是一个文件名。

        return filename,file_path

    def examing_datetime_format(self,timestr):
        '''
        检测时间格式是否符合规定的一个函数。因为在实际情况中，有些网页解析出来的时间格式不对，情况比较多，因为要在文件名中用到这个字段所以这个字段比较重要，
        所以这里单独设置一个模块用来处理这些意外情况。有些网站没有publish_time，跟大数据商量好了，一律使用2018-02-01 00:00:00

        :param timestr: publsh_time
        :return: 处理过后的publish_time
        '''
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
                    return time.strptime('2018-02-01 00:00:00','%Y-%m-%d %H:%M:%S')

    def save_data(self,file_path, file, full_data):  # 因为后来要用到存储的时候的文件名，先要调用里边的文件名，所以生成文件名和爬取数据结果应该分开写。
        #file相当于是file_path+'/'+filename
        '''

        :param file_path: 数据存储的文件路径，
        :param file: 数据文件路径名+数据文件名
        :param full_data: 一个完成的处理过后的，只差存储了，的一个数据。
        :return: 这里已经是爬虫的末端了，
        '''
        if os.path.exists(file_path):
            with open(file, 'w+') as cmfl:
                json.dump(full_data, cmfl)
        else:
            os.makedirs(file_path)
            with open(file, 'w+') as cmfl:
                json.dump(full_data, cmfl)


class save_data_to_RemoteFile_XMX(object):
    '''
    跟前边的save_data_to_file一样，代码结构和变量名都是一样的，因为是copy过来的。
    只是将数据存储到BASIC_FILE2中，而不是BASIC_FILE，将来推数据肯定是从这个文件夹中推的，不过目前还没有设计好。需要修改push_data模块和KafkaConnection模块。
    因为他们要求推两个服务器，所以，到底怎么推送，怎么删除，还没有写好。目前跑第一次的历史数据没问题，增量爬取时需要注意这里。

    '''
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
    beacuse the spider_time are timestamp13，之前是10，可以上个class中修改，不过担心修改不完成，一处修改导致其它
    地方出先bug，所以直接添加了这个模块。
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
