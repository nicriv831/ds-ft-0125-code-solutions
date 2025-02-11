# import datetime

import datetime as dt

#run function that will give days until thanksgiving from today's date
#using the actual Thanksgiving date for the sake of time, rather than calculating the 4th Thu in Nov

def days_for_turk():
  today = dt.date.today()
  thanksgiving = dt.date(2025, 11, 27)
  days_to_turkey = thanksgiving - today
  return days_to_turkey.days

print('There are ' + str(days_for_turk()) + ' days until turkey!!!')
