# %%
#Write a function to calculate age based on date of birth

import datetime as dt

def how_old():
  # User enters bday
  bday = dt.datetime.strptime(input('Please enter your birthday in YYYY-MM-DD format'), '%Y-%m-%d')
  # Get today's date
  today = dt.datetime.today()
  # For a birthday that is yet to pass this year
  if (today.month, today.day) < (bday.month, bday.year):
    age = (today.year - bday.year) - 1
    return print(f'You are {age} years old!')
  # For a birthday that has already passed this year
  else:
    age = today.year - bday.year
    return print(f'You are {age} years old!')


how_old()
