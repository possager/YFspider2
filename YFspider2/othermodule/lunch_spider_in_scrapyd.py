#_*_coding:utf-8_*_
import requests
import json
import time


# console_url='http://192.168.6.230:6800'
console_url='http://127.0.0.1:6800'

def get_all_spiders():
    response1=requests.get(url=console_url+'/listspiders.json?',params={'project':'default'})
    result1=json.loads(response1.text)
    print('爬虫项目状态是-------------',result1['status'],'可用的爬虫数量：-------',len(result1['spiders']))
    print('可用的爬虫列表：')
    for onespider in result1['spiders']:
        print(onespider)
    return result1['spiders']


def start_a_spider_job(project='default',spidername=None):
    if spidername:
        spider_task={
            'project':project,
            'spider':spidername,
            'setting':None,
            'jobid':None
        }
        respons1=requests.post(url=console_url+'/schedule.json',data=spider_task)
        print(respons1.text)

    else:
        print('请输入一个正确的爬虫名称')


def cancel_job(jobId=None,project='default'):
    if jobId:
        cancel_spider={
            'project':project,
            'job':jobId
        }
        response1=requests.post(url=console_url+'/cancel.json',data=cancel_spider)

        print(response1.text)


def get_all_Jobs(project='default'):
    all_job_url=console_url+'/listjobs.json'
    all_job_dict={
        'project':project
    }
    response1=requests.get(url=all_job_url,params=all_job_dict)
    datajson=json.loads(response1.text)
    runingSpider=datajson['running']
    # for i in runingSpider:
    #     print('start_time:  ',i['start_time'])
    #     print('pid:         ',i['pid'])
    #     print('jobid:       ',i['id'])
    #     print('spiderName:  ',i['spider'])
    #     print('-----------------------------------')
    return runingSpider
    # print(response1.text)



def start_all_spider():
    all_spider_avalid=get_all_spiders()
    for one_spidername in all_spider_avalid:
        if one_spidername in ['aboluowang','bbc_com_zhongwen_simp','boxun',
                                  'boxunE','CFTchinese','chinaaid','chinainperspective','chinesepen']:
            start_a_spider_job(spidername=one_spidername)

    print('_____________\n'
          ' all start  \n'
          '_____________')

def cancel_all_spider_job():
    all_jobs_id=get_all_Jobs()
    for one_jod in all_jobs_id:
        print('cancel jobId-----',one_jod)
        cancel_job(jobId=str(one_jod['id']))
        time.sleep(1)

    print('_____________\n'
          ' all cancel  \n'
          '_____________')


def lanch_spider_runing_just_10Min():
    start_all_spider()
    while True:
        all_spider_jobs=get_all_Jobs()
        for onejob in all_spider_jobs:
            start_time=onejob['start_time'].split('.')[0]
            pid=onejob['pid']
            jobid=onejob['id']
            spider=onejob['spider']

            timenow=time.time()
            spidertime_str=start_time
            spider_start_time_touple=time.strptime(spidertime_str,'%Y-%m-%d %H:%M:%S')
            spider_start_time_stamp=time.mktime(spider_start_time_touple)
            if timenow-spider_start_time_stamp>60*5:
                cancel_job(jobid)
                print('has cancle a job,which name is ',spider,' which id is ',jobid)


        time.sleep(20)





if __name__ == '__main__':
    # get_all_spiders()
    # start_a_spider_job(spidername='chinainperspective')
    # cancel_job(jobId='27cf4bf04de011e880a40862667c7ee1')
    # get_all_Jobs()
    # cancel_all_spider_job()
    # start_all_spider()
    lanch_spider_runing_just_10Min()