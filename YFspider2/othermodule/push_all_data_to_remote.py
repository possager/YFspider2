#_*_coding:utf-8_*_
import requests
import os
from YFspider2.pipelines import BASIC_FILE2,BASIC_FILE


def get_all_filename(dir_path):
    file_list=os.listdir(dir_path)
    print file_list
    for one_file in file_list:
        print one_file


if __name__ == '__main__':
    get_all_filename(BASIC_FILE2)