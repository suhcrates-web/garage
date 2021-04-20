from datetime import timedelta, datetime


# print(datetime.today().strftime('%Y%m%d'))
for i in range(60):
    print((datetime.today()- timedelta(days=i)).strftime('%Y%m%d'))