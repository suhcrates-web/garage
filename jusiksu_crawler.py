import requests, json, time
from bs4 import BeautifulSoup
from toolBox import fullcode_finder, dict_to_file
from datetime import datetime, timedelta, date
from krx_data import jusiksu, jonmok_for_jusiksu



def open_dics():
    dics = {}
    dics_todo = []
    with open('data/kosdaq_jusiksu.csv', 'r') as f:
        temp = f.readlines()
    for i in temp[1:]:
        line = i.replace('\n','').split(',')
        corp_cd = str(line[0])
        corp_nm = line[1]
        first_price = line[2]
        last_price = line[3]

        dics[corp_cd] = {}


        dics[corp_cd]['corp_cd'] = corp_cd
        dics[corp_cd]['corp_nm'] = corp_nm
        dics[corp_cd]['first_price'] = first_price
        dics[corp_cd]['last_price'] = last_price
        try:
            jusiksu_num = line[4]
            dics[corp_cd]['jusiksu_num'] = jusiksu_num
        except:
            dics_todo.append(corp_cd)
    return dics, dics_todo
# print(dics)
dics, dics_todo = open_dics()
print(len(dics_todo))
n = 0
for i in dics_todo:
    n +=1
    print(f"{n}/{len(dics_todo)}")
    dics, dics_todo = open_dics()
    jusiksu_num = jusiksu(kos = 'kosdaq', corp_cd= i)
    # print(jusiksu_num)
    dics[i]['jusiksu_num'] = jusiksu_num
    # print(dics)
    dict_to_file(dics, 'kosdaq_jusiksu')
