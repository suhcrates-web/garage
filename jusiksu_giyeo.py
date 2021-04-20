import requests, json, time
from bs4 import BeautifulSoup
from toolBox import fullcode_finder, dict_to_file
from datetime import datetime, timedelta, date
from krx_data import jusiksu, jonmok_for_jusiksu

####파일정리구간
dics_jusiksu= {}
with open('data/kosdaq_jusiksu.csv','r') as f:
    temp=f.readlines()
for i in temp[1:]:
    line = i.replace('\n','').split(',')
    corp_cd = str(line[0])
    corp_nm = line[1]
    first_price = line[2]
    last_price = line[3]
    jusiksu_num = line[4]
    dics_jusiksu[corp_cd] = {}
    dics_jusiksu[corp_cd]['corp_cd'] = corp_cd
    dics_jusiksu[corp_cd]['corp_nm'] = corp_nm
    dics_jusiksu[corp_cd]['first_price'] = first_price
    dics_jusiksu[corp_cd]['last_price'] = last_price
    dics_jusiksu[corp_cd]['jusiksu_num'] = jusiksu_num


dics_upjong = {}
with open('data/kosdaq_upjong.csv','r') as f:
    temp=f.readlines()
for i in temp[1:]:
    line = i.replace('\n','').split(',')
    corp_cd = str(line[0])
    corp_nm = line[1]
    upjong = line[2]
    dics_upjong[corp_cd] = {}
    dics_upjong[corp_cd]['corp_cd'] = corp_cd
    dics_upjong[corp_cd]['corp_nm'] = corp_nm
    dics_upjong[corp_cd]['upjong'] = upjong

print(len([*dics_jusiksu]))
print(len([*dics_upjong]))
for i in dics_jusiksu:
    dics_jusiksu[i]['upjong'] =dics_upjong[i]['upjong']
# print(dics_jusiksu)


#####계산 후 재저장 구간 #######
dics = dics_jusiksu
temp = 0
first_sichong_list = []
last_sichong_list = []
for i in dics:
    first_price = int(dics[i]['first_price'])
    last_price = int(dics[i]['last_price'])
    jusiksu_num = int(dics[i]['jusiksu_num'])

    first_sichong = first_price * jusiksu_num
    last_sichong = last_price * jusiksu_num
    gap_sichong = last_sichong - first_sichong
    plus_rate = (last_sichong - first_sichong)/first_sichong

    dics[i]['first_sichong'] = first_sichong
    dics[i]['last_sichong'] = last_sichong
    dics[i]['gap_sichong'] = gap_sichong
    dics[i]['plus_rate'] = plus_rate

    first_sichong_list.append(first_sichong)
    last_sichong_list.append(last_sichong)
    temp += first_sichong

# print(first_sichong_list)
first_sum = sum(first_sichong_list)
last_sum = sum(last_sichong_list)
# print(f"{len(first_sichong_list)}  {len(last_sichong_list)}")
# print(f"{first_sum}  {last_sum}")
tot_plus_rate =  (last_sum - first_sum)/first_sum
tot_gap = last_sum - first_sum
print(f"기간 지수 상승률 : {tot_plus_rate}")
print(f"마지막날 시총 : {last_sum}")
print(f"첫날시총 : {first_sum}")
print(f"시총 갭 : {tot_gap}")

for i in dics:
    gap_sichong = int(dics[i]['gap_sichong'])
    giyeo_rate = gap_sichong / tot_gap
    dics[i]['giyeo_rate'] = giyeo_rate


# dict_to_file(dics, 'kosdaq_giyeo_rate')


#### 업종별 기여율 ######
#업종별로 나눠서 시총 계산.

#업종별
dics_upjong = {}
dics_upjong_real = {} #출력용
for i in dics:
    corp_cd = dics[i]['corp_cd']
    try:
        dics_upjong[dics[i]['upjong']][corp_cd] ={}
    except:
        dics_upjong[dics[i]['upjong']] ={}
        dics_upjong[dics[i]['upjong']][corp_cd] ={}
    dics_upjong[dics[i]['upjong']][corp_cd]['corp_cd'] = dics[i]['corp_cd']
    dics_upjong[dics[i]['upjong']][corp_cd]['corp_nm'] = dics[i]['corp_nm']
    dics_upjong[dics[i]['upjong']][corp_cd]['gap_sichong'] = dics[i]['gap_sichong']
    dics_upjong[dics[i]['upjong']][corp_cd]['first_sichong'] = dics[i]['first_sichong']
    dics_upjong[dics[i]['upjong']][corp_cd]['last_sichong'] = dics[i]['last_sichong']

# print(dics_upjong)
for i in dics_upjong: #여기서 i는 업종    업종 > corp_cd > gap_sichong
    temp_list = []
    temp_first = []
    temp_last = []

    for ii in dics_upjong[i]:
        temp_list.append(int(dics_upjong[i][ii]['gap_sichong']))
        temp_first.append(int(dics_upjong[i][ii]['first_sichong']))
        temp_last.append(int(dics_upjong[i][ii]['last_sichong']))
    dics_upjong_real[i] = {}
    dics_upjong_real[i]['upjong']= i
    dics_upjong_real[i]['gap_sum']= sum(temp_list)
    dics_upjong_real[i]['giyeo_rate']= sum(temp_list) / tot_gap
    dics_upjong_real[i]['plus_rate'] = (sum(temp_last) - sum(temp_first))/sum(temp_first)




# print(dics_upjong_real)
# dict_to_file(dics_upjong_real, 'kosdaq_giyeo_rate_upjong')