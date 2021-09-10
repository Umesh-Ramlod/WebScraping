import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

url = "https://www.imdb.com/search/title/?count=100&groups=top_1000&sort=user_rating%27"

# step 01 get the html
r = requests.get(url)
HTML_Content = r.content

# step 02 parse the html
# BeautifulSoup will convert the fetched htl contents into a structure like trees
soup = BeautifulSoup(HTML_Content, "html.parser")

# step 03 : traverse the html tree
title = soup.title

# variables for storing data
movie_name = []
year = []
duration = []
ratings = []
actors = []
directors = []
# collect all movie data
movie_data = soup.findAll("div", attrs={"class": "lister-item mode-advanced"})

for details in movie_data:
    name = details.h3.a.text
    movie_name.append(name)

    yor = details.h3.find('span', class_="lister-item-year text-muted unbold").text.replace('(', '').replace(')', '')
    year.append(yor)

    dur = details.p.find('span', class_='runtime').text.replace(" min", "")
    duration.append(dur)

    rate = details.find('div', class_='inline-block ratings-imdb-rating').text.replace("\n", "")
    ratings.append(rate)

    cast = details.find('p', class_="").text.replace("\n", "").replace("\t", "")
    sample = re.split(":", cast)
    actors.append(sample[2])
    sample2 = re.sub("\s", "", sample[1])
    sample2 = re.sub("Stars", "", sample2)
    sample2 = sample2[0:len(sample2) - 1]
    directors.append(sample2)

# Now create Dataframe
dataset = pd.DataFrame(
    {'Name Of Movie': movie_name, 'Year Of Release': year, 'Runtime': duration, 'Rating': ratings, 'Cast': actors,
     'Directors': directors})
print(dataset)
