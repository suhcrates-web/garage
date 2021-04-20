import requests, json, time
from bs4 import BeautifulSoup
from toolBox import fullcode_finder, dict_to_file
from datetime import datetime, timedelta, date
from krx_data import jusiksu, jonmok_for_jusiksu, sichong_crawl


##########
#화면번호 12025 (업종분류현황)에 나타난 시가총액을 이용해 기여율을 구함. 그러나 실패함.
#주가가 내렸는데도 시가총액은 오른 경우들이 발견됨. 시가총액이 정확히 반영 안되는 상황인것.

##ㄴㄴ 실패가 아니었다. 오히려 이게 정확한것. 주가 내렸는데 시총 오른건 무상증자******. 암튼 시총 오른건
#이거로 하는게 가장 정확

dics_last = sichong_crawl(kos='kosdaq', date0='20210415')
time.sleep(3)
dics_first = sichong_crawl(kos='kosdaq', date0='20210331')

real_key =[] #상폐, 상장종목 제거

for i in dics_first:
    if i in [*dics_last]:
        real_key.append(i)
    else:
        print(dics_first[i]['corp_nm'])
print('---------------------------')
for i in dics_last:
    if i in [*dics_first]:
        pass
    else:
        print(dics_last[i]['corp_nm'])
print('---------------------------')
print(f"{len([*dics_first])} / {len([*dics_last])} / {len(real_key)}")
dics = {}
first_sichong_list = []
last_sichong_list = []
for i in real_key:
    dics[i] = {}
    first_sichong = dics_first[i]['sichong']
    last_sichong = dics_last[i]['sichong']
    first_jongga = dics_first[i]['jongga']
    last_jongga = dics_last[i]['jongga']

    dics[i]['corp_cd']=i
    dics[i]['corp_nm']= dics_last[i]['corp_nm']
    dics[i]['upjong']= dics_last[i]['upjong']
    dics[i]['first_sichong']= first_sichong
    dics[i]['last_sichong']= last_sichong
    dics[i]['first_jongga']= first_jongga
    dics[i]['last_jongga']= last_jongga
    dics[i]['first_date0']= dics_first[i]['date0']
    dics[i]['last_date0']= dics_last[i]['date0']

    dics[i]['gap_sichong']= last_sichong - first_sichong
    dics[i]['plus_rate'] = (last_jongga - first_jongga)/first_jongga

    first_sichong_list.append(first_sichong)
    last_sichong_list.append(last_sichong)

first_sum = sum(first_sichong_list)
last_sum = sum(last_sichong_list)
tot_gap = last_sum - first_sum
tot_plus_rate = tot_gap / first_sum
print(f"기간 지수 상승률 : {tot_plus_rate}")
print(f"마지막날 시총 : {last_sum}")
print(f"첫날시총 : {first_sum}")
print(f"시총 갭 : {tot_gap}")

#기여율
for i in dics:
    gap_sichong = dics[i]['gap_sichong']
    giyeo_rate = gap_sichong / tot_gap
    dics[i]['giyeo_rate'] = giyeo_rate


dict_to_file(dics, 'kosdaq_giyeo_rate')


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
    dics_upjong[dics[i]['upjong']][corp_cd]['plus_rate'] = dics[i]['plus_rate']
    dics_upjong[dics[i]['upjong']][corp_cd]['giyeo_rate'] = dics[i]['giyeo_rate']

# print(dics_upjong)
for i in dics_upjong: #여기서 i는 업종    업종 > corp_cd > gap_sichong
    temp_list = []
    temp_first = []
    temp_last = []

    n = 0 #유상증자 숫자
    nn = 0 #전체 수
    for ii in dics_upjong[i]:
        nn += 1
        temp_list.append(int(dics_upjong[i][ii]['gap_sichong']))
        temp_first.append(int(dics_upjong[i][ii]['first_sichong']))
        temp_last.append(int(dics_upjong[i][ii]['last_sichong']))

        if dics_upjong[i][ii]['plus_rate'] * dics_upjong[i][ii]['giyeo_rate'] < 0: #부호 다름. : 증자
            n+=1
    dics_upjong_real[i] = {}
    dics_upjong_real[i]['upjong']= i
    dics_upjong_real[i]['gap_sum']= sum(temp_list)
    dics_upjong_real[i]['giyeo_rate']= sum(temp_list) / tot_gap
    dics_upjong_real[i]['plus_rate'] = (sum(temp_last) - sum(temp_first))/sum(temp_first)

    dics_upjong_real[i]['first_bijung']= sum(temp_first) / first_sum
    dics_upjong_real[i]['last_bijung']= sum(temp_last) / last_sum
    dics_upjong_real[i]['jeungja']= n
    dics_upjong_real[i]['jeungja_rate']= n / nn




dict_to_file(dics_upjong_real, 'kosdaq_giyeo_rate_upjong')