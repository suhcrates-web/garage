import requests, re, time
from bs4 import BeautifulSoup
from toolBox import eokwon, dict_to_file
from krx_data import jonmok_history,  jonmok_for_seongjang


###성장주 가치주  종목별 통계 정리 코드 #####
dics = {}

with open('seongjang_list.txt','r', encoding='utf-8') as f:
    temp = f.readlines()
    seongjang_dic = {}
    for i in temp:
        a= i.replace('\n','')
        a = a.split(',')
        seongjang_dic[a[1]]={}
        seongjang_dic[a[1]]['code']=a[1]
        seongjang_dic[a[1]]['name']=a[0]
with open('gachi_list.txt','r', encoding='utf-8') as f:
    temp = f.readlines()
    gachi_dic = {}
    for i in temp:
        a= i.replace('\n','')
        a = a.split(',')
        gachi_dic[a[1]]={}
        gachi_dic[a[1]]['code']=a[1]
        gachi_dic[a[1]]['name']=a[0]
print(seongjang_dic)
print(gachi_dic)


def start_to_end_rate(dic, filename, strtDd, endDd):
    for i in dic:
        print(i)
        result = jonmok_for_seongjang(corp_cd=i, strtDd=strtDd, endDd=endDd)
        dic[i]['m0301']= result[0]
        dic[i]['m0330']= result[1]
        dic[i]['m_rate']= result[2]
    dict_to_file(dic, filename)

start_to_end_rate(seongjang_dic,'seongjang_rate_2', '20210201', '20210228')
start_to_end_rate(gachi_dic,'gachi_rate_2', '20210201', '20210228')

