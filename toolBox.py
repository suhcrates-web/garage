import re
import requests, json, time
from bs4 import BeautifulSoup

#'억원'을 일반 수로 환산. 쉼표 떼줌
def eokwon(x):
    x = x.replace('원', '').replace(',','')
    if bool(re.search('억',x)):
        x = x.replace('억','')
        x = int(x) * 100000000
    return str(x)

#krx에서  스톡코드 (123123) 넣으면 풀코드(kr1244593945959)로 환산. 이게 있어야 krx에서 종목별 검색이 됨.
def fullcode_finder(kos='kospi', corp_cd=''):
    if kos == 'kospi':
        kos_code = 'STK'
    elif kos == 'kosdaq':
        kos_code = 'KSQ'
    url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'

    header = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7',
        'Connection': 'keep-alive',
        'Content-Length': '315',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': '__smVisitorID=mgX3gboq6Sf; __utmz=139639017.1612159881.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); finder_stkisu_finderCd=finder_stkisu; finder_stkisu_param1=STK; finder_stkisu_typeNo=0; JSESSIONID=K9rSGrpfJ1s7Hw4LCKMDumbkzaITTI2I08tBy9q5v8zIUswQJM4i1zICE9FYfepM.bWRjX2RvbWFpbi9tZGNvd2FwMS1tZGNhcHAwMQ==; finder_stkisu_codeVal2=KR7334970001; __utma=139639017.1458902062.1612159881.1615958375.1616638506.6; __utmc=139639017; __utmt=1; __utmb=139639017.1.10.1616638506; finder_stkisu_tbox=282330%2FBGF%EB%A6%AC%ED%85%8C%EC%9D%BC; finder_stkisu_codeNm=BGF%EB%A6%AC%ED%85%8C%EC%9D%BC; finder_stkisu_codeVal=KR7282330000',
        'Host': 'data.krx.co.kr',
        'Origin': 'http://data.krx.co.kr',
        'Referer': 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.90 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    data = {
        'mktsel': kos_code, # 코스닥은 KSQ,  코스피는 STK 인듯.
        'typeNo': '0',
        'searchText':corp_cd,
        'bld': """dbms/comm/finder/finder_stkisu"""
    }
    # print(data)
    temp = requests.post(url, data=data, headers = header)
    temp = json.loads(temp.content.decode('utf-8'))
    # print(temp)
    time.sleep(3)
    return temp['block1'][0]['full_code']

#딕셔너리를 csv파일로
def dict_to_file(dic, filename ):
    with open(f'data/{filename}.csv', 'w') as f:
        list = []
        for i in [*dic[[*dic][0]]]:
            list.append(str(i))
            list.append(',')
        list[-1] = '\n'
        # print(list)
        f.writelines(list)

        for i in [*dic]:
            list = []
            for ii in [*dic[i]]:
                list.append(str(dic[i][ii]))
                list.append(',')
            list[-1] = '\n'
            # print(list)
            f.writelines(list)



#딕셔너리 순서정렬
def dict_sort(dict0, key0='key0'):
    dict0 = {k:v for k, v in sorted(dict0.items(), reverse=True, key=lambda item: item[1][key0])}
    return dict0


# print(fullcode_finder(kos='kosdaq',corp_cd='361390'))