import requests, json, time
from bs4 import BeautifulSoup
from toolBox import fullcode_finder, dict_to_file
from datetime import datetime, timedelta, date
from krx_data import jusiksu, jonmok_for_jusiksu


##외국인 순매수목록 읽어서, 주식수 크롤링해서, 비율 구해서 파일 만들기
def jusiksu_to_rate():
    dics = {}
    with open('alien_list.csv', 'r') as f:
        temp = f.readlines()


    for i in temp:
        line = i.split(',')
        corp_cd = str(line[0])
        num_0 = 6 - len(corp_cd)
        corp_cd = num_0 * '0' +corp_cd
        corp_nm = line[1]
        mesu = line[2].replace('\n','')
        mesu_price = line[3].replace('\n','')
        dics[corp_cd]={}
        dics[corp_cd]['corp_cd'] = corp_cd
        dics[corp_cd]['corp_nm'] = corp_nm
        dics[corp_cd]['mesu'] = mesu
        dics[corp_cd]['mesu_price'] = mesu_price

    # print(dics)
    for i in dics:
        try:
            mesu = int(dics[i]['mesu'])
            jusu =  int(jusiksu(corp_cd = i))
            rate = mesu/jusu
            dics[i]['jusu'] = jusu
            dics[i]['rate'] = rate
            print(dics[i])
        except:
            print(f'{i} fail')
    dict_to_file(dics, 'mesurate')

##다시 위에꺼 읽어서, 주가상승률 구하기
def juga_rate():
    dics = {}
    with open('alien_list_after.csv', 'r') as f:
        temp = f.readlines()

    for i in temp:
        line = i.split(',')
        corp_cd = str(line[0])
        num_0 = 6 - len(corp_cd)
        corp_cd = num_0 * '0' +corp_cd
        corp_nm = line[1]
        mesu = line[2]
        mesu_price = line[3]
        jusu = line[4]
        rate = line[5].replace('\n','')
        dics[corp_cd]={}
        dics[corp_cd]['corp_cd'] = corp_cd
        dics[corp_cd]['corp_nm'] = corp_nm
        dics[corp_cd]['mesu'] = mesu
        dics[corp_cd]['mesu_price'] = mesu_price
        dics[corp_cd]['jusu'] = jusu
        dics[corp_cd]['rate'] = rate

    del dics['corp_cd']
    # print(dics)

    for i in dics:
        result = jonmok_for_jusiksu(corp_cd=i, strtDd='20210331', endDd='20210409')
        d_l =  result[0]
        d_f =  result[1]
        rate_juga =  result[2]
        dics[i]['d_l'] = d_l
        dics[i]['d_f'] = d_f
        dics[i]['rate_juga'] = rate_juga
        print(dics[i])
    dict_to_file(dics, 'jusiksu_jonmok')


# print(jonmok_for_jusiksu(corp_cd='009470', strtDd='20210331', endDd='20210409'))

if __name__ == '__main__':
    pass