from datetime import datetime, timedelta
import pandas, math
import statsmodels.api as sm
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.font_manager as fm
import numpy
from scipy.stats import t
from sklearn.linear_model import LinearRegression
from scipy.stats import f as f_test
from toolBox import dict_sort


######기본 dics 만들기 #####
with open('data/after_krx_0405_test.csv','r') as f:
    temp =f.readlines()

vip_list = {'302440':{'name':'sk바사'}, '293490':{'name':'카카오게임즈'}}

dics = {}

#칼럼 이름
names = temp[0].replace('\n','').split(',') #종목코드

#내용 채우기
for i in temp[1:]:
    i = i.replace('\n','')
    temp_0 = i.split(',')
    corp_cd = temp_0[7] #종목코드
    dics[corp_cd]={}
    for ii in range(len(temp_0)):
        dics[corp_cd][names[ii]]=temp_0[ii]
# print(dics)

####계산기 ######
total_num = 0  # 표본 전체 숫자
##첫날 찾기
days_temp = {}
for i in dics:
    total_num  +=1
    day=dics[i]['day']
    days_temp[i]={}
    days_temp[i]['day']=day

days_temp = dict_sort(days_temp, 'day')
first_day = days_temp[[*days_temp][-1]]['day']
first_day = datetime.strptime(first_day, '%Y%m%d')
last_day = days_temp[[*days_temp][0]]['day']
last_day = datetime.strptime(last_day, '%Y%m%d')


interval = (last_day - first_day).days
intv = math.floor(interval /7)
x_ints = []
for ii in range(0,8):
    x_ints.append((first_day + timedelta(days=intv*ii)).strftime('%Y-%m'))
x_ints = ['']+x_ints

print(f"첫날:{first_day.strftime('%Y-%m-%d')} // 마지막날:{last_day.strftime('%Y-%m-%d')}")

list=[]
x_value = []
x = []
y_value = []
x_days = []
over = []
very_good = []
###########################################
############## 기준 설정구간 #####################

# 1) 기본
temp=[]
day_list = []
real_num = 0
for i in dics:
    day = dics[i]['day']
    d_len = dics[i]['d_len']
    day =datetime.strptime(day,'%Y%m%d')

    days_from_start = (day - first_day).days
    jangwe = int(dics[i]['jangwe_jonga'])
    d_30 = int(dics[i]['d_30'])
    d_60 = int(dics[i]['d_30'])
    # rate = (d_30 - jangwe)/jangwe
    rate = (d_60 - jangwe)/jangwe
    if  d_len == False or day < datetime.strptime('20190101','%Y%m%d') or \
            day > datetime.strptime('20201231','%Y%m%d') :
        over.append(dics[i]['name'])
        pass
    elif rate >2:
        very_good.append(dics[i]['name'])
    else:
        day_list.append(dics[i]['day'])
        real_num +=1
        rate = rate*100
        x_days.append(day.strftime('%Y-%m-%d'))
        list.append([days_from_start , rate])
        x.append([days_from_start])  ### x축 이렇게 넣줘야함.
        x_value.append(days_from_start)
        y_value.append(rate)
        if i in [*vip_list]:
            vip_list[i]['x_axis'] = days_from_start
            vip_list[i]['y_axis'] = rate

first_day = min(day_list)
first_day = datetime.strptime(first_day, '%Y%m%d')
last_day = max(day_list)
last_day = datetime.strptime(last_day, '%Y%m%d')
print(f"첫날:{first_day.strftime('%Y-%m-%d')} // 마지막날:{last_day.strftime('%Y-%m-%d')}")


# 2)
# temp=[]
# real_num = 0
# for i in dics:
#     day = dics[i]['day']
#     day =datetime.strptime(day,'%Y%m%d')
#
#     days_from_start = (day - first_day).days
#     jangwe = int(dics[i]['jangwe_jonga'])
#     gongmo_p = int(dics[i]['gongmo_p'])
#     jusicsu = int(dics[i]['jusicsu'])
#     sigachong = gongmo_p * jusicsu
#     temp.append(sigachong)
#     d_30 = int(dics[i]['d_30'])
#     rate = (d_30 - jangwe)/jangwe
#     #중앙값으로 나눔  # 부호 > < 조절 가능
#     if (sigachong > 183551459900) or (rate>2) :
#         # print('here')
#         pass
#     else:
#         rate = rate*100
#         real_num +=1
#         x_days.append(day.strftime('%Y-%m-%d'))
#         list.append([days_from_start , rate])
#         x.append([days_from_start])  ### x축 이렇게 넣줘야함.
#         x_value.append(days_from_start)
#         y_value.append(rate)
#
#         if i in [*vip_list]:
#             vip_list[i]['x_axis'] = days_from_start
#             vip_list[i]['y_axis'] = rate


# print(dics)
# 3)
# temp=[]
# names = []
# real_num = 0
# real_date = []
# for i in dics:
#     day = dics[i]['day']
#     day =datetime.strptime(day,'%Y%m%d')
#
#     days_from_start = (day - first_day).days
#     jangwe = int(dics[i]['jangwe_jonga'])
#     gongmo_p = int(dics[i]['gongmo_p'])
#     jusicsu = int(dics[i]['jusicsu'])
#     type = dics[i]['type']
#     name = dics[i]['name']
#     sigachong = gongmo_p * jusicsu
#     temp.append(sigachong)
#     d_30 = int(dics[i]['d_30'])
#     rate = (d_30 - jangwe)/jangwe
#     #중앙값으로 나눔  # 부호 > < 조절 가능
#     if type == 'kospi' or rate>2 :
#         names.append(name)
#         # print('here')
#         pass
#     else:
#         days = day.strftime('%Y-%m-%d')
#         real_date.append(days)
#         real_num +=1
#         x_days.append(days_from_start)
#         list.append([days_from_start , rate])
#         x.append([days_from_start])  ### x축 이렇게 넣줘야함.
#         x_value.append(days_from_start)
#         y_value.append(rate)
# print(names)

# 4)
# first_day = datetime.strptime('2018-02-01', '%Y-%m-%d')
# last_day = datetime.strptime('2019-12-31', '%Y-%m-%d')
# interval = (last_day - first_day).days
# intv = math.floor(interval /7)
# x_ints = []
# for ii in range(0,8):
#     x_ints.append((first_day + timedelta(days=intv*ii)).strftime('%Y-%m'))
# x_ints = ['']+x_ints
#
# print(f"실제 첫날:{first_day.strftime('%Y-%m-%d')} // 마지막날:{last_day.strftime('%Y-%m-%d')}")
#
# temp=[]
# names = []
# real_num = 0
# real_date = []
# for i in dics:
#     day = dics[i]['day']
#     day =datetime.strptime(day,'%Y%m%d')
#
#     days_from_start = (day - first_day).days
#     jangwe = int(dics[i]['jangwe_jonga'])
#     gongmo_p = int(dics[i]['gongmo_p'])
#     jusicsu = int(dics[i]['jusicsu'])
#     type = dics[i]['type']
#     name = dics[i]['name']
#     sigachong = gongmo_p * jusicsu
#     temp.append(sigachong)
#     d_30 = int(dics[i]['d_30'])
#     rate = (d_30 - jangwe)/jangwe
#     #중앙값으로 나눔  # 부호 > < 조절 가능
#     if day < first_day or rate>2 :
#         # names.append(name)
#         # print('here')
#         pass
#     else:
#         days = day.strftime('%Y-%m-%d')
#         real_date.append(days)
#         real_num +=1
#         x_days.append(days_from_start)
#         list.append([days_from_start , rate])
#         x.append([days_from_start])  ### x축 이렇게 넣줘야함.
#         x_value.append(days_from_start)
#         y_value.append(rate)
#

# 5)
# temp=[]
# real_num = 0
# legend = {}
# x_ints =[]
# for i in dics:
#     day = dics[i]['day']
#     day =datetime.strptime(day,'%Y%m%d')
#
#     days_from_start = (day - first_day).days
#     jangwe = int(dics[i]['jangwe_jonga'])
#     gongmo_p = int(dics[i]['gongmo_p'])
#     jusicsu = int(dics[i]['jusicsu'])
#     sigachong = gongmo_p * jusicsu
#     temp.append(sigachong)
#     d_30 = int(dics[i]['d_30'])
#     rate = (d_30 - jangwe)/jangwe
#     rate = rate*100
#     if False:#rate > 200 or sigachong >1000000000000:
#         legend[i] = {}
#         legend[i]['name'] = dics[i]['name']
#         legend[i]['rate'] = rate
#         legend[i]['sigachong'] = sigachong
#         legend[i]['jangwe'] = jangwe
#         legend[i]['d_30'] = d_30
#         pass
#     else:
#
#         real_num +=1
#         # x_days.append(day.strftime('%Y-%m-%d'))
#         list.append([sigachong , rate])
#         x.append([sigachong])  ### x축 이렇게 넣줘야함.
#         x_value.append(sigachong)
#         y_value.append(rate)
#         if i in [*vip_list]:
#             vip_list[i]['x_axis'] = sigachong
#             vip_list[i]['y_axis'] = rate
#             vip_list[i]['jangwe'] = jangwe
#             vip_list[i]['d_30'] = d_30
#             vip_list[i]['d_1'] = int(dics[i]['d_1'])
#             x_ints.append(sigachong)




a = math.floor(max(x_value)/(10000000000*7))
x_ints =[a, 2*a, 3*a, 4*a, 5*a, 6*a , 7*a]
print(a)
print(f"very_good: {very_good}")
print(vip_list)
# print(legend)
print(numpy.median(temp))
############## 기준 설정구간 #####################
###########################################

print(f"{real_num}/{total_num}")

###
line_fitter = LinearRegression()
line_fitter.fit(x, y_value)
print(f"기울기 {line_fitter.coef_}")
print(f"기울기 연환산 {line_fitter.coef_ * 365}")


# print(line_fitter.predict([[x_value[-1]]]))

### R제곱 계수 구하기
y_bar = numpy.mean(y_value)
print(f"y바 : {y_bar}")
ssr_list = []
sst_list = []
sse_list = []
for i in range(len(x_value)):
    y_hat = line_fitter.predict([[x_value[i]]])
    y = y_value[i]
    ssr_list.append(pow( y_hat - y_bar, 2 ))
    sst_list.append(pow( y - y_bar, 2 ))
    sse_list.append(pow( y - y_hat, 2))

print(f"첫날:{line_fitter.predict([[x_value[-1]]])} // 막날 : {line_fitter.predict([[x_value[0]]])}")
print(f"처음:{line_fitter.predict([[min(x_value)]])} // 끝 : {line_fitter.predict([[max(x_value)]])}")
ssr = sum(ssr_list)
sst = sum(sst_list)
sse = sum(sse_list)
R2 = ssr/sst
print(f"R2: {R2}")

#### 기울기 적합도 구하기 : F검정

msr = ssr
mse = sse / (len(x_value)-2)
F_v = msr/mse

p_value =  f_test.cdf(F_v, 1, len(x_value)-2)

# print(f"F: {F_v}")
print(f"P: {p_value}")

##오차범위 구하기###


##MSE구하기
#MSE는 분산임. 나중에 루트 씌워줘야 s 가 됨.
x_bar = sum(x_value) / len(x_value)  #x의 평균

for i in [min(x_value), max(x_value)]:
    bottom = []
    for ii in x_value:
        bottom.append((ii - x_bar)**2)
    bottom = sum(bottom)

    e_dev = (mse*(1 + (1/len(x_value)) + ((i - x_bar)**2) / bottom))**(1/2)
    t_value = t.ppf(0.90, df = len(x_value)-2)

    predict = line_fitter.predict([[i]])
    ocha = e_dev * t_value
    print(f"오차범위 : {float(predict - ocha)}, {float(predict + ocha)}")

    over_th = False
    iii = 0
    while over_th == False:
        pre = predict + e_dev * t.ppf(iii, df = len(x_value)-2)
        if pre > 0:
            over_th = True
            print(f"0을 넘을 확률 {(1-iii)*100}")
            print(f"0을 못넘을 확률 {100 - (1-iii)*100}")
        else:
            iii = iii+ 0.001


### 0 이하로 내려갈 확률 #####



print(f"제외: {over}")

# print(real_date)
fig = plt.figure()



ax = fig.add_subplot(1,1,1)

#
x_test = []
y_test = []
tag_name = []
# for i in [*vip_list]:
#
#     tag_name.append(vip_list[i]['name'])
#     x_test.append(vip_list[i]['x_axis'])
#     y_test.append(vip_list[i]['y_axis'])


##플롯 구간 ####
font_path = r'C:\stamp\naver_font\NanumBarunpenB.ttf'
fontprop = fm.FontProperties(fname = font_path, size=10)
fontprop2 = fm.FontProperties(fname = font_path, size=15)
plt.plot(x,y_value,'o', color='navy')
plt.plot(x,line_fitter.predict(x))
plt.plot(x_test,y_test,'o', color='red')
plt.xlabel('공모가 기준 시총(백억원)', fontproperties=fontprop2)
plt.ylabel('장외가 대비 상장 30일 후 가격(%)', fontproperties=fontprop2)
plt.title('시총 규모별 실가격 비율', fontproperties=fontprop2)
print(vip_list)

ax.set_xticklabels(x_ints, rotation = 30)
for i, txt in enumerate(tag_name):
    ax.annotate(txt, (x_test[i]+1, y_test[i]+5), fontproperties=fontprop)

# ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))






# ax.xaxis.set_major_formatter(DateFormatter('%Y-%m'))

plt.show()


