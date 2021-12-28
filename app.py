#!/usr/bin/python
#
# UN Member States Scraper
# v1.0
# Author: Alex Castro
# Link: https://github.com/alexpcastro/UN-Member-States-Scraper

from bs4 import BeautifulSoup
import requests
import pandas as pd

# Manual setting of url as list
url = 'https://www.un.org/en/about-us/member-states'

# Use requests library to get HTML from URL
resp = requests.get(url)
bsoup = BeautifulSoup(resp.text,features="lxml")

#countries = []
#links = []
data = []
# Select each country name HTML element from the page
for card in bsoup.select('.card-body'):
    # Get Country
    country = card.h2.text
    # Get Admission Date
    date = card.select_one('.mb-1').text.split(': ')[1]
    # Check if title contains a link
    link = None
    description = None
    if card.h2.a:
        link = card.h2.a['href']
        link_resp = requests.get(link)
        link_bsoup = BeautifulSoup(link_resp.text,features="lxml")
        description = link_bsoup.select_one('.field-item').text

    data.append([country,date,link, description])


df = pd.DataFrame(data, columns = ['Country','Date','Link','Description'])
df.to_excel("un_member_states.xlsx",index=False)
df.to_csv("un_member_states.csv",index=False)
