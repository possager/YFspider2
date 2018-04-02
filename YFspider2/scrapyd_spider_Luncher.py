#_*_coding:utf-8_*_
import requests
import json
import time


console_url='http://192.168.6.230:6800'


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
    for i in runingSpider:
        print('start_time:  ',i['start_time'])
        print('pid:         ',i['pid'])
        print('jobid:       ',i['id'])
        print('spiderName:  ',i['spider'])
        print('-----------------------------------')
    return runingSpider
    # print(response1.text)



def start_all_spider():
    all_spider_avalid=get_all_spiders()
    for one_spidername in all_spider_avalid:
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



if __name__ == '__main__':
    # get_all_spiders()
    # start_a_spider_job(spidername='middleway')
    # cancel_job(jobId='1c2691c032d611e8b1ca30b49e7b08df')
    # get_all_Jobs()
    cancel_all_spider_job()
    # start_all_spider()