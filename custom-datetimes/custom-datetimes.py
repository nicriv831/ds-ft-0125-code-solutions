# %%
import datetime as dt

date1 = '03/23/21'
d1 = dt.datetime.strptime(date1, '%m/%d/%y')
print(f'03/23/21 = {d1}')


# %%
date2 = '23/03/2021'
d2 = dt.datetime.strptime(date2, '%d/%m/%Y')
print(f'23/03/2021 = {d2}')


# %%
import pytz
pst = pytz.timezone('US/Pacific')
date3 = 'March 23rd, 2021 13:01 US/Pacific'
new_date = date3.replace('rd', "")
newer_date = new_date.replace(' US/Pacific', "")
d3 = dt.datetime.strptime(newer_date, '%B %d, %Y %H:%M').astimezone(pst)
print(f'March 23rd, 2021 13:01 US/Pacific = {d3}')


# %%

date4 = '1:01pm 23rd March, 2021 Europe/London'
london_time = pytz.timezone('Europe/London')
date4_clean = date4.replace('rd', "")
date4_clean_notz = date4_clean.replace(' Europe/London','')
date4_clean_notz
d4 = dt.datetime.strptime(date4_clean_notz, '%I:%M%p %d %B, %Y').astimezone(london_time)
print(f'1:01pm 23rd March, 2021 Europe/London = {d4}')


# %%

date5 = '1616482800'
d5 = dt.datetime.fromtimestamp(int(date5))
print(f'1616482800 = {d5}')


# %%

date6 = '2021-03-23T12:00:53.034-07:00'
date6_clean = date6.replace('T', " ")
d6 = dt.datetime.strptime(date6_clean, '%Y-%m-%d %H:%M:%S.%f%z')
# d6 = dt.datetime.fromisoformat(date6)
# #d6 = dt.datetime.strptime(date6, '%m/%d/%y')
print(f'2021-03-23T12:00:53.034-07:00 = {d6} manually coding')

#EASIER ALTERNATIVE

d6_with_iso = dt.datetime.fromisoformat(date6)
print(f'2021-03-23T12:00:53.034-07:00 = {d6_with_iso} using fromisoformat')
