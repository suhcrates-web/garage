import requests, json, time
from bs4 import BeautifulSoup
from toolBox import fullcode_finder, dict_to_file
from datetime import datetime, timedelta, date
from krx_data import jusiksu, jonmok_for_jusiksu

#전종목 등락률,  주식수 나온 페이지 찾아서 연결하려고 했는데
#이 경우 증자된건 계산이 안됨. sichong_giyeo 가 가장 정확

#전종목 등락률 krx12002
#결과값 : corp_cd , corp_nm , first_jongga, last_jongga, plus_rate, first_date, last_date  / 기준일 전날 종가, 막날 종가.
def jongmok_plma(kos = 'kosdaq', strtDd='', endDd=''): #20210414 형식
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
        'Cookie': '__smVisitorID=mgX3gboq6Sf; __utmz=139639017.1612159881.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=('
                  'none); __utma=139639017.1458902062.1612159881.1614737745.1615958375.5; ',
        # 'finder_stkisu_finderCd=finder_stkisu; finder_stkisu_param1=STK; finder_stkisu_typeNo=0; JSESSIONID=K9rSGrpfJ1s7Hw4LCKMDumbkzaITTI2I08tBy9q5v8zIUswQJM4i1zICE9FYfepM.bWRjX2RvbWFpbi9tZGNvd2FwMS1tZGNhcHAwMQ==; finder_stkisu_codeVal2=KR7334970001; finder_stkisu_tbox=138930%2FBNK%EA%B8%88%EC%9C%B5%EC%A7%80%EC%A3%BC; finder_stkisu_codeNm=BNK%EA%B8%88%EC%9C%B5%EC%A7%80%EC%A3%BC',#; finder_stkisu_codeVal=KR7138930003',
        'Host': 'data.krx.co.kr',
        'Origin': 'http://data.krx.co.kr',
        'Referer': 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.90 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    # corp_cd = '361390'
    # kos_cd = 'kosdaq'
    # temp_date = datetime.strptime(strtDd, '%Y%m%d')
    # endDd = datetime.strftime(temp_date + timedelta(days=60), '%Y%m%d')
    # print(strtDd)
    # print(endDd)

    data = {
        'bld': 'dbms/MDC/STAT/standard/MDCSTAT01602',
        'mktId': kos_code,
        'strtDd': strtDd,
        'endDd': endDd,
        'adjStkPrc_check': 'Y',
        'adjStkPrc': '2',
        'share': '1',
        'money': '1',
        'csvxls_isNo': 'false'
    }
    temp = requests.post(url, data=data, headers = header)
    temp = json.loads(temp.content.decode('utf-8'))['OutBlock_1'] #리스트임
    dics = {}
    for i in temp:
        corp_cd = i['ISU_SRT_CD']
        first_jongga = int(i['BAS_PRC'].replace(',',''))
        last_jongga = int(i['TDD_CLSPRC'].replace(',',''))
        dics[corp_cd] ={}
        dics[corp_cd]['corp_cd'] =corp_cd
        dics[corp_cd]['corp_nm'] =i['ISU_ABBRV'] #회사이름
        dics[corp_cd]['first_jongga'] = first_jongga  # 기준일 전날 종가
        dics[corp_cd]['last_jongga'] = last_jongga #마지막날 종가
        dics[corp_cd]['plus_rate'] = (last_jongga - first_jongga)/ first_jongga
        dics[corp_cd]['first_date'] = strtDd  #기준일
        dics[corp_cd]['last_date'] = endDd
    return dics

# jongmok_plma(kos='kosdaq', strtDd='20210407', endDd='20210415')

#전종목기본정보 크롤링
def jongmok_info(kos='kosdaq'):
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
        'Cookie': '__smVisitorID=mgX3gboq6Sf; __utmz=139639017.1612159881.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=('
                  'none); __utma=139639017.1458902062.1612159881.1614737745.1615958375.5; ',
        # 'finder_stkisu_finderCd=finder_stkisu; finder_stkisu_param1=STK; finder_stkisu_typeNo=0; JSESSIONID=K9rSGrpfJ1s7Hw4LCKMDumbkzaITTI2I08tBy9q5v8zIUswQJM4i1zICE9FYfepM.bWRjX2RvbWFpbi9tZGNvd2FwMS1tZGNhcHAwMQ==; finder_stkisu_codeVal2=KR7334970001; finder_stkisu_tbox=138930%2FBNK%EA%B8%88%EC%9C%B5%EC%A7%80%EC%A3%BC; finder_stkisu_codeNm=BNK%EA%B8%88%EC%9C%B5%EC%A7%80%EC%A3%BC',#; finder_stkisu_codeVal=KR7138930003',
        'Host': 'data.krx.co.kr',
        'Origin': 'http://data.krx.co.kr',
        'Referer': 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.90 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    data = {
        'bld': 'dbms/MDC/STAT/standard/MDCSTAT01901',
        'mktId': kos_code,
        'share': '1',
        'csvxls_isNo': 'false'
    }
    temp = requests.post(url, data=data, headers = header)
    temp = json.loads(temp.content.decode('utf-8')) #리스트임
    print(temp)