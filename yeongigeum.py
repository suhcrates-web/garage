import requests, json, time
from bs4 import BeautifulSoup
from toolBox import fullcode_finder, dict_to_file
from datetime import datetime, timedelta, date
from krx_data import jusiksu, jonmok_for_jusiksu

#연기금 등. 투자자별 매수매도 일별 추세 확인.  코스피, 코스닥, 전체.
#toojaja : 금융투자, 보험, 투신, 사모, 은행, 기타금융, 연기금 등, 기관합계, 기타법인, 개인, 외국인, 기타외국인
def yeongigeum(kos = 'kosdaq', strtDd='', toojaja=''): #날짜는 하나만
    if kos == 'kospi':
        kos_code = 'STK'
    elif kos == 'kosdaq':
        kos_code = 'KSQ'
    elif kos == 'all':
        kos_code = 'ALL'
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
        'bld': 'dbms/MDC/STAT/standard/MDCSTAT02201',
        'inqTpCd': '1',
        'trdVolVal': '2',
        'askBid': '3',
        'mktId': kos_code,
        'etf': 'EF',
        'etn': 'EN',
        'elw': 'EW',
        'strtDd': strtDd,
        'endDd': strtDd,
        'share': '2',
        'money': '3',
        'csvxls_isNo': 'false'
    }
    temp = requests.post(url, data=data, headers = header)
    temp = json.loads(temp.content.decode('utf-8'))['output']
    dics = {}
    dics[toojaja]={}
    for i in temp:
        if i['INVST_TP_NM'] == toojaja:
            dics[toojaja][strtDd]={}
            dics[toojaja][strtDd]['strtDd']=strtDd
            dics[toojaja][strtDd]['soon_mesu']=int(i['NETBID_TRDVAL'].replace(',',''))

            time.sleep(3)
            return dics
        else:
            pass



toojaja = '연기금 등'
print(yeongigeum(kos='all',strtDd='20210416',toojaja =toojaja))
dics_all={toojaja:{}}
dics_kospi={toojaja:{}}
dics_kosdaq={toojaja:{}}


for i in range(60):
    strtDd = (datetime.today()- timedelta(days=i)).strftime('%Y%m%d')
    dics_all[toojaja][strtDd]={}
    dics_kospi[toojaja][strtDd]={}
    dics_kosdaq[toojaja][strtDd]={}

    dics_all[toojaja][strtDd] = yeongigeum(kos='all',strtDd=strtDd,toojaja =toojaja)[toojaja][strtDd]
    dics_kospi[toojaja][strtDd] = yeongigeum(kos='kospi',strtDd=strtDd,toojaja =toojaja)[toojaja][strtDd]
    dics_kosdaq[toojaja][strtDd] = yeongigeum(kos='kosdaq',strtDd=strtDd,toojaja =toojaja)[toojaja][strtDd]
    print(i)
# print(dics_all)

dict_to_file(dics_all[toojaja], '연기금_all')
dict_to_file(dics_kospi[toojaja], '연기금_kospi')
dict_to_file(dics_kosdaq[toojaja], '연기금_kosdaq')