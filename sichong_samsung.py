import requests, json, time
from bs4 import BeautifulSoup
from toolBox import fullcode_finder, dict_to_file, dict_sort
from datetime import datetime, timedelta, date
from krx_data import jusiksu, jonmok_for_jusiksu, sichong_crawl


#### 시총 대비 상위 30 기업 비율,   삼성 비율. #####

with open(f'data/sichong_samsung.csv', 'w') as f:
    f.writelines(['today0',',','sum_all',',','sum_30',',','samsung',',','sum_30_rate',',','samsung_rate','\n'])
dics = {}

num = (datetime.today() - datetime.strptime('20180101', '%Y%m%d')).days

for i in range(num+1):
    try:
        today = date.today()
        today0 = (today - timedelta(days=i)).strftime('%Y%m%d')

        dics_temp = sichong_crawl(kos='kospi', date0=today0)
        dics_temp = dict_sort(dics_temp, key0 = 'sichong')
        # print(dics_temp)


        sum_all_list = [] #모든기업 시총
        sum_30_list = [] #시총30위기업

        n =0
        for i in dics_temp:
            n+=1
            sum_all_list.append(dics_temp[i]['sichong'])
            if n<=30:
                sum_30_list.append(dics_temp[i]['sichong'])

        sum_all = sum(sum_all_list)
        sum_30 = sum(sum_30_list)
        samsung = dics_temp['005930']['sichong']
        sum_30_rate = sum_30/sum_all
        samsung_rate = samsung/sum_all

        dics[today0]={}
        dics[today0]['today'] = today0
        dics[today0]['sum_all'] = sum_all
        dics[today0]['sum_30'] = sum_30
        dics[today0]['samsung'] = samsung
        dics[today0]['sum_30_rate'] = sum_30_rate
        dics[today0]['samsung_rate'] = samsung_rate

        with open(f'data/sichong_samsung.csv', 'a+') as f:
            f.writelines([str(today0),',',str(sum_all),',',str(sum_30),',',str(samsung),',',str(sum_30_rate),',',
                          str(samsung_rate),'\n'])
        print(dics[today0])
        time.sleep(4)
    except:
        pass
