# %%
import json

#opens/reads a json file and converts it to a dictionary

with open('json_file.txt', 'r') as f:
 lines = json.load(f)

# %%
# need to loop through each dictionary entry (there are two, each entry is its own dictionary) and list each of their keys and values

for entry in lines:
 print(f'id: {entry['id']}')
 print(f'name: {entry['name']}')
 print(f'sports: {entry['sports']}')
 print('=' * 10)

# %%
with open('daily_covid_cases.json', 'r') as file:
  covid_data = json.load(file)

print('meta')
print(f'build_time: {covid_data['meta']['build_time']}')
print(f'license: {covid_data['meta']['license']}')
print(f'version: {covid_data['meta']['version']}')
print(f'field_definitions: {covid_data['meta']['field_definitions']}')
print("\ndata")
print(f'date: {covid_data['data']['date']}')
print(f'states: {covid_data['data']['states']}')
print(f'cases: {covid_data['data']['cases']}')
print(f'testing: {covid_data['data']['testing']}')
print(f'outcomes: {covid_data['data']['outcomes']}')
