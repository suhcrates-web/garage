import requests, re, time
from bs4 import BeautifulSoup
from toolBox import eokwon, dict_to_file
from krx_data import jonmok_history

#38에서 장외시장가격 정보 긁어온 후 krx 이어붙임
def crawler():

    url = 'http://www.38.co.kr/html/fund/index.htm?o=nw&page=' #전체 리스트화면 url
    url2 = 'http://www.38.co.kr/chart/chart_page_new.php3?code=' #개별 장외종가 url
    login_url = 'https://www.38.co.kr/member/login/login_process.php' #로그인url

    ##로그인 ####
    session_requests = requests.session()
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                  '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '147',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': '__utmb=105967361.9.10.1616586757',
        'Host': 'www.38.co.kr',
        'Origin': 'http://www.38.co.kr',
        'Referer': 'http://www.38.co.kr/',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
    }
    payload = {
        'reurl': '%2Fhtml%2Ffund%2Findex.htm%3Fo%3Dnw',
        'time': '1616588438',
        'dauto': '8eb4c13d81e667badd6c2c626336ce64',
        'x': '34',
        'y': '12',
        'id': 'suhcrates',
        'passwd':'seoseoseo7'
    }
    temp = session_requests.post(
        login_url,
        data = payload,
        headers=header
    )




    ##### 38커뮤 리스트뽑기 ####
    dics = {}
    for n in range(1,21):
        url_0 = url + str(n)
        temp = session_requests.get(url_0)
        temp = BeautifulSoup(temp.content, 'html.parser')
        temp = temp.find('table', {'summary':'신규상장종목'})
        trs = temp.find_all('tr')
        print(f'페이지 {n}')
        dics_page = {}
        for i in trs:
            dic={}
            list = []
            tds = i.find_all('td')
            for ii in tds:
                list.append(ii.text.replace('\xa0',''))

            try:
                #이름구간
                name = list[0]
                type = ''#시장
                if bool(re.search('\(유가\)',name)): #코스피
                    type = 'kospi'
                    name.replace('(유가)','')
                else:
                    type = 'kosdaq'
                dic['name'] = name  #회사이름
                dic['type'] = type  #시장종류
                dic['day'] = list[1].replace('/','')  #상장일
                dic['now_p'] = list[2].replace(',','') #현재가
                dic['gongmo_p'] = list[4].replace(',','') #공모가
                dic['sicho_p'] = list[6].replace(',','') #시초가
                dic['first_p'] = list[8].replace(',','') #첫날 종가
                if dic['sicho_p'] in ['-']:
                    raise Exception('데이터 없음')

                corp_cd = re.search("(?<=\=)\d*$",tds[-1].find('a')['href'])[0]
                dic['code'] =corp_cd  # 종목코드
                dics_page[corp_cd] = dic

            except:
                pass

        time.sleep(3)

        #종목별 장외종가 뽑기
        delete_list = []
        for i in dics_page:
            print(str(i) + str([*dics_page]))
            print(dics_page[i])
            temp = session_requests.get(url2 + i)
            temp = BeautifulSoup(temp.content, 'html.parser')

            table = temp.find_all('table')
            tds = table[0].find_all('tr')[1].find_all('td')
            time.sleep(7)

            #장외종가
            jangwe_jonga = table[1].find_all('tr')[1].find('td').text.replace('\xa0','') #장외종가
            jangwe_jonga = eokwon(jangwe_jonga)
            if jangwe_jonga in ['','0','-', 0]:
                print(f'{i}here')
                delete_list.append(i)
            else:
                print(f'{i}here2')
                dics_page[i]['jangwe_jonga'] = jangwe_jonga

                #자본
                jabon = tds[0].text #자본금
                dics_page[i]['jabon'] = eokwon(jabon)

                jusicsu = tds[1].text.replace(',','') #주식수
                print(jusicsu)
                dics_page[i]['jusicsu'] = jusicsu.replace(',','')
                akmyen =tds[2].text #액면가
                dics_page[i]['akmyen'] = eokwon(akmyen)

                # 시가총액
                # sigachong = tds[3].text #시가총액

                #공모가, 주식수 기준 시가총액
                # print(dics[i])
                dics_page[i]['sigachong'] =int(dics_page[i]['gongmo_p']) * int(jusicsu)
                print(dics_page[i])
        print(delete_list)
        for iii in delete_list:
            del dics_page[iii]
        dics = {**dics, **dics_page}
        print("지금까지 총 "+str(len([*dics])))

    dict_to_file(dics, 'comu38')

    print('--------------------------------------')
    print('krx 이어붙이기 시작')



    #krx데이터 이어붙임.
    # 각 종목들의 상장 1~5일 종가, 30일 뒤(최근)가 뽑기.
    delete_list= []
    for i in dics:
        temp = dics[i]
        kos_cd = temp['type']
        datas = jonmok_history(kos_cd=kos_cd, corp_cd = i, strtDd=temp['day'])
        print(datas)

        if datas in ['0',0]:
            delete_list.append(i)
        else:
            list = ['d_1','d_2','d_3','d_4','d_5','d_30']
            for ii in range(len(list)):
                dics[i][list[ii]] = datas[ii]
        print(dics[i])
    print(delete_list)
    for i in delete_list:

        del dics[i]
    #결과물 출력
    dict_to_file(dics, 'after_krx')


#krx 이어붙이는거만 따로 함.
def second_shot():
    dics = {}
    with open('data/comu38.csv','r') as f:
        temp = f.readlines()
    header =temp[0].replace('\n','').split(',')

    for i in temp[1:]:
        line = i.replace('\n','').split(',')
        dics[line[7]] = {}
        for ii in range(len(line)):
            dics[line[7]][header[ii]] = line[ii]
    print(dics)

    #krx데이터 이어붙임.
    # 각 종목들의 상장 1~5일 종가, 30일 뒤(최근)가 뽑기.
    delete_list= []
    for i in dics:
        temp = dics[i]
        kos_cd = temp['type']
        datas = jonmok_history(kos_cd=kos_cd, corp_cd = i, strtDd=temp['day'])
        print(datas)

        if datas in ['0',0]:
            delete_list.append(i)
        else:
            list = ['d_1','d_2','d_3','d_4','d_5','d_30', 'd_60', 'd_len']
            for ii in range(len(list)):
                dics[i][list[ii]] = datas[ii]
        print(dics[i])
    print(delete_list)
    for i in delete_list:

        del dics[i]
    #결과물 출력
    dict_to_file(dics, 'after_krx_0405')



second_shot()