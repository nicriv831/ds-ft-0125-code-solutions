# %%
import requests

url = 'https://api.themoviedb.org/3/search/movie?query=star%20wars&include_adult=false&language=en-US&page=1'

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlYzFhOTY0ZjIzNzU5NzdkNWJmOTQ1ZjI5YWQ5Njk3MiIsIm5iZiI6MTczOTI0MTI0NC45MzI5OTk4LCJzdWIiOiI2N2FhYjcxYzVjMGU2N2U1NmJiYjE5MTQiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.PIPWM9RKB7Lkr7DpX2z7sjOJ91fi4PNM6FCjMaInhJ8"
}

response = requests.get(url, headers=headers)

star_wars = response.json()


# %%
import pandas as pd


star_wars_cleaned = star_wars['results']

starwars_df = pd.DataFrame(star_wars_cleaned)

starwars_sorted = starwars_df.sort_values(by='popularity', ascending = False)

starwars_sorted
