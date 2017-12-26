#_*_coding:utf-8_*_
import json


str_data='''2011年01月09日 上午01:26'''

# time_str=str_data.replace('年','-').replace('月','-').replace('日','')
# print time_str
#
# time_str2_l= time_str.split(' ')
# time_str2=time_str2_l[1]
# if '下午' in time_str2:
#     time_str3= time_str2.replace('下午','').split(':')[0]
#     time_str3_int=int(time_str3)
#     print time_str2_l[0]+' '+str(12+time_str3_int)+':'+time_str2.replace('下午','').split(':')[1]+':00'


def deal_publishtime_inside(publishtime):
    publish_time = publishtime.replace('年', '-').replace('月', '-').replace('日', '')
    time_split_2 = publish_time.split(' ')

    data_str=time_split_2[0]
    data_str_list=data_str.split('-')
    mounth=data_str_list[1]
    day=data_str_list[2]
    if len(mounth)<2:
        mounth='0'+mounth
    if len(day)<2:
        day='0'+day
    data_str=data_str_list[0]+'-'+mounth+'-'+day

    time_split_2_part2 = time_split_2[1]
    if '下午' in time_split_2_part2:
        time_part2_h_m = time_split_2_part2.replace('下午', '').split(':')
        time_split_2_h = int(time_part2_h_m[0])
        time_split_2_m = time_part2_h_m[1]
        time_split_2_h_add = 12 + time_split_2_h

        time_pm_finally = str(time_split_2_h_add) + ':' + time_split_2_m + ':00'
        return data_str + ' ' + time_pm_finally
    elif '上午' in time_split_2_part2:
        time_part2_h_m = time_split_2_part2.replace('上午', '').split(':')
        time_split_2_h = int(time_part2_h_m[0])
        time_split_2_m = time_part2_h_m[1]
        time_split_2_h_add = time_split_2_h

        if time_split_2_h_add < 10:
            time_split_2_h_add = '0' + str(time_split_2_h)

        time_am_finally = time_split_2_h_add+':' + time_split_2_m + ':00'
        return data_str + ' ' + time_am_finally


print deal_publishtime_inside(str_data)